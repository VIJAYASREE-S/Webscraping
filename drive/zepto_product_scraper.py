from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")

# Setup Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open the Zepto Lay's brand page
url = "https://www.zeptonow.com/brand/Lay's/18d6cb72-65aa-4881-8984-a08aa295dd35?spvid=351db1e6-d693-4a28-88a8-2d59e864f67a"
driver.get(url)

time.sleep(5)  # Let page load

# Scroll to bottom to trigger lazy loading
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Collect product names
products = []
product_xpath = "//h5[@data-testid='product-card-name']"
product_elements = driver.find_elements(By.XPATH, product_xpath)

print(f"🟢 Found {len(product_elements)} product names.")

# Refetch inside loop to avoid stale element errors
for i in range(len(product_elements)):
    try:
        name = driver.find_elements(By.XPATH, product_xpath)[i].text.strip()
        products.append({
            "Product Name": name,
            "Position on Page": i + 1
        })
    except Exception as e:
        print(f"❌ Error reading product {i+1}: {e}")

driver.quit()

# Save to Excel
df = pd.DataFrame(products)
print(df.head())  # Optional: see first few entries
df.to_excel("zepto_products.xlsx", index=False, engine="openpyxl")
print("✅ Data saved to zepto_products.xlsx")
