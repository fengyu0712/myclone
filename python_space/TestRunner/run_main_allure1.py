import pytest
import time,sys,os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)    #获取绝对路径，以便shell脚本跑
from Common import PC_cmd
from Conf import Project_path

test_path_name = "InterFere_Test/new"  # "InterFere_Test" 接口  UI_Test UI
test_path = Project_path.TestCase_path+test_path_name
# test_path = Project_path.TestCase_path #仅PC端可用，云端无法启动app和浏览器
now = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())
result_file=Project_path.TestResult_path+"allure_result"
report_file=Project_path.TestReport_path+"allure_report"
shell1 = "allure generate %s -o %s --clean"%(result_file,report_file)
shell2 = "allure open  %s"%report_file


pytest.main(['-s', '-q',"D:/Users\ex_lijq4\Documents\python_space\TestCase/InterFere_Test/new", '--alluredir',"D:/Users\ex_lijq4\Documents\python_space\TestResult\Report/allure_report"])

