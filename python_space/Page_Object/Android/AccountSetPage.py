from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  selenium.webdriver.common.by import By
from appium import webdriver
from Conf import Project_path

quit_login_button_location="com.jeagine.cloudinstitute:id/rl_memberinfo_logout"
Yes_location="com.jeagine.cloudinstitute:id/confirm_btn"
class Accoune_set:
    def __init__(self,driver):
        self.driver=driver
        # 退出登录
    # def quit_account(self):
    #     WebDriverWait(self.driver, 10, 0.2).until(EC.visibility_of_element_located((By.ID, quit_login_button_location)))
    #     self.driver.find_element_by_id(quit_login_button_location).click()
    #     WebDriverWait(self.driver, 10, 0.2).until(EC.visibility_of_element_located((By.ID, Yes_location)))
    #     self.driver.find_element_by_id(Yes_location).click()