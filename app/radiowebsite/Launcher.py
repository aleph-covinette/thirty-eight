from selenium import webdriver
from selenium.webdriver.common.keys import Keys
def init():
    driver = webdriver.Firefox("C:\Program Files (x86)\Mozilla Maintenance Service")
    driver.get('http://127.0.0.1:8000/')
init()