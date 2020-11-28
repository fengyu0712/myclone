# from Common.read_xls import Read_xls
# from Common.write_xls import WriteExcel
# from Common.http_request import Request
# from Common.list_dict import Change
# from Common.conf import Read_conf
# from Conf import Project_path
# from Common.mysql import MySql
# from Common.log import Logger
# from Common import globalvar as gl
import time,unittest,allure,pytest,sys,requests
from ddt import ddt,data

url="http://bkt.jeagine.com/api/user/signin"
class LoginTest(unittest.TestCase):
    def setUp(self):
        self.url=url
        pass
    def tearDown(self):
        pass
    def testlogin(self):
        # n=0
        error=0
        data={'account': '130000000000', 'appKey': 'all', 'category_id': 80, 'password': 123456, 'terminal': 2}
        # print("第%s次请求"%n)
        try:
            requests.get(self.url,data)
        except Exception as e:
            print(e)
            error+=1
        else:
            print("请求成功")
        # while  error<3:
        #     n+=1
        #     print("第%s次请求"%n)
        #     try:
        #         requests.get(self.url,data)
        #     except Exception as e:
        #         print(e)
        #         error+=1
        #     else:
        #         print("请求成功")

if __name__ == '__main__':
    unittest.main()