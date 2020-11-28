import unittest,os
from multiprocessing import Pool
import pytest,time,random
from Conf import Project_path



def runpy(test_path):
    print('Parent process %s.' % os.getpid())
    result_file = Project_path.TestResult_path + "allure_result/"
    report_file = Project_path.TestReport_path + "allure_report/"
    pytest.main(["-s", test_path, '--alluredir', result_file])
    # shell1 = "allure generate %s -o %s --clean"%(result_file,report_file)
    shell3 = "allure generate %s -o %s " % (result_file, report_file)
    shell2 = "allure open  %s"%report_file
    os.system(shell3)
    os.system(shell2)



if __name__=='__main__':
    case_path1 = "E:\pachong\single\chrom"
    case_path2 = "E:\pachong\single/firefox"
    path = [case_path1, case_path2]
    now = time.strftime("%Y%m%d%H%M%S")
    filename = 'E:/pachong/result/' + now + "_PyTestReport.html"
    # path="E:/pachong/single/chrom/"
    # runpy(path)
    p = Pool(4)
    for i in path:
        # p.apply_async(pytest.main([path[i],'--html',filename]), args=(i,))
         p.apply_async(runpy, args=(i,))      #apply_async   引入的函数如果带有其他变量多进程会滞留，直接带入i不会
    # for i in range(5):
    #    p.apply_async(deam,args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')

