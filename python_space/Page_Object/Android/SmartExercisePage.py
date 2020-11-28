
start_location="com.jeagine.cloudinstitute:id/btn_start"

class SmartExam:
    def __init__(self,driver):
        self.driver=driver
    def start_answer(self):
        self.driver.find_element_by_id(start_location).click()