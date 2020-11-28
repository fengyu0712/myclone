#!D:\Python33
import HTMLTestRunners
import time,sys,os,threading
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)    #获取绝对路径，以便shell脚本跑
from Common.send_mail import Mail
from Common.createt_Testsuite import CreateSuite
from Conf import Project_path
from multiprocessing import Pool


def run_main():
    test_path_name="InterFere_Test"   #"InterFere_Test" 接口  UI_Test UI
    case_path = Project_path.TestCase_path + test_path_name
    now = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())
    filename = Project_path.TestReport_path + now + "TestReport.html"
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

def demo():
    print("执行任务")






if __name__=="__main__":
    start_time = time.time()
    p = Pool(2)
    for i in range(1):
        print("当前执行：%s" % i)
        p.apply_async(demo, args=(i,))  # apply_async   引入的函数如果带有其他变量多进程会滞留，直接带入i不会
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
    endtime = time.time()
    print("this run take %s seconds" % format(endtime - start_time))

    # start_time = time.time()
    # threads = []
    #
    # # start all threading.
    # for i in range(1, 3):
    #     t = threading.Thread(target=run_main())
    #     t.start()
    #     print("thread %s start"%i)
    #     threads.append(t)
    #
    # # wait until all the threads terminnates.
    # for thread in threads:
    #     thread.join()
    # endtime=time.time()
    # print("this run take %s seconds"%format(endtime - start_time))




