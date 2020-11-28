from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  selenium.webdriver.common.by import By
from Common.regular import regular



page_title_location="com.jeagine.cloudinstitute:id/tv_title"
rate_riget_location="// android.widget.TextView[contains(text(),'正确答案')]"
finish_answer_location="com.jeagine.cloudinstitute:id/tv_submit"


class Result:
    def __init__(self,driver):
        self.driver=driver
        WebDriverWait(self.driver, 10, 0.2).until(EC.visibility_of_element_located((By.ID, page_title_location)))
    def get_rate(self):
        result = self.driver.find_element_by_android_uiautomator(
            'new UiSelector().textContains("正确率")').text      # 根据text模糊定位
        expression = "正确率(.*)%"
        rate = regular(expression, result, 1)
        return rate
    def finish_answer(self):
        self.driver.find_element_by_id(finish_answer_location).click()