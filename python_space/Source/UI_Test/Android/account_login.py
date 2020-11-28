import unittest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  selenium.webdriver.common.by import By
from appium import webdriver
from Conf import Project_path
from Common.conf import Read_conf
from Common.log import Logger
from Page_Object.Android.LoginPage import Login
from Page_Object.Android import LoginPage
from Page_Object.Android import Public
from Page_Object.Android import MinePage
from  Page_Object.Android.AccountSetPage import Accoune_set
from Page_Object.Android import AccountSetPage
import time,sys

appium_path=Project_path.Conf_path+"appium.conf"
desired_caps=Read_conf(appium_path).get_value("Android","desired_caps")
appium_url=Read_conf(appium_path).get_value("Android","appium_url")

#元素定位
mine_location=Public.mine_location
mine_login_location=MinePage.mine_login_location
mine_username_location=MinePage.mine_username_location
account='13017659465'
password='123456'

class AccountLoginTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        nowtime = time.strftime("%Y%m%d%H%M")
        Log = Logger()
        driver = webdriver.Remote(appium_url, desired_caps)
        Logger().info("%s测试开始:" % __class__.__name__)
        cls.nowtime=nowtime
        cls.Log=Log
        cls.driver=driver

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.Log.info("%s测试结束!" % __class__.__name__)

    def test_account_login(self):
        self.Log.info("账户密码登录")
        # 进入我的
        WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located((By.ID, mine_location)))
        self.driver.find_element_by_id(mine_location).click()
        # 进入登录页
        WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located((By.ID, mine_login_location)))
        self.driver.find_element_by_id(mine_login_location).click()
        #登录账户密码
        Logion(self.driver).account_login(account,password)
        #验证登录
        try:
            # 等待显示账户名截图
            WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located((By.ID, mine_username_location)))
            self.Log.debug("登录成功")
        except Exception as e:
            self.driver.save_screenshot(Project_path.Image_path+"%s_%s.png"%(sys._getframe().f_code.co_name,self.nowtime))
            self.Log.error("%s test faile" % sys._getframe().f_code.co_name)
        else:
            self.Log.info("%s test pass" % sys._getframe().f_code.co_name)
            #退出登录
            self.driver.find_element_by_id(mine_username_location).click()
            Accoune_set(self.driver).quit_account()
            self.Log.debug("退出登录")


if __name__=="__main__":
    unittest.main()