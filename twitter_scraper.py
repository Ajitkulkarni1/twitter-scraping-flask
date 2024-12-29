from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pymongo
import uuid
import random
import time


proxy_ip = f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"
# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["twitter_trends"]
collection = db["trends"]


class TwitterTrendsScraper:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--no-sandbox')
        options.add_argument("--headless")
        options.add_argument('--disable-dev-shm-usage')
        return webdriver.Chrome(options=options)


    def scrape_trends(self):
        driver = self.setup_driver()
        try:
            driver.get("https://x.com/login")
            time.sleep(2)

            # Log in
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@autocomplete='username']"))
            )
            username_field.send_keys(self.username)
            username_field.send_keys(Keys.RETURN)
            time.sleep(2)

            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@autocomplete='current-password']"))
            )
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.RETURN)
            time.sleep(3)

            
            driver.get("https://x.com/explore/tabs/trending")  # Trending URL
            time.sleep(3)  # Allow time for the page to load

            # Wait for the trends to load based on class 'r-18u37iz' for trend text
            trends_xpath = "//span[contains(@class, 'r-18u37iz')]"
            trends = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, trends_xpath))
            )

            # Extract text of the first 5 trends
            trend_texts = [trend.text for trend in trends[:5]]

# r-18u37iz




            # Insert to MongoDB
            while len(trend_texts) < 5:
                trend_texts.append("Trend not found")

            record = {
                "_id": str(uuid.uuid4()),
                "nameoftrend1": trend_texts[0],
                "nameoftrend2": trend_texts[1],
                "nameoftrend3": trend_texts[2],
                "nameoftrend4": trend_texts[3],
                "nameoftrend5": trend_texts[4],
                "datetime": datetime.now(),
                "IP address":proxy_ip
            }
            collection.insert_one(record)
            return record
        finally:
            driver.quit()