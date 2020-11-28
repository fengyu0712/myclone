import unittest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  selenium.webdriver.common.by import By
from appium import webdriver
from Conf import Project_path
from Common.conf import Read_conf
from Common.log import Logger
from Common.move import Move
from Common.regular import regular
from Page_Object.Android.LoginPage import Login
from Page_Object.Android.Public import  Main
from Page_Object.Android.HomePage import Home
from Page_Object.Android import QuestionPage
from Page_Object.Android import ResultPage
from Page_Object.Android.QuestionPage import Question
from Page_Object.Android.AnswerCardPage import AnswerCard
from Page_Object.Android.ResultPage import Result
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
result_pagetitle=ResultPage.page_title_location

userconf_path=Project_path.Conf_path+"bkt_user.conf"
account = Read_conf(userconf_path).get_value( "Test", "account")
password = Read_conf(userconf_path).get_value( "Test", "password")

class TestBProcess(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Logger().info("========%s测试开始========" % __class__.__name__)
        nowtime = time.strftime("%Y%m%d%H%M")
        Log = Logger()
        driver = webdriver.Remote(appium_url, desired_caps)
        cls.nowtime=nowtime
        cls.Log=Log
        cls.driver=driver
        Main(driver).close_ad()
        # 判断是否有弹窗,并关闭
    @classmethod
    def tearDownClass(cls):
        cls.Log.info("========%s测试结束!========" % __class__.__name__)
        cls.driver.quit()
        cls.Log.close()

    def test_account_login(self):
        self.Log.debug("登录测试开始")
        Mine(self.driver).stay_unlocation()
        Login(self.driver).account_login(account,password)
        try:     #验证登录
            Mine(self.driver).get_accountname()
        except Exception as e:
            self.driver.save_screenshot(Project_path.Image_path+"%s_%s.png"%(sys._getframe().f_code.co_name,self.nowtime))
            raise e
        else:
            self.Log.debug("登录成功")
            self.Log.info("%s test pass" % sys._getframe().f_code.co_name)

    def test_everydayExercise(self):
        self.Log.info("[每日一练]测试开始")
        Main(self.driver).into_Mainpage(1)
        Home(self.driver).shot_menu("每日一练")
        try:
            WebDriverWait(self.driver,5, 0.2).until(EC.visibility_of_element_located((By.NAME, "再做一遍")))
        except:
            pass
        else:
            self.driver.find_element_by_name("再做一遍").click()
        while True:
            try:
                title = Question(self.driver).confirm_type()
                if "单" in title:
                    Question(self.driver).single_choice("A")
                elif "多" in title:
                    Question(self.driver).multiple_choice(["A", "B"])
                    Move(self.driver).swipLeft()
                else:
                    Move(self.driver).swipLeft()
            except Exception as e:
                break
                self.driver.save_screenshot(
                    Project_path.Image_path + "%s_%s.png" % (sys._getframe().f_code.co_name, self.nowtime))
                raise e
        try:
            rate=Result(self.driver).get_rate()
        except Exception as e:
            self.driver.save_screenshot(
                Project_path.Image_path + "%s_%s.png" % (sys._getframe().f_code.co_name, self.nowtime))
            raise e
        else:
            self.Log.info("进入测试结果页,[每日一练]测试结束,正确率为%s%%"%rate)
        finally:
            Main(self.driver).back()

    def test_everydayExercise_right(self):
        self.Log.info("[每日一练:偷窥答案全部做对]测试开始")
        Main(self.driver).into_Mainpage(1)
        Home(self.driver).shot_menu("每日一练")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located((By.NAME, "再做一遍")))
        except:
            pass
        else:
            self.driver.find_element_by_name("再做一遍").click()
        while True:
            try:
                title = Question(self.driver).confirm_type()
                if "单" in title:
                    Question(self.driver).right_answer()
                elif "多" in title:
                    Question(self.driver).right_answer()
                    Move(self.driver).swipLeft()
                else:
                    Move(self.driver).swipLeft()
            except Exception as e:
                break
                self.driver.save_screenshot(
                    Project_path.Image_path + "%s_%s.png" % (sys._getframe().f_code.co_name, self.nowtime))
                raise e
        try:
            rate = int(Result(self.driver).get_rate())
            self.assertEqual(rate,100)
        except Exception as e:
            self.driver.save_screenshot(
                Project_path.Image_path + "%s_%s.png" % (sys._getframe().f_code.co_name, self.nowtime))
            raise e
        else:
            self.Log.info("正确率是100%,[每日一练:偷窥答案全部做对]测试结束")
        finally:
            Main(self.driver).back()




if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBProcess)
    unittest.TextTestRunner(verbosity=1).run(suite) in (2)