from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# Path to ChromeDriver
chromedriver_path = r"C:\chromedriver\chromedriver.exe"

# Path to Brave browser executable
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application/brave.exe"

options = Options()
options.binary_location = brave_path
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--headless")

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

# open lukkari
driver.get("https://www.vib.com.vn/en/ty-gia/bang-ty-gia")
time.sleep(3)  # wait to ensure page loads
driver.save_screenshot("headless-debug.png")
euro_element = driver.find_element(By.XPATH, '//*[@id="dataListTable"]/div[7]')
euro_html = euro_element.get_attribute("outerHTML")

soup = BeautifulSoup(euro_html, "html.parser")
root = soup.find("div", class_="vib-v2-line-box-table-deposit")

# EUR / Euro text
code = root.find("span", class_="text").get_text(strip=True)
name = root.find("span", class_="name").get_text(strip=True)

# All the numbers in the right columns
cols = root.find_all("div", class_="vib-v2-colum-table-deposit")
values = [c.get_text(strip=True) for c in cols]

print(code)      # "EUR"
print(name)      # "Euro"
# print(values)    # ['29.890,00', '29.990,00', '31.030,00', '30.930,00']
print(f"Buy cash: {values[0]}")
print(f"Buy transfer: {values[1]}")
print(f"Sell cash: {values[2]}")
print(f"Sell transfer: {values[3]}")

driver.quit()