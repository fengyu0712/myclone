import unittest
# from Conf import Project_path

def CreateSuite(case_path):
    testunit=unittest.TestSuite()
    #在case_path目录搜索test_开头的文件,加入测试集合
    discover=unittest.defaultTestLoader.discover(case_path,pattern='test_*.py',top_level_dir=None)
    for test_suite in discover:
        for test_case in test_suite:
            testunit.addTest(test_case)
    return testunit
    # for test_suit in  discover:
    #     testunit.addTests(test_suit)
    #     return testunit
if __name__=='__main__':
    case_path='E:\pachong\single\chrom'
    a=CreateSuite(case_path)
    print(a)