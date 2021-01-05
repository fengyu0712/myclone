import pytest
import time
import Project_path
import os

now = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())
result_file = Project_path.TestResult_path + "allure_result\\"
report_file = Project_path.TestReport_path + "allure_report\\"

# test_path = Project_path.TestCase_path + "\\TestAiyunNew\\"" \
test_path=r"F:\git\myclone\AITEST\testcase\TestAiyunNew\test_allureDemo.py"
# pytest.main(["-s","--env=www.baidu.com",test_path,'--alluredir',result_file])
pytest.main(["-s", f'--alluredir={result_file}', "--env=UAT", test_path, '--allure-features=AC,1C'])


# os.system("chcp 65001")


def run():
    # pytest.main()
    pytest.main(["-s", "q", '-n=1', test_path, f'--alluredir={result_file}', '--allure-features=AC,1C'])
    # pytest.main(["-s",  test_path, '--alluredir', result_file])
    # '-s' 展示日志
    # '-p' 隐藏pytest打印日志
    # '-n=2'  分布式运行，n后面为CPU数量      多进程数据写入存在问题
    # '--alluredir'  执行文件夹下的所有
    # '--allure-features=PYTEST'  运行选定的标签或者场景


print("allure generate %s -o %s --clean" % (result_file, report_file))
print("allure open  %s" % report_file)
os.system("allure generate %s -o %s --clean" % (result_file, report_file))
os.system("allure open  %s" % report_file)
