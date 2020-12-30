import allure
import pytest
import time
import os

data = [
    ("name1", "123456", "name1 登录成功"),
    ("name2", "123456", "name2 登录失败"),
    ("name3", "123456", "name1 登录成功")
]


@allure.feature("AC")
class TestLogin():
    def setup(self):
        self.log = ""
        # print(host)
        pass

    def teardown(self):
        pass

    # @pytest.mark.parametrize('username,pwd,tatile', data)
    @allure.step(title="设备上线")
    def login1(self, username, pwd):
        host=os.environ["host"]
        print(host)
        self.log = "\n" + str(time.time()) + ":准备数据"
        self.log += "\n" + str(time.time()) + "：" + username + "==>" + pwd

    @allure.step(title="发送音频")
    def login2(self, username, pwd):
        self.log = "\n" + str(time.time()) + ":发送音频"
        self.log += "\n" + str(time.time()) + "：" + username + "==>" + pwd
        print("登录成功")

    @allure.step(title="请求设备状态")
    def login3(self, username, pwd):
        self.log += "\n" + str(time.time()) + ":请求设备状态"
        self.log += "\n" + str(time.time()) + "：" + username + "==>" + pwd
        print("设备状态获取成功")

    @pytest.mark.parametrize('username,pwd,tatile', data)
    def test_allure(self, username, pwd, tatile):
        self.login1(username, pwd)
        self.login2(username, pwd)
        self.login3(username, pwd)
        allure.attach(self.log, "log")
        allure.dynamic.story(tatile)
        assert pwd == "123456"
        print(username, pwd)
