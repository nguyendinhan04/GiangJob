from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import json
import datetime
import re


key_words = [
    "Language school",
    "Language center",
    "International school",
    "English school",
]

citys = [
    "Hà Nội",
    "Hải Phòng",
    "Đà Nẵng",
    "Cần Thơ",
    "TP. Hồ Chí Minh",
]

def is_valid_email(email):
    """
    Kiểm tra xem chuỗi có phải là email hợp lệ không
    Loại bỏ các pattern có thể là số điện thoại hoặc false positive
    """
    import re
    
    # Loại bỏ các pattern rõ ràng không phải email
    invalid_patterns = [
        r'^\d+@\d+$',  # Chỉ toàn số
        r'^\d+@\d+\.\d+$',  # Pattern như số điện thoại
        r'^[0-9\.\-\+\(\)\s]+@[0-9\.\-\+\(\)\s]+$',  # Chỉ chứa ký tự số điện thoại
        r'@\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',  # IP address
        r'@localhost$',  # localhost
        r'@example\.',  # example domains
        r'@test\.',  # test domains
        r'@placeholder\.',  # placeholder domains
        r'@sample\.',  # sample domains
        r'@domain\.',  # generic domain
        r'@email\.',  # generic email
        r'@mail\.',  # generic mail domain when suspicious
    ]
    
    # Kiểm tra các pattern không hợp lệ
    for pattern in invalid_patterns:
        if re.search(pattern, email, re.IGNORECASE):
            return False
    
    # Kiểm tra domain hợp lệ
    domain_part = email.split('@')[1] if '@' in email else ''
    
    # Domain phải có ít nhất một dấu chấm và ít nhất 2 ký tự sau dấu chấm cuối
    if not re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', domain_part):
        return False
    
    # Loại bỏ email có quá nhiều số
    local_part = email.split('@')[0] if '@' in email else ''
    if len(re.findall(r'\d', local_part)) > len(local_part) * 0.7:  # Nếu >70% là số
        return False
    
    # Kiểm tra độ dài hợp lý
    if len(email) < 5 or len(email) > 254:
        return False
    
    # Kiểm tra local part không bắt đầu hoặc kết thúc bằng dấu chấm
    if local_part.startswith('.') or local_part.endswith('.'):
        return False
    
    # Kiểm tra không có hai dấu chấm liên tiếp
    if '..' in email:
        return False
    
    return True

def find_email(driver,link):
    try:
        driver.get(link)
        print(f"Đang mở trang: {link}")
        time.sleep(3)
        html_content = driver.page_source

        try:
            emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", html_content)
            emails = list(set(emails))
            print("Các email tìm được:", emails)
            filtered_emails = []
            for email in emails:
                if is_valid_email(email):
                    filtered_emails.append(email)
            return filtered_emails
        except Exception as e:
            print(f"Lỗi khi tìm email: {e}")
            return []
    except Exception as e:
        print(f"Lỗi khi mở trang web: {e}")
        return []

def safe_find_text(parent, selector):
    from selenium.common.exceptions import NoSuchElementException
    try:
        return parent.find_element(By.CSS_SELECTOR, selector).text
    except NoSuchElementException:
        return None

def safe_find_element(parent, selector):
    from selenium.common.exceptions import NoSuchElementException
    try:
        return parent.find_element(By.CSS_SELECTOR, selector)
    except NoSuchElementException:
        return None
    
def get_driver():
    # Cấu hình Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Chạy không hiển thị trình duyệt
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-features=TranslateUI")
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-sync")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    
    # Tắt các dịch vụ Google không cần thiết
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Tắt logging để giảm noise
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--silent")
    
    # Khởi tạo WebDriver với nhiều cách khác nhau
    driver = None
    
    # Cách 1: Thử sử dụng webdriver-manager (cần cài đặt: pip install webdriver-manager)
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Sử dụng webdriver-manager thành công")
    except ImportError:
        print("webdriver-manager chưa được cài đặt")
    except Exception as e:
        print(f"Lỗi khi sử dụng webdriver-manager: {e}")
    
    # Cách 2: Thử sử dụng ChromeDriver từ thư mục hiện tại
    if not driver:
        try:
            service = Service(executable_path='chromedriver.exe')
            driver = webdriver.Chrome(service=service, options=chrome_options)
            print("Sử dụng chromedriver.exe từ thư mục hiện tại")
        except Exception as e:
            print(f"Lỗi khi sử dụng chromedriver.exe: {e}")
    
    # Cách 3: Thử sử dụng ChromeDriver từ PATH
    if not driver:
        try:
            driver = webdriver.Chrome(options=chrome_options)
            print("Sử dụng ChromeDriver từ PATH")
        except Exception as e:
            print(f"Lỗi khi sử dụng ChromeDriver từ PATH: {e}")
            print("Vui lòng:")
            print("1. Tải ChromeDriver phù hợp với phiên bản Chrome của bạn từ: https://chromedriver.chromium.org/")
            print("2. Hoặc cài đặt webdriver-manager: pip install webdriver-manager")
            return None
    
    if not driver:
        print("Không thể khởi tạo WebDriver")
        return None
    return driver

