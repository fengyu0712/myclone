from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  selenium.webdriver.common.by import By

account_location = "//input[@name='phone']"
password_location = "//input[@name='password']"
login_button_location = "//button[text()='登录']"

error_wrongphone_location="//div[text()='请输入正确的手机号']"
error_noaccount_location="//div[text()='请输入手机号']"
error_nopassword_location="//div[text()='请输入密码']"
error_wrongpassword_location="//div[text()='帐号或密码错误!']"
error_wrongaccount_location="//div[text()='此账号没有经过授权，请联系管理员!']"

class Login:
    def __init__(self,driver):
        self.driver=driver
    def login(self,account,password):
        try:
            WebDriverWait(self.driver, 10, 0.2).until(EC.visibility_of_element_located((By.XPATH,account_location)))
        except Exception as e:
            raise e
        else:
            self.driver.find_element_by_xpath(account_location).clear()
            self.driver.find_element_by_xpath(account_location).send_keys(account)
            self.driver.find_element_by_xpath(password_location).send_keys(password)
            self.driver.find_element_by_xpath(login_button_location).click()

# driver = webdriver.Chrome()
# conf_path = "E:\PycharmProjects\po_test_qianchengdai\Web.conf"
# driver.get("http://120.76.42.189:8765/Index/login.html")
# url = ReadConf(conf_path,"Login","url").getvalue()
# account = ReadConf(conf_path,"Login","account").getvalue()
# password = ReadConf(conf_path,"Login","password").getvalue()
# myaccount_location = "//a[text()='我的帐户[土小姐]']"
#
# login_page=Login(driver)
# login_page.login(url,account,password)
# WebDriverWait(driver,20,0.5).until(EC.visibility_of_element_located((By.XPATH,myaccount_location)))
# try:
#     driver.find_element_by_xpath(myaccount_location)
#     print( "登录成功")
# except Exception as e:
#     print("登录异常:%s"%e)
