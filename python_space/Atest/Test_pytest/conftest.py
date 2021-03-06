import pytest
import allure
import yaml
from  selenium import  webdriver
from Common.conf import Read_conf
from Common.log import Logger
from Conf import Project_path
conf_path=Project_path.Conf_path+"Web.conf"
env_conf=Project_path.Conf_path+"env_config.yml"

url = Read_conf(conf_path).get_value( "BID", "url")

@pytest.fixture(scope="session", autouse=True)
# def env(request):
#     """
#     Parse env config info
#     """
#     root_dir = request.config.rootdir
#     # config_path = 'E:\python_space\Conf\env_config.yml'.format(root_dir)
#     # with open(config_path,encoding='utf-8') as f:
#     #     env_config = yaml.load(f) # 读取配置文件
#     allure.environment(host='123') # 测试报告中展示host
#     allure.environment(browser='456') # 测试报告中展示browser
#
#     return env_config

@pytest.fixture(scope='class')
def Web_driver_class():
    driver = webdriver.Firefox()
    Logger().info("测试开始了！")
    yield driver
    # driver.close()
    driver.quit()
    Logger().info("测试结束了!")

@pytest.fixture()
def Web_driver(Web_driver_class):
    Web_driver_class.get(url)
    # handle = self.driver.current_window_handle
    # self.driver.switch_to_window(handle)
    Web_driver_class.get(url)
    yield
    pass
