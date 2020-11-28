#!D:\Python33
import HTMLTestRunners
import time,sys,os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)    #获取绝对路径，以便shell脚本跑
from Common.send_mail import Mail
from Common.createt_Testsuite import CreateSuite
from Conf import Project_path

def run_main():
    test_path_name="InterFere_Test/new"   #"InterFere_Test" 接口  UI_Test UI
    case_path = Project_path.TestCase_path + test_path_name
    now = time.strftime("%Y-%m-%d", time.localtime())
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
    # m=Mail()
    # m.creat_mail(filename,subject)
    # m.sent_mail()


if __name__=="__main__":
    run_main()




