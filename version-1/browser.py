import helium
from selenium import webdriver


def get_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--force-device-scale-factor=1")
    chrome_options.add_argument("--window-size=1000,1350")
    chrome_options.add_argument("--disable-pdf-viewer")
    chrome_options.add_argument("--window-position=0,0")
    driver = helium.start_chrome(headless=False, options=chrome_options)
    return driver
