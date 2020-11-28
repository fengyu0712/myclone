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
from Common.conf import Read_conf
from Common.log import Logger
from Conf import Project_path


conf_path=Project_path.Conf_path+"Web.conf"
url = Read_conf(conf_path).get_value( "BID", "url")
login_account = Read_conf(conf_path).get_value( "BID", "login_account")
pickname=Read_conf(conf_path).get_value( "BID", "my_account_name")
password = Read_conf(conf_path).get_value( "BID", "password")

verificationErrors=[]
myaccount_location=home_page.myaccount_location
error_noaccount_location=login_page.error_noaccount_location
error_nopassword_location=login_page.error_nopassword_location
error_wrongpassword_location=login_page.error_wrongpassword_location
error_wrongaccount_location=login_page.error_wrongaccount_location
error_wrongphone_location=login_page.error_wrongphone_location
class LoginTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        self.nowtime = time.strftime("%Y%m%d%H%M")
        Logger().info("测试开始了！")
    def test_login_ok(self):
        Logger().info("测试用例：正常登录")
        try:
            Login(self.driver).login(url,login_account,password)
            self.assertIn(pickname,Home(self.driver).get_account_name())
            self.driver.close()
        except Exception as e:
            verificationErrors.append(e)
            self.driver.save_screenshot(Project_path.Image_path+"%s_%s.png"%(sys._getframe().f_code.co_name,self.nowtime))
            Logger().error("%s test fail:%s" % (sys._getframe().f_code.co_name,e))
        else:
            Logger().info("%s test pass" % sys._getframe().f_code.co_name)

    def test_login_wrongphone(self):
        Logger().info("测试用例：异常用例-手机号错误")
        try:
            Login(self.driver).login(url,"22222222222", "123456")
            WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located((By.XPATH, error_wrongphone_location)))
            self.driver.close()
            Logger().error("%s test pass" % sys._getframe().f_code.co_name)
        except Exception as e:
            verificationErrors.append(e)
            self.driver.save_screenshot(Project_path.Image_path+"%s_%s.png"%(sys._getframe().f_code.co_name,self.nowtime))
            Logger().info("%s test fail" % sys._getframe().f_code.co_name)


    def test_login_nopassword(self):
        Logger().info("测试用例：异常用例-密码为空")
        try:
            Login(self.driver).login(url, login_account, "")
            WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located((By.XPATH, error_nopassword_location)))
            self.driver.close()
            Logger().error("%s test pass" % sys._getframe().f_code.co_name)
        except Exception as e:
            verificationErrors.append(e)
            self.driver.save_screenshot(Project_path.Image_path+"%s_%s.png"%(sys._getframe().f_code.co_name,self.nowtime))
            Logger().info("%s test fail" % sys._getframe().f_code.co_name)
    def test_login_noaccount(self):
        Logger().info("测试用例：异常用例-账户为空")
        try:
            Login(self.driver).login(url, "", password)
            WebDriverWait(self.driver, 10, 0.5).until(
                EC.visibility_of_element_located((By.XPATH, error_noaccount_location)))
            self.driver.close()
            Logger().error("%s test pass" % sys._getframe().f_code.co_name)
        except Exception as e:
            verificationErrors.append(e)
            self.driver.save_screenshot(Project_path.Image_path+"%s_%s.png"%(sys._getframe().f_code.co_name,self.nowtime))
            Logger().info("%s test fail" % sys._getframe().f_code.co_name)

    def test_login_wrong_password(self):
        Logger().info("测试用例：异常用例-密码错误")
        try:
            Login(self.driver).login(url, login_account, "11111111")
            WebDriverWait(self.driver, 10, 0.5).until(
                EC.visibility_of_element_located((By.XPATH, error_wrongpassword_location)))
            self.driver.close()
            Logger().error("%s test pass" % sys._getframe().f_code.co_name)

        except Exception as e:
            verificationErrors.append(e)
            self.driver.save_screenshot(Project_path.Image_path+"%s_%s.png"%(sys._getframe().f_code.co_name,self.nowtime))
            Logger().info("%s test fail" % sys._getframe().f_code.co_name)
    def test_login_wrong_account(self):
        Logger().info("测试用例：异常用例-账户错误")
        try:
            Login(self.driver).login(url, "13017659465", password)
            WebDriverWait(self.driver, 10, 0.5).until(
                EC.visibility_of_element_located((By.XPATH, error_wrongaccount_location)))
            self.driver.close()
            Logger().error("%s test pass" % sys._getframe().f_code.co_name)
        except Exception as e:
            verificationErrors.append(e)
            self.driver.save_screenshot(Project_path.Image_path+"%s_%s.png"%(sys._getframe().f_code.co_name,self.nowtime))
            Logger().info("%s test fail" % sys._getframe().f_code.co_name)

    def tearDown(self):
        self.driver.quit()
        Logger().info("测试结束了!")




if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(LoginTest)
    unittest.TextTestRunner(verbosity=1).run(suite)