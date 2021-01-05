import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import pytest
import time
import Project_path



now = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())
result_file= Project_path.TestResult_path + "allure_result\\"
report_file= Project_path.TestReport_path + "allure_report\\"

test_path=Project_path.TestCase_path+"\\TestAiyunNew\\test_allureDemo.py"
pytest.main(["-s",test_path,'--alluredir',result_file])
os.system("chcp 65001")


print("allure generate %s -o %s --clean"%(result_file,report_file))
print("allure open  %s"%report_file)
os.system("allure generate %s -o %s --clean"%(result_file,report_file))
os.system("allure open  %s"%report_file)