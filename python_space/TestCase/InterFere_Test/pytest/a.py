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
            # gl._init()
            # uid=gl.get_value('uid')
            # print(uid)
            # datas[i][9]=gl.get_value('uid')
            test_data.append(datas[i])
            i += 1
        else:
            continue
elif mode == 0:
    Logger().info("[mode:0],本次测试执行全部测试用例")
    test_data = datas[1:]


#创建表格,建立表头
writedata = WriteExcel()
writedata.creattable("result")
header=["case_num","explain","result","data","code"]  #第四个开始设置你需要的值(要和报文字典的key值对应)
for n in range(len(header)):
    writedata.write_onlydata(0, n, header[n])
now = time.strftime('%Y-%m-%d-%H-%M-%S')
test_data=[[1, 1, 1, '正常查看', '/api/user/mission/list', 'get', 'code', 0, 1, 441456]]
print(test_data)
@pytest.mark.parametrize(('tdata'), test_data)
def test_run(self, tdata):
    ruselt_path = Project_path.TestResult_path + now +  ".xls"
    caseid = int(tdata[0])
    testcase_num = tdata[1]
    explain = tdata[3]
    url = tdata[4]
    type = tdata[5]
    comparison_key = tdata[6]
    if tdata[7] == 0:
        expectation = tdata[8]
    elif tdata[7] == 1:
        expectation = sql.read_data(tdata[8])
    else:
        return "sql类型错误"
    m = 9  # 前面有几个非参数字段这里写几
    data = Change().list_dict(tdata, keys_list, m)
    result = Request(host).request(url, data, type)
    try:
        self.assertEqual(str(result[comparison_key]), str(expectation), "与期望值不符")
        test_result = "Pass"
    except Exception as e:
        self.Log.error("第%s条用例[%s]测试失败【%s】" % (testcase_num, explain, e))
        test_result = "Faile"
        raise e
    else:
        self.Log.info("第%s条用例[%s]测试通过" % (testcase_num, explain))

if __name__ == "__main__":
    pytest.main(["-v"])