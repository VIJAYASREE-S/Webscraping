from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--headless")  # Uncomment to run without GUI

# Automatically download and use the correct version of ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    url = "https://www.zeptonow.com/brand/Lay's/18d6cb72-65aa-4881-8984-a08aa295dd35?spvid=351db1e6-d693-4a28-88a8-2d59e864f67a"
    driver.get(url)

    time.sleep(5)  # Wait for page to load

    print("Page Title:", driver.title)
    if "Lay's" in driver.title:
        print("✅ Page loaded successfully.")
    else:
        print("⚠️ Page title unexpected.")

except Exception as e:
    print("❌ Error occurred:", str(e))

finally:
    driver.quit()
