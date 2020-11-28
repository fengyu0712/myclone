from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  selenium.webdriver.common.by import By
from Common.conf import Read_conf
from Common.log import Logger
from Conf import Project_path
import sys
import time


# my_accounname=ReadConf(conf_path, "BID", "my_account_name").getvalue()

home_sign_location = "//a[text()='首页']"
myaccount_location="//a[contains(text(),'我的帐户')]"
bid_button_location="//span[text()=' %s']//ancestor::a//following-sibling::div//a[text()='抢投标']"
homequit_location="//a[text()='退出']"
homelogin_location="//a[text()='登录']"
class Home:
    def __init__(self,driver):
        self.driver=driver
    def get_account_name(self):
        try:
            WebDriverWait(self.driver,10,0.5).until(EC.presence_of_element_located((By.XPATH,myaccount_location)))
        except Exception as e:
            raise e
        else:
            account_name=self.driver.find_element_by_xpath(myaccount_location).text
            return account_name

    def into_bid(self,bid_name):
        try:
            WebDriverWait(self.driver,10, 0.2).until(EC.visibility_of_element_located((By.XPATH,bid_button_location%bid_name)))
        except Exception as e:
            raise e
        else:
            self.driver.find_element_by_xpath(bid_button_location%bid_name).click()

    def into_myaccount(self):
        try:
            WebDriverWait(self.driver,10,0.2).until(EC.visibility_of((By.XPATH,myaccount_location)))
        except Exception as e:
            raise e
        else:
            self.driver.find_element_by_xpath(myaccount_location).click()
    def quit_login(self):
        try:
            WebDriverWait(self.driver,10,0.5).until(EC.visibility_of_element_located((By.XPATH, homequit_location)))
            self.driver.find_element_by_xpath(homequit_location).click()
        except Exception as e:
            raise e
        else:
            WebDriverWait(self.driver, 10, 0.2).until(EC.visibility_of_element_located((By.XPATH, homelogin_location)))
            pass






