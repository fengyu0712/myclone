import pytest
from  selenium import  webdriver
from Common.conf import Read_conf
from Common.log import Logger
from Conf import Project_path
conf_path=Project_path.Conf_path+"Web.conf"
url = Read_conf(conf_path).get_value( "BID", "url")

@pytest.fixture(scope='class')
def Web_driver_class():
    driver = webdriver.Chrome()
    Logger().info("测试开始了！")
    yield driver
    driver.close()
    driver.quit()
    Logger().info("测试结束了!")

@pytest.fixture(scope='function')
def Web_driver():
    Web_driver_class.get(url)
    # handle = self.driver.current_window_handle
    # self.driver.switch_to_window(handle)
    Web_driver_class.get(url)
    yield
    pass
