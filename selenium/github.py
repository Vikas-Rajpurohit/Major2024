from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

s = Service("C:/Users/agarw/Desktop/chromedriver-win64/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=s)
driver.get('https://github.com/unprricedlace/CV_1-Motion-Detection-Alarm-System')
repo_name_element = driver.find_element(by=By.XPATH, value='//strong[@itemprop="name"]/a')

# Extract the text content of the element
repo_name = repo_name_element.text

print("Repository Name:", repo_name)
readme_section = driver.find_element(by=By.XPATH,value='//*[contains(concat( " ", @class, " " ), concat( " ", "container-lg", " " ))]')
# Extract the text content of the README
readme_content = readme_section.text

# Print the README content
print("README Content:")
print(readme_content)

elements = driver.find_element(by=By.XPATH, value='//*[contains(concat( " ", @class, " " ), concat( " ", "iXWA-dl", " " ))]')

print("Element with class 'iXWA-dl':", elements.text)

# html = driver.page_source
# with open('smartprix.html','w',encoding='utf-8') as f:
#   f.write(html)