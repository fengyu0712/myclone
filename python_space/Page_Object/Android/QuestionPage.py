from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  selenium.webdriver.common.by import By
from Common.regular import regular
from Page_Object.Android.Public import Main

close_advertising_location="com.jeagine.cloudinstitute:id/ib_close"
question_type_location="com.jeagine.cloudinstitute:id/tv_title_name"
question_location="com.jeagine.cloudinstitute:id/tv_question"
see_answer_location="com.jeagine.cloudinstitute:id/tv_see"
answer_location="com.jeagine.cloudinstitute:id/look_tv_right_answer"
submit_location="com.jeagine.cloudinstitute:id/tv_submit"
collect_location="com.jeagine.cloudinstitute:id/tv_collect"
answer_card="com.jeagine.cloudinstitute:id/tv_sheet"
confirm_window="com.jeagine.cloudinstitute:id/layout"
class Question:
    def __init__(self,driver):
        self.driver=driver
        WebDriverWait(self.driver, 10, 0.2).until(EC.visibility_of_element_located((By.ID, question_location)))
    def confirm_type(self):
        title=self.driver.find_element_by_id(question_type_location).text
        return title
    def single_choice(self,options):
        self.driver.find_element_by_name(options).click()
    def multiple_choice(self,options_list):
        for each in  options_list:
            self.single_choice(each)

    def right_answer(self):  # 有偷窥答案才可以用
        self.see_answer()
        answer = self.driver.find_element_by_id(answer_location).text
        self.see_answer()
        expression = '：([^"]+) '
        answer_new = regular(expression, answer, 1)
        answer_list = []
        for each in answer_new:
            answer_list.append(each)
        self.multiple_choice(answer_list)
    def answer_question(self):
        pass
    def see_answer(self):
        self.driver.find_element_by_id(see_answer_location).click()
    def submit(self):
        self.driver.find_element_by_id(submit_location).click()
        try:
            WebDriverWait(self.driver, 2, 0.2).until(EC.visibility_of_element_located((By.ID, confirm_window)))
        except:
            pass
        else:
            Main(self.driver).click_windows("确定")
    def collect(self):
        self.driver.find_element_by_id(collect_location).click()
    def answer_card(self):
        self.driver.find_element_by_id(answer_card).click()





