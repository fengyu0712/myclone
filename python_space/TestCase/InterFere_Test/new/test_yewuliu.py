from  Common.read_xls import Read_xls
from  Common.write_xls import WriteExcel
from Common.http_request import Request
from  Common.list_dict import Change
from Common.conf import Read_conf
from Conf import Project_path
from Common.mysql import MySql
from Common.log import Logger
from Common import globalvar as gl
import time,unittest,pytest,sys,allure
from ddt import ddt,data
import unittest

host='http://bkt.jeagine.com'
@allure.feature('登录=》任务列表')
class TestT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Log=Logger()
        Logger().info("%s测试开始:" % __class__.__name__ )
        cls.Log=Log

    @classmethod
    def tearDownClass(cls):
        cls.Log.info("%s测试结束!" % __class__.__name__)
    @allure.story("请求登录接口")
    def test_login(self):
        global uid
        url='/api/user/signin'
        data={'account': 13017600000, 'appKey': 'all', 'category_id': 81, 'password': 123456, 'terminal': 2}
        type='get'
        result = Request(host).request(url, data, type)
        try:
            self.assertEqual(str(result['code']), '1', "与期望值不符")
        except Exception as e:
            self.Log.error("%s测试失败【%s】" % (sys._getframe().f_code.co_name, e))
            raise e
        else:
            self.Log.info("%s测试通过" % sys._getframe().f_code.co_name)
            result['code']==1
            uid = result['user']['id']
    @allure.story("请求任务列表接口")
    def test_mission(self):
        url='/api/user/mission/list'
        data={'uid':uid}
        type = 'get'
        result = Request(host).request(url, data, type)
        try:
            self.assertEqual(str(result['code']), '1', "与期望值不符")
        except Exception as e:
            self.Log.error("%s测试失败【%s】" % (sys._getframe().f_code.co_name, e))
            raise e
        else:
            self.Log.info("%s测试通过" % sys._getframe().f_code.co_name)

if __name__=="__main__":
    unittest.main(*sys.argv[1:])