from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  selenium.webdriver.common.by import By
from Page_Object.Android.Public import Main
from Conf import Project_path
from Common.conf import Read_conf

mainmenu_location="com.jeagine.cloudinstitute:id/tab_img_%s"
back_button_location="com.jeagine.cloudinstitute:id/zhuce1_back"
quit_login_button_location="com.jeagine.cloudinstitute:id/rl_memberinfo_logout"
confirm_window="com.jeagine.cloudinstitute:id/layout"
mine_login_location="com.jeagine.cloudinstitute:id/tv_fast_login"
mine_username_location="com.jeagine.cloudinstitute:id/tv_user_name"
account_login_location="com.jeagine.cloudinstitute:id/tv_quick_login"
account_location="com.jeagine.cloudinstitute:id/et_username"
password_location="com.jeagine.cloudinstitute:id/et_password"
login_botton_location="com.jeagine.cloudinstitute:id/btn_login"

userconf_path=Project_path.Conf_path+"bkt_user.conf"
account = Read_conf(userconf_path).get_value( "Test", "account")
password = Read_conf(userconf_path).get_value( "Test", "password")

class Mine:
    def __init__(self,driver):
        self.driver=driver
        try:
            Main(self.driver).into_Mainpage(4)
        except:
            pass
    def into_login(self):
        # 进入登录页
        try:
            WebDriverWait(self.driver, 5, 0.2).until(EC.visibility_of_element_located((By.ID, mine_login_location)))
        except Exception as e:
            raise e
        else:
            self.driver.find_element_by_id(mine_login_location).click()
    def get_accountname(self):
        try:
            WebDriverWait(self.driver, 5, 0.2).until(EC.visibility_of_element_located((By.ID, mine_username_location)))
        except Exception as e:
            raise e
        else:
            account_name = self.driver.find_element_by_id(mine_username_location).text
            return account_name
    def quit_account(self):
        try:
            WebDriverWait(self.driver, 5, 0.2).until(EC.visibility_of_element_located((By.ID, mine_username_location)))
        except Exception as e:
            raise  e
        else:
            self.driver.find_element_by_id(mine_username_location).click()
            try:
                WebDriverWait(self.driver, 10, 0.2).until(EC.visibility_of_element_located((By.ID, quit_login_button_location)))
            except Exception as e:
                raise e
            else:
                self.driver.find_element_by_id(quit_login_button_location).click()
                Main(self.driver).click_windows("确定")
    def stay_location(self):
        try:
            WebDriverWait(self.driver, 5, 0.2).until(EC.visibility_of_element_located((By.ID, mine_username_location)))
        except:
            # Login(self.driver).account_login()
            Mine(self.driver).into_login()
            try:
                WebDriverWait(self.driver, 10, 0.2).until(
                    EC.visibility_of_element_located((By.ID, account_login_location)))
            except Exception as e:
                raise e
            else:
                self.driver.find_element_by_id(account_login_location).click()
            try:
                WebDriverWait(self.driver, 10, 0.2).until(EC.visibility_of_element_located((By.ID, account_location)))
            except Exception as e:
                raise e
            else:
                # 判断是否有输入,有输入则清楚后输入
                self.driver.find_element_by_id(account_location).clear()
                self.driver.find_element_by_id(account_location).send_keys(account)
                self.driver.find_element_by_id(password_location).clear()
                self.driver.find_element_by_id(password_location).send_keys(password)
                self.driver.find_element_by_id(login_botton_location).click()
                Main(self.driver).close_update()
    def stay_unlocation(self):
        try:
            WebDriverWait(self.driver, 10, 0.2).until(EC.visibility_of_element_located((By.ID, mine_login_location)))
            # self.driver.find_element_by_id(mine_login_location).is_displayed()
        except :
            self.quit_account()


