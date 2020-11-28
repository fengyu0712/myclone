from Page_Object.Web.testpage import home_page
from Page_Object.Web.testpage import login_page
from Page_Object.Web.testpage.login_page import Login
from Page_Object.Web.testpage.home_page import Home
import sys,time

from Common.conf import Read_conf
from Common.log import Logger
from Common import PC_cmd
from Conf import Project_path
import pytest,allure


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



@pytest.mark.usefixtures("Web_driver_class","Web_driver")
@allure.feature('登录功能接口')
class Test_Login():
    nowtime=time.strftime("%Y%m%d%H%M")
    @allure.story('正常登录测试')
    @pytest.mark.smoke
    def test_login_ok(self,Web_driver_class):
        Logger().info("测试用例：正常登录")
        Login(Web_driver_class).login(login_account, password)
        try:
            assert pickname in Home(Web_driver_class).get_account_name()
        except Exception as e:
            Web_driver_class.save_screenshot(Project_path.Image_path+"%s_%s.png"%(sys._getframe().f_code.co_name,self.nowtime))
            Logger().error("%s test fail:%s" % (sys._getframe().f_code.co_name,e))
            Web_driver_class.execute_script('window.stop()')
            raise e
        else:
            Logger().info("%s test pass" % sys._getframe().f_code.co_name)
        finally:
            Home(Web_driver_class).quit_login()

    @allure.story('手机号错误登录测试')
    def test_login_wrongphone(self,Web_driver_class):
        Logger().info("测试用例：异常用例-手机号错误")
        Login(Web_driver_class).login("13017659465", "123456")
        try:
            assert Web_driver_class.find_element_by_xpath(error_wrongphone_location).is_displayed()
        except Exception as e:
            Web_driver_class.save_screenshot(Project_path.Image_path+"%s_%s.png"%(sys._getframe().f_code.co_name,self.nowtime))
            raise e
        else:
            Logger().info("%s test pass" % sys._getframe().f_code.co_name)

    @allure.story('无密码登录测试')
    def test_login_nopassword(self,Web_driver_class):
        Logger().info("测试用例：异常用例-密码为空")
        Login(Web_driver_class).login( login_account, "")
        try:
            assert Web_driver_class.find_element_by_xpath(error_nopassword_location).is_displayed()
        except Exception as e:
            Web_driver_class.save_screenshot(
                Project_path.Image_path + "%s_%s.png" % (sys._getframe().f_code.co_name, self.nowtime))
            raise e
        else:
            Logger().info("%s test pass" % sys._getframe().f_code.co_name)

    @allure.story('无账户登录测试')
    def test_login_noaccount(self,Web_driver_class):
        Logger().info("测试用例：异常用例-账户为空")
        Login(Web_driver_class).login( " ", password)
        try:
           assert Web_driver_class.find_element_by_xpath(error_noaccount_location).is_displayed()
        except Exception as e:
            Web_driver_class.save_screenshot(
                Project_path.Image_path + "%s_%s.png" % (sys._getframe().f_code.co_name, self.nowtime))
            raise e
        else:
            Logger().info("%s test pass" % sys._getframe().f_code.co_name)

    @allure.story('密码错误登录测试')
    def test_login_wrong_password(self,Web_driver_class):
        Logger().info("测试用例：异常用例-密码错误")
        Login(Web_driver_class).login( login_account, "11111111")
        try:
            assert Web_driver_class.find_element_by_xpath(error_wrongpassword_location).is_displayed()
        except Exception as e:
            Web_driver_class.save_screenshot(
                Project_path.Image_path + "%s_%s.png" % (sys._getframe().f_code.co_name, self.nowtime))
            raise e
        else:
            Logger().info("%s test pass" % sys._getframe().f_code.co_name)

    @allure.story('账户错误登录测试')
    def test_login_wrong_account(self,Web_driver_class):
        Logger().info("测试用例：异常用例-账户错误")
        Login(Web_driver_class).login( "13017659465", password)
        try:
            assert Web_driver_class.find_element_by_xpath(error_wrongaccount_location).is_displayed()
        except Exception as e:
            Web_driver_class.save_screenshot(Project_path.Image_path + "%s_%s.png" % (sys._getframe().f_code.co_name, self.nowtime))
            raise e
        else:
            Logger().info("%s test pass" % sys._getframe().f_code.co_name)
if __name__ == '__main__':

    shell1 = "allure generate E:\python_space\TestResult/allure_result -o E:\python_space\TestResult\Report --clean"
    shell2 = "allure open -h 127.0.0.1 -p 8083 E:\python_space\TestResult\Report"
    # pytest.main()
    pytest.main([ '--alluredir ', 'E:/python_space/1test/Test_pytest/'])
    # pytest.main(['--allure_stories=测试模块_demo1, 测试模块_demo2', '--allure_severities=critical, blocker'])
    # PC_cmd.cmd(shell1)
    PC_cmd.cmd(shell2)