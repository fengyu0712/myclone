__author__ = 'Administrator'
from  Common.read_xls import Read_xls
from  Common.write_xls import WriteExcel
from Common.http_request import Request
from  Common.list_dict import Change
from Common.conf import Read_conf
from Conf import Project_path
from Common.mysql import MySql
from Common.log import Logger
from Common import globalvar as gl
import time,unittest,pytest,allure
from ddt import ddt,data
from TestCase.InterFere_Test.new import test_Login

test_data_path= Project_path.TestData_path + "Test_data1.xls"
mode_path=Project_path.Conf_path+"interf_TestMode.conf"
http_conf_path=Project_path.Conf_path+"http.conf"
host=Read_conf(http_conf_path).get_value("HTTP","host")
mode=Read_conf(mode_path).get_value("Mode","login_mode")
conf_path=Project_path.Conf_path+"db.conf"
config=Read_conf(conf_path).get_value("Mysql","config")
sql=MySql(config)
datas= Read_xls().read_data(test_data_path,booknum=1) #默认读取第一个表格
keys_list = datas[0]
test_data=[]
if mode == 1:
    Logger().info("[mode:1],本次测试执行基本流测试用例")
    for i in range(len(datas)):
        if datas[i][2] == 1:
            gl._init()
            uid=gl.get_value('uid')
            print(uid)
            datas[i][9]=gl.get_value('uid')
            test_data.append(datas[i])
            i += 1
        else:
            continue
elif mode == 0:
    Logger().info("[mode:0],本次测试执行全部测试用例")
    test_data = datas[1:]