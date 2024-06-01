from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time, os
from PIL import Image
options = Options()
options.add_argument("--disable-images")
options.add_argument("--disable-webgl")
options.add_argument("--enable-javascript")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--enable-chrome-browser-cloud-management")
def get_screenshot():
    driver = webdriver.Chrome(options=options)
    driver.get("https://excalibur-craft.ru/")
    time.sleep(2)
    driver.execute_script("window.scrollBy(0, 600)")
    current_size = driver.get_window_size()
    new_width = current_size['width'] + 250
    new_height = current_size['height']
    driver.set_window_size(new_width, new_height)
    time.sleep(2)
    driver.save_screenshot('screenshot.png')
    driver.quit()
def crop_screenshot():
    get_screenshot()
    image = Image.open('screenshot.png')
    cropped_image = image.crop((0, 125, 950 + 200, 670))
    cropped_image.save('output.png')
    os.remove("screenshot.png")
