from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  selenium.webdriver.common.by import By
from  selenium.webdriver.common.action_chains import ActionChains

srk_element="//input[@id='kw']"
ss_element="//input[@id='su']"
url='http://www.baidu.com/'
jj_element="//a[contains(@ourl,'jeagine.com')]"
set_element="//a[text()='百度首页']//following-sibling::a[text()='设置']"
search_set="//a[text()='搜索设置']"


browser = webdriver.Chrome()
browser.get(url)
search=browser.current_window_handle
print(search)
WebDriverWait(browser,10,0.5).until(EC.visibility_of_element_located((By.XPATH,srk_element)))
browser.find_element_by_xpath(srk_element).send_keys("寄锦教育")
browser.find_element_by_xpath(ss_element).click()
WebDriverWait(browser,30,0.5).until(EC.visibility_of_element_located((By.XPATH,jj_element)))
browser.find_element_by_xpath(jj_element).click()
#获得当前打开所有窗口句柄
all_handles = browser.window_handles
for handle in all_handles:
    if handle ==search:
        browser.switch_to_window(handle)
        print ('now search window')
    elif handle !=search:
        browser.switch_to_window(handle)
        print('now  no search window')
#切换到搜索框
browser.switch_to_window(search)

#鼠标模拟点击下拉框
ActionChains(browser).move_to_element(browser.find_element_by_xpath(set_element)).perform()
browser.find_element_by_xpath(search_set).click()
# browser.quit()




