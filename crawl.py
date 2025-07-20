from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

def open_website(url):
    """
    Mở một trang web bằng Selenium
    """
    # Cấu hình Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Chạy không hiển thị trình duyệt
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Khởi tạo WebDriver
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Mở trang web
        print(f"Đang mở trang web: {url}")
        driver.get(url)
        
        # Đợi trang web load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Lấy thông tin trang web
        page_title = driver.title
        current_url = driver.current_url
        
        print(f"Tiêu đề trang: {page_title}")
        print(f"URL hiện tại: {current_url}")
        
        # Chờ 3 giây để xem trang web
        time.sleep(3)
        
        return driver
        
    except Exception as e:
        print(f"Lỗi khi mở trang web: {e}")
        driver.quit()
        return None

def crawl_example():
    """
    Ví dụ crawl dữ liệu từ một trang web
    """
    url = "https://www.google.com"
    
    driver = open_website(url)
    
    if driver:
        try:
            # Tìm ô tìm kiếm
            search_box = driver.find_element(By.NAME, "q")
            search_box.send_keys("selenium python")
            search_box.submit()
            
            # Đợi kết quả tải
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "search"))
            )
            
            print("Đã thực hiện tìm kiếm thành công!")
            
            # Đợi 3 giây để xem kết quả
            time.sleep(3)
            
        except Exception as e:
            print(f"Lỗi khi crawl dữ liệu: {e}")
        
        finally:
            # Đóng browser
            driver.quit()
            print("Đã đóng browser")

if __name__ == "__main__":
    # Ví dụ 1: Mở trang web đơn giản
    print("=== Ví dụ 1: Mở trang web ===")
    driver = open_website("https://www.python.org")
    time.sleep(1000)  # Chờ để xem trang web
    if driver:
        driver.quit()
    
    # print("\n=== Ví dụ 2: Crawl dữ liệu từ Google ===")
    # crawl_example()
