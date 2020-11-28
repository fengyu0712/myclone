import pytest,time
from Conf import Project_path
from Common.send_mail import Mail
now=time.strftime("%Y%m%d%H%M%S")
test_path="D:/Users\ex_lijq4\Documents\python_space"
filename = Project_path.TestReport_path + now + "_PyTestReport.html"
# pytest.main([test_path,'-m','smoke','--html',filename])
pytest.main([test_path,'--html',filename])
# subject="【%s】测试报告"%test_path
# m=Mail()
# m.creat_mail(filename,subject)
# m.sent_mail()