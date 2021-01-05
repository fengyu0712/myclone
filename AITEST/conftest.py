import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
print(curPath)
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import pytest
from common.conf import Conf
import Project_path

allure_result=os.path.join(Project_path.TestResult_path,"allure_result")
env_conf_path = os.path.join(Project_path.conf_path, "environment.properties.ini")
allure_conf_path=os.path.join(allure_result,"environment.properties")


# 添加命令行参数
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        # default: 默认值，命令行没有指定host时，默认用该参数值
        default="PRO",
        help="test case project host address"
    )


@pytest.fixture(scope="session", autouse=True)
def host(request):
    '''获取命令行参数'''
    # 获取命令行参数给到环境变量
    env = request.config.getoption("--env").upper()
    test_host = Conf(env_conf_path).get_value(env, "test_host")
    print(f"当前用例运行测试环境:{test_host}")
    os.environ["host"] = test_host
    updata_allure_env(env,test_host)

def updata_allure_env(env,testhost):
   '''
   同步环境信息到allure报告上
   :param env: 当前环境
   :param testhost: 当前测试HOST
   :return:
   '''
   with open(allure_conf_path, "a") as f:
       f.write(f"ENVIRONMENT={env}\n")
       f.write(f"HOST={testhost}\n")

