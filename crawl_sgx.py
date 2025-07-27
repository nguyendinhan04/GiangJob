from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import datetime
import re



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
    

def open_website(url):
    """
    Mở một trang web bằng Selenium với auto-management ChromeDriver
    """
    driver = get_driver()
    if not driver:
        print("Không thể khởi tạo WebDriver")
        return None

    try:
        # Mở trang web
        print(f"Đang mở trang web: {url}")
        driver.get(url)
        time.sleep(5)  # Chờ một chút để trang web load
        print("done waiting")
        
                                    
        
        return driver
        
    except Exception as e:
        print(f"Lỗi khi mở trang web: {e}")
        driver.quit()
        return None
    

if __name__ == "__main__":
    # Kiểm tra phiên bản Chrome
    print("=== Kiểm tra phiên bản Chrome ===")
    check_chrome_version()

    print("\n=== Mở trang web ===")
    driver = open_website("https://www.sgx.com/research-education/derivatives")
    time.sleep(1000)  # Chờ để xem trang web
    if driver:
        driver.quit()