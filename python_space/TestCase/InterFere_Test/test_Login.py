__author__ = 'Administrator'
from Common.read_xls import Read_xls
from Common.write_xls import WriteExcel
from Common.http_request import Request
from Common.list_dict import Change
from Common.conf import Read_conf
from Conf import Project_path
from Common.log import Logger
import sys,time,unittest,pytest,allure
from ddt import ddt,data

test_data_path= Project_path.TestData_path + "Test_data.xls"
mode_path=Project_path.Conf_path+"interf_TestMode.conf"
http_conf_path=Project_path.Conf_path+"http.conf"
host=Read_conf(http_conf_path).get_value("HTTP","host")
mode=Read_conf(mode_path).get_value("Mode","login_mode")
datas= Read_xls().read_data(test_data_path,booknum=0) #默认读取第一个表格
keys_list = datas[0]
test_data=[]
if mode == 1:
    Logger().info("[mode:1],本次测试执行基本流测试用例")
    for i in range(len(datas)):
        if datas[i][2] == 1:
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
header=["case_num","explain","result","data"]  #第四个开始设置你需要的值(要和报文字典的key值对应)
for n in range(len(header)):
    writedata.write_onlydata(0, n, header[n])
now = time.strftime('%Y-%m-%d-%H-%M-%S')
@ddt
@allure.feature('登录功能接口')
class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Log=Logger()
        Logger().info("%s测试开始:" % __class__.__name__ )
        # cls.Log=Log
    @classmethod
    def tearDownClass(cls):
        cls.Log.info("%s测试结束!" % __class__.__name__)

    @data(*test_data)
    def test_run(self,tdata):
        ruselt_path = Project_path.TestResult_path +now + self.__class__.__name__ + ".xls"
        caseid=int(tdata[0])
        testcase_num = tdata[1]
        explain=tdata[3]
        url = tdata[4]
        type = tdata[5]
        expectation=tdata[6]

        m=7  #前面有几个非参数字段这里写几
        data=Change().list_dict(tdata,keys_list,m)
        result=Request(host).request(url,data,type)
        try:
            self.assertEqual(result["code"],expectation,"与期望值不符")
            test_result = "Pass"
        except Exception as e:
            self.Log.error("第%s条用例[%s]测试失败【%s】" % (testcase_num,explain,e))
            test_result = "Faile"
            raise e
        else:
            self.Log.info("第%s条用例[%s]测试通过" %(testcase_num,explain))
        finally:
            writedata.write_onlydata(caseid, 0, testcase_num)
            writedata.write_onlydata(caseid, 1, explain)
            writedata.write_onlydata(caseid, 2, test_result)
            writedata.write_onlydata(caseid, 3, str(result))
            for each  in list(result.keys()):
                 if each  not in header:
                    header.append(each)
                    writedata.write_onlydata(0, header.index(each), each)
            for each in list(result.keys()):
                # print(str(result[each])
                writedata.write_onlydata(caseid, header.index(each), str(result[each]))
            writedata.save_excel(ruselt_path)


if __name__=="__main__":
    pytest.main(*sys.argv[1:])






