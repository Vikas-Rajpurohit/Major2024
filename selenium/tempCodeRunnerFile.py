from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

s=service("C:/Users/agarw/Desktop/chromedriver-win64/chromedriver-win64/chromedriver.exe")

driver=webdriver.Chrome(service=s)

driver.get('https://www.smartprix.com/mobiles')