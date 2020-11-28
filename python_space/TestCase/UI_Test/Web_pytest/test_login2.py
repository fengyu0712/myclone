from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  selenium.webdriver.common.by import By
from Page_Object.Web.testpage import home_page
from Page_Object.Web.testpage import login_page
from Page_Object.Web.testpage.login_page import Login
from Page_Object.Web.testpage.home_page import Home
from  selenium import  webdriver
import unittest
import sys
import time
from time import sleep
from Common.conf import Read_conf
from Common.log import Logger
from Conf import Project_path
import pytest


conf_path=Project_path.Conf_path+"Web.conf"
url = Read_conf(conf_path).get_value( "BID", "url")
login_account = Read_conf(conf_path).get_value( "BID", "login_account")
pickname=Read_conf(conf_path).get_value( "BID", "my_account_name")
password = Read_conf(conf_path).get_value( "BID", "password")

# verificationErrors=[]
myaccount_location=home_page.myaccount_location
error_noaccount_location=login_page.error_noaccount_location
error_nopassword_location=login_page.error_nopassword_location
error_wrongpassword_location=login_page.error_wrongpassword_location
error_wrongaccount_location=login_page.error_wrongaccount_location
error_wrongphone_location=login_page.error_wrongaccount_location
homelogin_location=home_page.homelogin_location


@pytest.mark.usefixture("Web_driver_class")
@pytest.mark.usefixtures("Web_driver")
class LoginTest:
    @pytest.mark.smoke
    def test_login_ok(self,Web_driver_class):
        Logger().info("测试用例：正常登录")
        Login(Web_driver_class).login(login_account, password)
        try:
            self.assertIn(pickname,Home(Web_driver_class).get_account_name())
        except Exception as e:
            Web_driver_class.save_screenshot(Project_path.Image_path+"%s_%s.png"%(sys._getframe().f_code.co_name,self.nowtime))
            Logger().error("%s test fail:%s" % (sys._getframe().f_code.co_name,e))
            Web_driver_class.execute_script('window.stop()')
        else:
            Logger().info("%s test pass" % sys._getframe().f_code.co_name)
        finally:
            Home(Web_driver_class).quit_login()
    # def test_login_wrongphone(self):
    #     Logger().info("测试用例：异常用例-手机号错误")
    #     Login(Web_driver_class).login("13017659465", "123456")
    #     try:
    #         WebDriverWait(Web_driver_class, 5, 0.2).until(
    #                         EC.visibility_of_element_located((By.XPATH, error_wrongphone_location)))
    #         self.assertIsNotNone(Web_driver_class.find_element_by_xpath(error_wrongphone_location),"没有提示手机号错误,fail")
    #     except Exception as e:
    #         Web_driver_class.save_screenshot(Project_path.Image_path+"%s_%s.png"%(sys._getframe().f_code.co_name,self.nowtime))
    #         raise e
    #     else:
    #         Logger().info("%s test pass" % sys._getframe().f_code.co_name)
    #
    # def test_login_nopassword(self):
    #     Logger().info("测试用例：异常用例-密码为空")
    #     Login(Web_driver_class).login( login_account, "")
    #     WebDriverWait(Web_driver_class, 5, 0.2).until(
    #         EC.visibility_of_element_located((By.XPATH, error_nopassword_location)))
    #     try:
    #         self.assertIsNotNone(Web_driver_class.find_element_by_xpath(error_nopassword_location), "没有提示密码为空,fail")
    #     except Exception as e:
    #         Web_driver_class.save_screenshot(
    #             Project_path.Image_path + "%s_%s.png" % (sys._getframe().f_code.co_name, self.nowtime))
    #         raise e
    #     else:
    #         Logger().info("%s test pass" % sys._getframe().f_code.co_name)
    # def test_login_noaccount(self):
    #     Logger().info("测试用例：异常用例-账户为空")
    #     Login(Web_driver_class).login( " ", password)
    #     try:
    #         WebDriverWait(Web_driver_class, 5, 0.2).until(
    #             EC.visibility_of_element_located((By.XPATH, error_noaccount_location)))
    #         self.assertIsNotNone(Web_driver_class.find_element_by_xpath(error_noaccount_location),"没有提示账户为空,fail")
    #     except Exception as e:
    #         Web_driver_class.save_screenshot(
    #             Project_path.Image_path + "%s_%s.png" % (sys._getframe().f_code.co_name, self.nowtime))
    #         raise e
    #     else:
    #         Logger().info("%s test pass" % sys._getframe().f_code.co_name)
    # def test_login_wrong_password(self):
    #     Logger().info("测试用例：异常用例-密码错误")
    #     Login(Web_driver_class).login( login_account, "11111111")
    #     try:
    #         WebDriverWait(Web_driver_class, 5, 0.2).until(
    #             EC.visibility_of_element_located((By.XPATH, error_wrongpassword_location)))
    #         self.assertIsNotNone(Web_driver_class.find_element_by_xpath(error_wrongpassword_location),"没有提示密码错误,fail")
    #     except Exception as e:
    #         Web_driver_class.save_screenshot(
    #             Project_path.Image_path + "%s_%s.png" % (sys._getframe().f_code.co_name, self.nowtime))
    #         raise e
    #     else:
    #         Logger().info("%s test pass" % sys._getframe().f_code.co_name)
    # def test_login_wrong_account(self):
    #     Logger().info("测试用例：异常用例-账户错误")
    #     Login(Web_driver_class).login( "13017659465", password)
    #     try:
    #         WebDriverWait(Web_driver_class, 5, 0.2).until(EC.visibility_of_element_located((By.XPATH, error_wrongaccount_location)))
    #         self.assertIsNotNone(Web_driver_class.find_element_by_xpath(error_wrongaccount_location),"没有提示账户错误,fail")
    #     except Exception as e:
    #
    #         Web_driver_class.save_screenshot(Project_path.Image_path + "%s_%s.png" % (sys._getframe().f_code.co_name, self.nowtime))
    #         raise e
    #     else:
    #         Logger().info("%s test pass" % sys._getframe().f_code.co_name)

if __name__ == '__main__':
    pytest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(LoginTest)
    # unittest.TextTestRunner(verbosity=1).run(suite)