from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time, os, json
import re
from PIL import Image
from bs4 import BeautifulSoup, re
with open('./cookies.json', 'r') as f:
    cookies = json.load(f)
options = Options()
options.add_argument("--disable-images")
options.add_argument("--disable-webgl")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--enable-javascript")
options.add_argument("--enable-chrome-browser-cloud-management")
def get_exchange():
    driver = webdriver.Chrome(options=options)
    driver.get("https://excalibur-craft.ru/index.php?do=clans&go=exchange")
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    driver.execute_script("document.body.style.zoom='58%'")
    time.sleep(4)
    driver.save_screenshot('exchange.png')
    resize_image()
    source_code = driver.page_source
    driver.quit()
    soup = BeautifulSoup(source_code, 'html.parser')
    buy = [tag.parent.text for tag in soup.find_all(string=re.compile("запросов на покупку"))]
    sell = [tag.parent.text for tag in soup.find_all(string=re.compile("предложений на продажу"))]
    sell_complete = ''.join([char for char in sell if char not in " "])
    buy_complete = ''.join([char for char in buy if char not in " "])
    return (f"{buy_complete}\n"
        f"{sell_complete}\n")      


def resize_image():
    img = Image.open("exchange.png")
    width, height = img.size
    new_height = height
    img = img.crop((97, 185, 815, new_height - 75)) 
    img.save("exchangeoutput.png")