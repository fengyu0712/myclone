

import allure
import pytest
import time
import os
import Project_path
import jsonpath
from testcase.simDevices import SimDevices

wavfail1 = Project_path.TestData_path + "test_audio\\201M24_01_41_0001.wav"
wavfail2 = Project_path.TestData_path + "test_audio\\237M32_08_41_0160.wav"
wavfail3 = Project_path.TestData_path + "test_audio\\佛山的天气如何.wav"



data = [
    ("case1", wavfail1, "打开卧室空调"),
    ("case2", wavfail2, "打开卧室空调"),
    ("case3", wavfail3, "佛山的天气如何")
]



@allure.feature("1C")
class TestDemo():
    def setup(self):
        self.host = os.environ["host"]
        url = self.host + "/cloud/connect"
        print(url)
        self.ws = SimDevices(url)
        self.log = "链接建立成功"
        pass

    def teardown(self):
        self.ws.close()
        pass

    # @pytest.mark.parametrize('username,pwd,tatile', data)
    @allure.step(title="设备上线")
    def online(self):
        login=self.ws.on_line()
        print(login)
        self.log = "\n" + str(time.time()) + ":设备上线"
        # self.log += "\n" + str(time.time()) + "：" + username + "==>" + pwd
        print("登录成功")

    @allure.step(title="发送音频")
    def speech(self, casenum, wavfail):
        result=self.ws.speech(wavfail)
        self.log = "\n" + str(time.time()) + ":发送音频"
        self.log += "\n" + str(time.time()) + "：" + casenum + "==>" + wavfail
        return result



    @allure.step(title="请求设备状态")
    def check(self, casenum, wavfail):

        self.log += "\n" + str(time.time()) + ":请求设备状态"
        self.log += "\n" + str(time.time()) + "：" + casenum + "==>" + wavfail
        print("设备状态获取成功")

    @pytest.mark.parametrize('casenum,wavfail,asr', data)
    def test_allure(self, casenum, wavfail, asr):
        self.online()
        result=self.speech(casenum, wavfail)
        print(result)
        asr_result=eval(result['asr'])['data']['asr']

        # self.check(username, pwd)
        allure.attach(self.log, "log")
        allure.dynamic.story(casenum)
        assert asr_result == asr
        print(casenum,wavfail, asr)