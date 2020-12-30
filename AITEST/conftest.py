import os
import pytest
# 添加命令行参数
def pytest_addoption(parser):
    parser.addoption(
        "--cmdhost",
        action="store",
        # default: 默认值，命令行没有指定host时，默认用该参数值
        default="ws://linksit.aimidea.cn:10000",
        help="test case project host address"
    )

# autouse=True自动执行该前置操作
@pytest.fixture(scope="session", autouse=True)
def host(request):
    '''获取命令行参数'''
    # 获取命令行参数给到环境变量
    os.environ["host"] = request.config.getoption("--cmdhost")
    print("当前用例运行测试环境:%s"%os.environ["host"])