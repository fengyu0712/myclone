from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  selenium.webdriver.common.by import By
from Page_Object.Android.MinePage import Mine
from Page_Object.Android.Public import Main
from Common.conf import Read_conf
from Conf import Project_path



account_login_location="com.jeagine.cloudinstitute:id/tv_quick_login"
account_location="com.jeagine.cloudinstitute:id/et_username"
clear_account_location="com.jeagine.cloudinstitute:id/iv_clear_username"
password_location="com.jeagine.cloudinstitute:id/et_password"
clear_password_location="com.jeagine.cloudinstitute:id/iv_clear_password"
login_botton_location="com.jeagine.cloudinstitute:id/btn_login"
warning_location="com.jeagine.cloudinstitute:id/tv_tips_code"


userconf_path=Project_path.Conf_path+"bkt_user.conf"
account = Read_conf(userconf_path).get_value( "Test", "account")
password = Read_conf(userconf_path).get_value( "Test", "password")

class Login:
    def __init__(self,driver):
        self.driver=driver
    def into_account_login(self):
        Mine(self.driver).into_login()
        try:
            WebDriverWait(self.driver, 10, 0.2).until(EC.visibility_of_element_located((By.ID, account_login_location)))
        except Exception as e:
            raise e
        else:
            self.driver.find_element_by_id(account_login_location).click()
    def account_login(self,account=account,password=password):
        self.into_account_login()
        try:
            WebDriverWait(self.driver, 10, 0.2).until(EC.visibility_of_element_located((By.ID, account_location)))
        except Exception as e:
            raise e
        else:
            #判断是否有输入,有输入则清楚后输入
            self.driver.find_element_by_id(account_location).clear()
            self.driver.find_element_by_id(account_location).send_keys(account)
            self.driver.find_element_by_id(password_location).clear()
            self.driver.find_element_by_id(password_location).send_keys(password)
            self.driver.find_element_by_id(login_botton_location).click()
        Main(self.driver).close_update()
    def warn(self):
        try:
            WebDriverWait(self.driver, 5, 0.2).until(EC.visibility_of_element_located((By.ID, warning_location)))
        except Exception as e:
            raise e
        else:
            warn_title = self.driver.find_element_by_id(warning_location).text
            return warn_title

    def phone_login(self,phone,vcode):
        Mine(self.driver).into_login()
        pass