def open_website(search_country, search_keyword,url):
    """
    Mở một trang web bằng Selenium với auto-management ChromeDriver
    """
    driver = get_driver()
    if not driver:
        print("Không thể khởi tạo WebDriver")
        return None

    # Kiểm tra xem file crawl_result.csv đã tồn tại chưa, nếu có thì xóa nó
    import os
    csv_file_path = "crawl_result.csv"
    if os.path.exists(csv_file_path):
        try:
            os.remove(csv_file_path)
            print(f"Đã xóa file {csv_file_path} cũ")
        except Exception as e:
            print(f"Lỗi khi xóa file {csv_file_path}: {e}")
    else:
        print(f"File {csv_file_path} chưa tồn tại")

    try:
        # Mở trang web
        print(f"Đang mở trang web: {url}")
        driver.get(url)
        time.sleep(5)  # Chờ một chút để trang web load
        print("done waiting")
        # Đợi trang web load
        # Lấy thông tin trang web
        page_title = driver.title
        current_url = driver.current_url
        search = driver.find_element(By.CSS_SELECTOR, "#APjFqb")
        # xoa he text trong ô tìm kiếm
        search.clear()
        search.send_keys(f"{search_country} {search_keyword}")
        # enter
        search.send_keys(u'\ue007')  # Nhấn Enter
        
        print(f"Tiêu đề trang: {page_title}")
        print(f"URL hiện tại: {current_url}")
        is_page_left = True
        while is_page_left:
            time.sleep(5)

            # Chờ 3 giây để xem trang web
            time.sleep(3)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#rl_ist0 > div > div.rl_tile-group > div.rlfl__tls.rl_tls"))
            )

            lists = driver.find_element(By.CSS_SELECTOR, "#rl_ist0 > div > div.rl_tile-group > div.rlfl__tls.rl_tls")

            if not lists:
                print("Không tìm thấy danh sách nào trên trang web")
                return None
            print(f"Tìm thấy danh sách trên trang web")

            child_divs = driver.find_elements(By.CSS_SELECTOR, "#rl_ist0 > div > div.rl_tile-group > div.rlfl__tls.rl_tls > div")
            if not child_divs:
                print("Không tìm thấy thẻ con nào trong container")
                return None
                
            print(f"Tìm thấy {len(child_divs)} thẻ con trong container")
            cnt = 0
            with open(f"crawl_result.jsonl", "a", encoding="utf-8") as f:
                for index, div in enumerate(child_divs):
                    # kiem tra neu the co class la PiKi2c thi bo qua
                    print("-------------------------------------------------------------------")
                    if "PiKi2c" in div.get_attribute("class"):
                        continue

                    # Chekc if div have any class, if not print text
                    if not div.get_attribute("id"):
                        print(f"Thẻ con {index + 1} k có id: {div.text}")
                        continue
                    
                    # print(f"Thẻ con {index + 1} có id: {div.text}")
                    # print(len(div.find_elements(By.CSS_SELECTOR, " :scope>div")))
                    
                    name = None
                    class_type = None
                    address = None
                    phone = None
                    web_link = None

                    #lay thon tin co ban
                    if (len(div.find_elements(By.CSS_SELECTOR, " :scope>div")) >1 ):
                        info = div.find_element(By.CSS_SELECTOR, "div:nth-child(2) > div > div:nth-child(1) > a > div > div")

                    elif(len(div.find_elements(By.CSS_SELECTOR, ":scope>div")) == 1 ):
                        info = div.find_element(By.CSS_SELECTOR, "div:nth-child(1) > div > div:nth-child(1) > a > div > div")
                    else:
                        print(f"Thẻ con {index + 1} không có thông tin cần thiết")
                        continue

                    # Lay ten
                    name = safe_find_text(info, "div:nth-child(1) > span")

                    # Lay link trang web 
                    temp_list = div.find_elements(By.CSS_SELECTOR, "div:nth-child(2) > div > a")
                    web_link = None
                    if len(temp_list) > 1:
                        web_link = temp_list[0].get_attribute("href") 


                    name_section = safe_find_element(info, "div:nth-child(1) > span")
                    name_section.click()
                    # Chờ để thông tin chi tiết tải xong
                    time.sleep(1)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-attrid="kc:/location/location:address"] > div > div > span:nth-child(2)'))
                    )

                    #lay dia chi va so dien thoai
                    address = safe_find_text(driver, 'div[data-attrid="kc:/location/location:address"] > div > div > span:nth-child(2)')
                    phone = safe_find_text(driver, 'div[data-attrid="kc:/local:alt phone"] > div > div > span:nth-child(2)')


                    email_str = None
                    if web_link is not None:
                        try:
                            get_email_driver = get_driver()
                            emails = find_email(get_email_driver, web_link)
                            if emails:
                                # convert emails to string seperated by comma
                                email_str = ', '.join(emails)
                        except Exception as e:
                            print(f"Lỗi khi tìm email: {e}")
                        finally:
                            if get_email_driver:
                                get_email_driver.quit()

                    print(f"Tên: {name}, Địa chỉ: {address}, Số điện thoại: {phone}, Link: {web_link}, Email : {email_str}")
                    # f.write(f"{name}\t{address}\t{phone}\t{web_link}\t{email_str}\n")
                    data = {
                        "name": name,
                        "address": address,
                        "phone": phone,
                        "web_link": web_link,
                        "email": email_str
                    }
                    f.write(f"{json.dumps(data, ensure_ascii=False)}\n")
                    cnt += 1

                print(f"Tổng số thẻ con không có class PiKi2c: {cnt}")
                input("Nhấn Enter để tiếp tục hoặc Ctrl+C để dừng...")
                
                from selenium.common.exceptions import NoSuchElementException
                try:
                    button = driver.find_element(By.CSS_SELECTOR, "#pnnext > span.oeN89d")
                    button.click()
                except NoSuchElementException:
                    print("Không còn trang tiếp theo")
                    is_page_left = False

                                    
        
        return driver
        
    except Exception as e:
        print(f"Lỗi khi mở trang web: {e}")
        driver.quit()
        return None

