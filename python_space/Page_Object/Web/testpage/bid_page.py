from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  selenium.webdriver.common.by import By
from Common.log import Logger
from Conf import Project_path
import time
import sys


money_box_location="//input[@class='form-control invest-unit-investinput']"
bid_buton_location="//button[text()='投标']"
bid_successlog_location="//div[@id='layui-layer1']//div[@class='capital_font1 note']"
close_popup_location="//div[@id='layui-layer1']//div[@class='close_pop']/img"
class Bid:
    def __init__(self,driver):
        self.driver=driver
    def get_amount(self):
        WebDriverWait(self.driver, 10, 0.2).until(EC.visibility_of_element_located((By.XPATH,money_box_location)))
        my_amount=self.driver.find_element_by_xpath(money_box_location).get_attribute("data-amount")
        return my_amount

    def bid(self,bid_money):
        WebDriverWait(self.driver, 10, 0.2).until(EC.visibility_of_element_located((By.XPATH,money_box_location)))
        self.driver.find_element_by_xpath(money_box_location).send_keys(bid_money)
        self.driver.find_element_by_xpath(bid_buton_location).click()
        ymd_time=time.strftime('%Y-%m-%d')
        hm_time=time.strftime("%H:%M")
        return [ymd_time,hm_time]

    def bid_result(self):
        try:
            WebDriverWait(self.driver, 10, 0.2).until(EC.visibility_of_element_located((By.XPATH,bid_successlog_location)))
            self.driver.find_element_by_xpath(bid_successlog_location)#能找到投资成功的坐标就算成功
        except Exception as e:
            nowtime=time.strftime("%Y%m%d%H%M")
            self.driver.save_screenshot(Project_path.Image_path+"%s_%s.png"%(sys._getframe().f_code.co_name,nowtime))
            Logger(sys._getframe().f_code.co_name).error("投标异常:%s" %e)
        else:
            Logger().info("投标成功")
    def close_popup(self):
        self.driver.find_element_by_xpath(close_popup_location).click()




