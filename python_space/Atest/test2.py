# -*- coding:utf-8 -*-
# @Time : 2019/3/15 0015
# @Author : Momentan
# @Software : PyCharm

import  unittest
import requests
import time
import  HTMLTestRunner
class Test(unittest.TestCase):

    def  setUp(self):
        self.url = 'https://httpbin.org/post'
        self.payload = {'key':'value','key2':'value'}
        print('============开始执行用例=========')

    def tearDown(self):
        print('============用例执行完成=============')

    def test_Add(self):
        r = requests.post(self.url,data=self.payload)
        t = r.json()
        self.assertEqual(t['url'],'https://httpbin.org/post')
        self.assertEqual(t['url'],'https://httpbin.org/post2',msg='断言是吧')

    def test_Best(self):
        r = requests.post(self.url, data=self.payload)
        self.assertEqual(r.status_code,200)



if __name__ == '_main_':

    # 构建测试套件
    suite = unittest.TestSuite()
    suite.addTest(Test('test_Add'))
    suite.addTest(Test('test_Best'))
    # 按照当前时间
    now = time.strftime("%Y-%m-%d %H_%M_%S")

    # 定义报告存路径
    filename = 'F:\python_space\TestResult\Report/' + now + 'result.html'
    fp = open(filename,'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='baogao',description='用例执行情况')
    runner.run(suite)
    fp.close()