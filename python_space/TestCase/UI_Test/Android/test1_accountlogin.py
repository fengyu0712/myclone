import unittest,allure
from appium import webdriver
from Conf import Project_path
from Common.conf import Read_conf
from Common.log import Logger
from Page_Object.Android.LoginPage import Login
from Page_Object.Android.Public import  Main
from Page_Object.Android import QuestionPage
from Page_Object.Android import MinePage
from Page_Object.Android.MinePage import Mine
import time,sys

appium_path=Project_path.Conf_path+"appium.conf"
mode_path=Project_path.Conf_path+"app_TestMode.conf"
desired_caps=Read_conf(appium_path).get_value("Android","desired_caps")
appium_url=Read_conf(appium_path).get_value("Android","appium_url")
mode=Read_conf(mode_path).get_value("Mode","mode")

#元素定位
mine_username_location=MinePage.mine_username_location
see_answer=QuestionPage.see_answer_location

@allure.feature("APP登录功能测试")
class LoginTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Log = Logger()
        Log.info("========%s测试开始:========" % __class__.__name__)
        nowtime = time.strftime("%Y%m%d%H%M")
        driver = webdriver.Remote(appium_url, desired_caps)
        cls.nowtime=nowtime
        cls.Log=Log
        cls.driver=driver
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.Log.info("========%s测试结束!========" % __class__.__name__)
        cls.Log.close()

    def setUp(self):
        Main(self.driver).close_ad()
        Main(self.driver).close_update()
        Mine(self.driver).stay_unlocation()
        # 判断是否有弹窗,并关闭
    def tearDown(self):
        pass

    @allure.story("正常登录测试")
    def test_account_login_ok(self):
        Login(self.driver).account_login()
        try:     #验证登录
            Mine(self.driver).get_accountname()
        except Exception as e:
            self.driver.save_screenshot(Project_path.Image_path+"%s_%s.png"%(sys._getframe().f_code.co_name,self.nowtime))
            raise e
        else:
            self.Log.debug("登录成功")
            self.Log.info("%s test pass" % sys._getframe().f_code.co_name)

    @allure.story("密码错误登录测试")
    def test_account_login_wrongword(self):
        Login(self.driver).account_login(password="654321")
        try:     #验证登录
            warning="用户名或密码错误"
            self.assertEqual(warning,Login(self.driver).warn())
            # self.assertIsNone(True,self.driver.find_element_by_id(mine_username_location),)
        except Exception as e:
            self.driver.save_screenshot(Project_path.Image_path+"%s_%s.png"%(sys._getframe().f_code.co_name,self.nowtime))
            raise e
        else:
            self.Log.info("%s test pass" % sys._getframe().f_code.co_name)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(LoginTest)
    unittest.TextTestRunner(verbosity=1).run(suite)in(2)