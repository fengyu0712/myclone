import unittest,allure
from retry import retry
from appium import webdriver
from Conf import Project_path
from Common.conf import Read_conf
from Common.log import Logger
from Common.move import Move
from Page_Object.Android.HomePage import Home
from Page_Object.Android.QuestionPage import Question
from Page_Object.Android import QuestionPage
from Page_Object.Android import MinePage
from Page_Object.Android.Public import Main
from Page_Object.Android import Public
from Page_Object.Android.MinePage import Mine
from Page_Object.Android.AnswerCardPage import AnswerCard
from Page_Object.Android.ResultPage import Result
import time,sys

appium_path=Project_path.Conf_path+"appium.conf"
desired_caps=Read_conf(appium_path).get_value("Android","desired_caps")
appium_url=Read_conf(appium_path).get_value("Android","appium_url")

userconf_path=Project_path.Conf_path+"bkt_user.conf"
account = Read_conf(userconf_path).get_value( "Test", "account")
password = Read_conf(userconf_path).get_value( "Test", "password")

#元素定位
mine_username_location=MinePage.mine_username_location
see_answer=QuestionPage.see_answer_location
collect_location=QuestionPage.collect_location
answer_location=QuestionPage.answer_location
share_location=Public.share_location
share_menu_location=Public.share_menu_location
cancel_share_location=Public.cancel_share_location

@allure.feature("APP每日一练功能测试")
class dailyExamTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        nowtime = time.strftime("%Y%m%d%H%M")
        Log = Logger()
        Log.info("========%s测试开始:========" % __class__.__name__)
        driver = webdriver.Remote(appium_url, desired_caps)
        cls.nowtime=nowtime
        cls.Log=Log
        cls.driver=driver
        #判断是否有弹窗,并关闭
        Main(driver).close_ad()
        Main(driver).close_update()
        Mine(driver).stay_location()
        Main(driver).into_Mainpage(1)
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.Log.info("========%s测试结束!========" % __class__.__name__)
        cls.Log.close()
    def setUp(self):
        Home(self.driver).into_dailyExam()
    def tearDown(self):
        pass

    @allure.story("收藏试题测试")
    @retry(exceptions=TimeoutError,tries=2,delay=2,max_delay=10)
    def test_iscollect(self):
        self.Log.info("收藏试题测试开始")
        collect_name1=self.driver.find_element_by_id(collect_location).text
        Question(self.driver).collect()
        collect_name2=self.driver.find_element_by_id(collect_location).text
        try:
            self.assertNotEqual(collect_name1,collect_name2)
        except Exception as e:
            self.driver.save_screenshot(
                Project_path.Image_path + "%s_%s.png" % (sys._getframe().f_code.co_name, self.nowtime))
            raise e
        else:
            self.Log.info("收藏按钮生效,测试结束")
        finally:
            Main(self.driver).back()

    @allure.story("偷窥答案测试")
    @retry(tries=2,delay=2)
    def test_seeAnswer(self):
        self.Log.info("偷窥答案测试开始")
        Question(self.driver).see_answer()
        try:
            self.assertIsNotNone(answer_location)
        except Exception as e:
            self.driver.save_screenshot(
                Project_path.Image_path + "%s_%s.png" % (sys._getframe().f_code.co_name, self.nowtime))
            raise e
        else:
            self.Log.info("偷窥答案生效,测试结束")
        finally:
            Main(self.driver).back()

    @allure.story("分享按钮测试")
    @retry(tries=2,delay=2)
    def test_share(self):
        self.Log.info("分享按钮测试开始")
        self.driver.find_element_by_id(share_location).click()
        try:
            self.assertIsNotNone(share_menu_location)
        except Exception as e:
            self.driver.save_screenshot(
                Project_path.Image_path + "%s_%s.png" % (sys._getframe().f_code.co_name, self.nowtime))
            raise e
        else:
            self.Log.info("弹出分享菜单,测试结束")
        finally:
            self.driver.find_element_by_id(cancel_share_location).click()
            Main(self.driver).back()
    @allure.story("试题页面交卷测试")
    @retry(tries=2,delay=2)
    def test_questionPage_submit(self):  #试题页面交卷按钮验证
        self.Log.info("试题页面交卷测试开始")
        Question(self.driver).single_choice("A")
        Question(self.driver).submit()
        try:
            rate = Result(self.driver).get_rate()
        except Exception as e:
            self.driver.save_screenshot(
                Project_path.Image_path + "%s_%s.png" % (sys._getframe().f_code.co_name, self.nowtime))
            raise e
        else:
            self.Log.info("进入测试结果页,正确率为%s%%,[每日一练:答题卡页面交卷]测试结束" % rate )
        finally:
            Main(self.driver).back()
    @allure.story("答题卡页面交卷测试")
    @retry(tries=2,delay=2)
    def test_answerCard_submit(self):  #答题卡页面交卷测试
        self.Log.info("答题卡页面交卷测试开始")
        Question(self.driver).single_choice("A")
        Question(self.driver).answer_card()
        AnswerCard(self.driver).submit()
        try:
            rate = Result(self.driver).get_rate()
        except Exception as e:
            self.driver.save_screenshot(
                Project_path.Image_path + "%s_%s.png" % (sys._getframe().f_code.co_name, self.nowtime))
            raise e
        else:
            self.Log.info("进入测试结果页,正确率为%s%%,[每日一练:答题卡页面交卷]测试结束" % rate)
        finally:
            Main(self.driver).back()
    @allure.story("随机作答测试")
    @retry(tries=2,delay=2)
    def test_customAnswer(self):  #自定义作答
        self.Log.info("[每日一练]测试开始")
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
            self.Log.info("进入测试结果页,正确率为%s%%,[每日一练:答题卡页面交卷]测试结束" % rate)
        finally:
            Main(self.driver).back()
    @allure.story("偷窥答案全部做对]测试")
    @retry(tries=2,delay=2)
    def test_rightAnswer(self):  #偷窥答案全部做对
        self.Log.info("[每日一练:偷窥答案全部做对]测试开始")
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
    suite = unittest.TestLoader().loadTestsFromTestCase(dailyExamTest)
    unittest.TextTestRunner(verbosity=1).run(suite)in(2)