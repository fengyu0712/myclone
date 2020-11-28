from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  selenium.webdriver.common.by import By
from appium import webdriver
from Conf import Project_path

submit_button_location="com.jeagine.cloudinstitute:id/bt_submit"

class AnswerCard:
    def __init__(self,driver):
        self.driver=driver
    def submit(self):
        self.driver.find_element_by_id(submit_button_location).click()

