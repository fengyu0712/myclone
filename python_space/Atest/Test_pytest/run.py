import pytest
from Common import PC_cmd
# pytest.main([ '--alluredir ', 'E:/python_space/1test/Test_pytest/'])
filename = "E:\python_space\TestResult/allure_result"
test_path="E:\python_space\TestCase"
# pytest.main([test_path,'-m','smoke','--html',filename])
pytest.main([test_path,'--alluredir',filename])
# shell1 = "allure generate E:\python_space\TestResult/allure_result -o E:\python_space\TestResult\Report/allure_report"
# shell2 = "allure open -h 127.0.0.1 -p 8083 E:\python_space\TestResult\Report/allure_report"
# PC_cmd.cmd(shell1)
# PC_cmd.cmd(shell2)