def check_chrome_version():
    """
    Kiểm tra phiên bản Chrome đang cài đặt
    """
    import subprocess
    import platform
    
    try:
        if platform.system() == "Windows":
            # Kiểm tra Chrome trên Windows
            result = subprocess.run([
                'reg', 'query', 
                'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', 
                '/v', 'version'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                version = result.stdout.split()[-1]
                print(f"Phiên bản Chrome: {version}")
                return version
            else:
                print("Không thể xác định phiên bản Chrome")
                return None
        else:
            # Kiểm tra Chrome trên Linux/Mac
            result = subprocess.run(['google-chrome', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"Phiên bản Chrome: {version}")
                return version
            else:
                print("Không thể xác định phiên bản Chrome")
                return None
    except Exception as e:
        print(f"Lỗi khi kiểm tra phiên bản Chrome: {e}")
        return None

if __name__ == "__main__":
    # Kiểm tra phiên bản Chrome
    print("=== Kiểm tra phiên bản Chrome ===")
    check_chrome_version()
    
    # Ví dụ 1: Mở trang web đơn giản
    country = input("Nhập tên quốc gia (ví dụ: Việt Nam): ")
    keyword = input("Nhập các từ khóa tìm kiếm: ")

    print("\n=== Mở trang web ===")
    driver = open_website(country, keyword,"https://www.google.com/search?q=English+school+H%E1%BA%A3i+Ph%C3%B2ng&sca_esv=c4d3b1b5b2456fed&hl=vi&biw=1349&bih=985&tbm=lcl&ei=dQN5aMSMAv2h0-kP5oD90AU&ved=0ahUKEwiEm4KoiMSOAxX90DQHHWZAH1oQ4dUDCAo&uact=5&oq=English+school+H%E1%BA%A3i+Ph%C3%B2ng&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhtFbmdsaXNoIHNjaG9vbCBI4bqjaSBQaMOybmdIAFAAWABwAHgAkAEAmAEAoAEAqgEAuAEDyAEAmAIAoAIAmAMAkgcAoAcAsgcAuAcAwgcAyAcA&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[20.8693047,106.72400460000001],[20.814306,106.6360823]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:14")
    time.sleep(1000)  # Chờ để xem trang web
    if driver:
        driver.quit()