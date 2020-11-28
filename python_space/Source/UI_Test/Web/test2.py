from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  selenium.webdriver.common.by import By
from  selenium.webdriver.common.action_chains import ActionChains

url="https://blog.csdn.net/Meinianda2017/article/details/77503867"
more_element="//a[@class='show-more-a']"
a="//a[@class='show-more-a']//following-sibling::div/div/a[text()='招聘']"

browser = webdriver.Chrome()
browser.get(url)
WebDriverWait(browser,30,0.5).until(EC.visibility_of_element_located((By.XPATH,more_element)))
m=browser.find_element_by_xpath(more_element)
m.find_element_by_xpath(a).click()
