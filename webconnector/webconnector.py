import os
# pip3 install selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class WebConnector():
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--window-size=1024x768")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('–-lang=zh-TW')
        chrome_driver = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver")

        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)