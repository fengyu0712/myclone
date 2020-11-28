from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  selenium.webdriver.common.by import By

bid_history_location = "//div[text()='投资项目']"
amount_location = "//li[@class='color_sub']"
bid_name_location = "//div[@ms-controller='tz_list']//div[text()='%s']//following-sibling::div[text()='%s']//parent::td//following-sibling::td//a"
bid_money_location = "//div[@ms-controller='tz_list']//div[text()='%s']//following-sibling::div[text()='%s']//parent::td//following-sibling::td//div[text()='本金']//preceding-sibling::div"
class UserInfo:
    verificationErrors=[]
    def __init__(self,driver):
        self.driver=driver
    def my_amount(self):
        try:
            WebDriverWait(self.driver, 10, 0.2).until(EC.visibility_of_element_located((By.XPATH,amount_location)))
        except Exception as e:
            raise e
        else:
            myamount=self.driver.find_element_by_xpath(amount_location).text
            return myamount

    def into_bid_hitory(self):
        WebDriverWait(self.driver, 10, 0.2).until(EC.visibility_of_element_located((By.XPATH,bid_history_location)))
        self.driver.find_element_by_xpath(bid_history_location).click()

    def find_mybid(self,ymd,hm):
        WebDriverWait(self.driver, 20, 0.5).until(EC.visibility_of_element_located((By.XPATH, bid_name_location% (ymd, hm))))
        result_bid_name=self.driver.find_element_by_xpath(bid_name_location% (ymd, hm)).text
        result_bid_money=self.driver.find_element_by_xpath(bid_money_location).text
        return [result_bid_name,result_bid_money]



