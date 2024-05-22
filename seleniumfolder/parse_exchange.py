from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time, os, json
from PIL import Image
from bs4 import BeautifulSoup
with open('./cookies.json', 'r') as f:
    cookies = json.load(f)
options = Options()
options.add_argument("--disable-images")
options.add_argument("--disable-webgl")
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
    info1 = soup.select_one('html > body > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(3) > div > div > div:nth-of-type(3) > div:nth-of-type(3) > div:nth-of-type(1)')
    info2 = soup.select_one('html > body > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(3) > div > div > div:nth-of-type(3) > div:nth-of-type(1) > div:nth-of-type(1)')
    data1 = info1.text
    data2 = info2.text
    return (f"{data1}\n"
        f"{data2}\n")


def resize_image():
    img = Image.open("exchange.png")
    width, height = img.size
    new_height = height
    img = img.crop((97, 185, 815, new_height - 75)) 
    img.save("exchangeoutput.png")