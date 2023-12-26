import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def convert_to_numeric(value):
    value = value.replace(',', '')  # Remove commas from the value
    if 'K' in value:
        return float(value.replace('K', '')) * 1000
    elif 'M' in value:
        return float(value.replace('M', '')) * 1000000
    elif 'B' in value:
        return float(value.replace('B', '')) * 1000000000
    else:
        return float(value)

def scrape_data():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(service=Service(), options=chrome_options)

    url = "https://www.warriortrading.com/day-trading-watch-list-top-stocks-to-watch/"
    driver.get(url)

    time.sleep(5)

    button_xpath = "//div[@aria-label='marketing and promotions']/div/div[2]"
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, button_xpath))
    )
    button.click()

    time.sleep(5)

    rows = driver.find_elements(By.XPATH, "//div[@class='overflow-x-auto']/div[2]")

    data = []
    for row in rows:
        # Extracting data from each set of 9 divs
        for i in range(10, 902, 9):
            symbol = row.find_element(By.XPATH, f".//div[{i}]/a").text.strip()
            gap_percent = row.find_element(By.XPATH, f".//div[{i+1}]").text.strip()
            price = convert_to_numeric(row.find_element(By.XPATH, f".//div[{i+2}]").text.strip())
            volume = convert_to_numeric(row.find_element(By.XPATH, f".//div[{i+3}]").text.strip())
            relative_volume_daily = convert_to_numeric(row.find_element(By.XPATH, f".//div[{i+4}]").text.strip())
            relative_volume_5min = convert_to_numeric(row.find_element(By.XPATH, f".//div[{i+5}]").text.strip())
            change_from_close = convert_to_numeric(row.find_element(By.XPATH, f".//div[{i+6}]").text.strip())
            stock_float = convert_to_numeric(row.find_element(By.XPATH, f".//div[{i+7}]").text.strip())
            short_interest = convert_to_numeric(row.find_element(By.XPATH, f".//div[{i+8}]").text.strip())
            
            data.append([
                symbol, gap_percent, price, volume,
                relative_volume_daily, relative_volume_5min,
                change_from_close, stock_float, short_interest
            ])

    date_today = datetime.now().strftime("%Y%m%d")
    df = pd.DataFrame(data, columns=[
        "Symbol", "Gap(%)", "Price", "Volume",
        "Relative Volume(Daily Rate)", "Relative Volume(5 min %)",
        "Change From Close(%)", "Float", "Short Interest"
    ])
    output_directory = r"./"  # Replace with your desired output directory
    csv_filename = f"{output_directory}\\{date_today}_watchlist.csv"
    df.to_csv(csv_filename, index=False)

    print(f"Data has been extracted and saved to {csv_filename}")

    driver.quit()

scrape_data()
