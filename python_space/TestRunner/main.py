#!/bin/env python
import HTMLTestRunners
import time
from Common.send_mail import Mail
from Common.createt_Testsuite import CreateSuite
from Conf import Project_path

if __name__=="__main__":
    test_path_name="InterFere_Test"   #"InterFere_Test" 接口  UI_Test UI
    case_path = Project_path.TestCase_path + test_path_name
    now = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())
    filename = Project_path.TestReport_path + now + "_TestReport.html"
    fp = open(filename, 'wb')
    subject="%s测试报告"%test_path_name
    runner = HTMLTestRunners.HTMLTestRunner(
        stream=fp,
        title=subject,
        description=u'用例执行情况：',
        tester="Lee"
    )
    runner.run(CreateSuite(case_path))
    # 关闭文件流，不关的话生成的报告是空的
    fp.close()
    m=Mail()
    m.creat_mail(filename,subject)
    m.sent_mail()



#单个文件测试报告
    # suite=unittest.TestLoader().loadTestsFromTestCase(TestLogin)
    #
    # now = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())
    # filename = Project_path.TestReport_path + now + "TestReport.html"
    # fp = open(filename, 'wb')
    # runner = HTMLTestRunner.HTMLTestRunner(
    #     stream=fp,
    #     title=u'接口测试报告',
    #     description=u'用例执行情况：')
    # runner.run(suite)
    # fp.close()


