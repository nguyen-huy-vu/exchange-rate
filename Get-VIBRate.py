from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json

def main():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://www.vib.com.vn/en/ty-gia/bang-ty-gia")
    time.sleep(3)  # wait to ensure page loads
    euro_element = driver.find_element(By.XPATH, '//*[@id="dataListTable"]/div[7]')
    euro_html = euro_element.get_attribute("outerHTML")

    driver.quit()

    soup = BeautifulSoup(euro_html, "html.parser")
    root = soup.find("div", class_="vib-v2-line-box-table-deposit")

    code = root.find("span", class_="text").get_text(strip=True)
    name = root.find("span", class_="name").get_text(strip=True)

    cols = root.find_all("div", class_="vib-v2-colum-table-deposit")
    values = [c.get_text(strip=True) for c in cols]

    print(code)      # "EUR"
    print(name)      # "Euro"
    print(f"Buy cash: {values[0]}")
    print(f"Buy transfer: {values[1]}")
    print(f"Sell cash: {values[2]}")
    print(f"Sell transfer: {values[3]}")

    result = {
        "Currency": name,
        "Code": code,
        "Buy cash": values[0],
        "Buy transfer": values[1],
        "Sell cash": values[2],
        "Sell transfer": values[3]
    }
    
    with open("result.json", "w") as f:
        json.dump(result, f)
    print("Saved:", result)


if __name__ == "__main__":
    main()