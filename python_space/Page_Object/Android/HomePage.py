from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  selenium.webdriver.common.by import By
from Page_Object.Android.Public import Main
class Home:
    def __init__(self,driver):
        self.driver=driver
        Main(self.driver).into_Mainpage(1)
    def shot_menu(self,name):
        self.driver.find_element_by_name(name).click()
        pass
    def into_dailyExam(self):
        self.shot_menu("每日一练")
        try:
            WebDriverWait(self.driver,5, 0.2).until(EC.visibility_of_element_located((By.NAME, "再做一遍")))
        except:
            pass
        else:
            self.driver.find_element_by_name("再做一遍").click()



