import json
import time
import os
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--disable-images")
options.add_argument("--disable-webgl")
options.add_argument("--enable-javascript")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--enable-chrome-browser-cloud-management")
with open('./cookies.json', 'r') as f:
    cookies = json.load(f)
def get_source(url):
    print(f"Сделан запрос profile на никнейм {url}")
    driver = webdriver.Chrome(options=options)
    driver.get('https://excalibur-craft.ru/index.php?do=profile&name=' + url)
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(4)
    driver.save_screenshot('screenshotPROFILE.png')
    source_code = driver.page_source
    soup = BeautifulSoup(source_code, 'html.parser')
    exp = soup.select_one('html > body > div:nth-of-type(2) > div:nth-of-type(1) > div > div:nth-of-type(1) > div > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(5) > div:nth-of-type(2) > p')
    clan = soup.select_one('html > body > div:nth-of-type(2) > div:nth-of-type(1) > div > div:nth-of-type(1) > div > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(6) > div > label > a')
    status = soup.select_one('html > body > div:nth-of-type(2) > div:nth-of-type(1) > div > div:nth-of-type(1) > div > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(4) > div:nth-of-type(2) > p')
    online_on_month = soup.select_one('html > body > div:nth-of-type(2) > div:nth-of-type(1) > div > div:nth-of-type(1) > div > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > p')
    online_on_all = soup.select_one('html > body > div:nth-of-type(2) > div:nth-of-type(1) > div > div:nth-of-type(1) > div > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(3) > div:nth-of-type(2) > p')
    registration_date = soup.select_one('html > body > div:nth-of-type(2) > div:nth-of-type(1) > div > div:nth-of-type(1) > div > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(2) > p')

    if exp and status and online_on_month and online_on_all and registration_date:
        resize_image()
        time.sleep(2)
        if clan:
            return (f"Опыт: {exp.text}\n"
                f"Клан: {clan.text}\n"
                f"Статус в игре: {status.text}\n"
                f"Онлайн за месяц: {online_on_month.text}\n"
                f"Онлайн за все время: {online_on_all.text}\n"
                f"Дата регистрации: {registration_date.text}\n")
        else:
            return (f"Опыт: {exp.text}\n"
                f"Статус в игре: {status.text}\n"
                f"Онлайн за месяц: {online_on_month.text}\n"
                f"Онлайн за все время: {online_on_all.text}\n"
                f"Дата регистрации: {registration_date.text}\n")
    else:
        return 1337

def resize_image():
    img = Image.open("screenshotPROFILE.png")
    img = img.crop((80, 150, 730, 435))
    img.save("outputPROFILE.png")
    os.remove("screenshotPROFILE.png")
