from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  selenium.webdriver.common.by import By
from Conf import Project_path
from Common.conf import Read_conf


mainmenu_location="com.jeagine.cloudinstitute:id/tab_img_%s"
back_button_location="com.jeagine.cloudinstitute:id/zhuce1_back"
quit_login_button_location="com.jeagine.cloudinstitute:id/rl_memberinfo_logout"
Yes_location="com.jeagine.cloudinstitute:id/confirm_btn"
close_advertising_location="com.jeagine.cloudinstitute:id/ib_close"
close_update_location="com.jeagine.cloudinstitute:id/btn_close"
share_location="com.jeagine.cloudinstitute:id/iv_share"
share_menu_location="com.jeagine.cloudinstitute:id/share_popuwindow"
cancel_share_location="com.jeagine.cloudinstitute:id/btn_cencel"
confirm_window="com.jeagine.cloudinstitute:id/layout"#原毙考题弹窗
yidian_confirm_window="com.jeagine.cloudinstitute:id/tvTitle"


userconf_path=Project_path.Conf_path+"bkt_user.conf"
account = Read_conf(userconf_path).get_value( "Test", "account")
password = Read_conf(userconf_path).get_value( "Test", "password")
class Main:
    def __init__(self,driver):
        self.driver=driver
    def into_Mainpage(self, type):   #type=  1:首页  2:学习 3:考友圈 4:我的.............
        try:
            WebDriverWait(self.driver, 10, 0.2).until(EC.visibility_of_element_located((By.ID, mainmenu_location % type)))
        except Exception as e:
            raise e
        else:
            self.driver.find_element_by_id(mainmenu_location % type).click()
    def back(self):
        WebDriverWait(self.driver, 10, 0.2).until(EC.visibility_of_element_located((By.ID, back_button_location)))
        self.driver.find_element_by_id(back_button_location).click()
        try:
            WebDriverWait(self.driver, 2, 0.2).until(EC.visibility_of_element_located((By.ID, confirm_window)))
        except:
            pass
        else:
           self.driver.click_windows("确定")
    def close_ad(self):
        try:
            self.driver.find_element_by_id(close_advertising_location).is_displayed()
        except :
            pass
        else:
            self.driver.find_element_by_id(close_advertising_location).click()
    def close_update(self):
        try:
            WebDriverWait(self.driver,2,0.2).until(EC.visibility_of_element_located((By.ID,close_update_location)))
        except :
            pass
        else:
            self.driver.find_element_by_id(close_update_location).click()
    def click_windows(self,choice):  #choice 确认或者取消
        try:
            WebDriverWait(self.driver, 2, 0.2).until(EC.visibility_of_element_located((By.ID, yidian_confirm_window)))
        except:
            pass
        else:
            self.driver.find_element_by_name(choice).click()



