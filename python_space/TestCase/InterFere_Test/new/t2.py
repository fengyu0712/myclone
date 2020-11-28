# from TestCase.InterFere_Test.new import t1
# from TestCase.InterFere_Test.new import test_Login
import unittest,allure
from ddt import ddt,data
from Common.log import Logger

data1=[[{'url': 'http://bkt.jeagine.com/api/user/signin', 'type': 'get', 'header': '', '参数': "{'account': '13017600000', 'appKey': 'all', 'category_id': 80, 'password': '123456', 'terminal': 2}", '继承参数': '', '调用参数': '', '下传参数': '{\'uid\':\'/"id":(.+?),/"\'}'},  {'url': 'http://bkt.jeagine.com/api/user/mission/list', 'type': 'get', 'header': '', '参数': "{'uid': ''}", '继承参数': '', '调用参数': '["uid"]', '下传参数': '{\'addExperienceValue\': "checkInCount\': (.*?), \'name"}'},  'code'], [{'url': 'http://bkt.jeagine.com/api/user/signin', 'type': 'get', 'header': '', '参数': "{'account': '13017600000', 'appKey': 'all', 'category_id': 80, 'password': '123456', 'terminal': 3}", '继承参数': '', '调用参数': '', '下传参数': '{\'uid\':\'/"id":(.+?),/"\'}'}, {'url': 'http://bkt.jeagine.com/api/user/mission/list', 'type': 'get', 'header': '', '参数': "{'uid': ''}", '继承参数': '', '调用参数': '["uid"]', '下传参数': '{\'addExperienceValue\': "checkInCount\': (.*?), \'name"}'}, 'code']]
@ddt
class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Log = Logger()
        Logger().info("%s测试开始:" % __class__.__name__)
        cls.Log = Log
        pass

    @classmethod
    def tearDownClass(cls):
        pass


    # @allure.story('登录功能接口')
    @data(*data1)
    def test_run(self,tdata):
        try:
            self.assertEqual(tdata[-1], 'code', "与期望值不符")
        except Exception as e:
            raise e
        self.Log.info(tdata[-1])
        pass