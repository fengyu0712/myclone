__author__ = 'Administrator'
from Common.read_xls import Read_xls
from  Common.write_xls import WriteExcel
from Common.http_request import Request
from  Common.list_dict import Change
from Conf import Project_path
from Common.log import Logger
from Common.conf import Read_conf
import time


class Login:
    def __init__(self,test_data_path,mode):
        data=Read_xls().read_data(test_data_path) #默认读取第一个表格
        self.keys_list=data[0]
        self.test_data=[]
        if mode==1:
            Logger().info("[mode:1],本次测试执行基本流测试用例")
            for i in range(1,len(data)):
                if data[i][1]==1:
                    self.test_data.append(data[i])
                    i+=1
                else:
                    continue
        elif mode==0:
            Logger().info("[mode:0],本次测试执行全部测试用例")
            self.test_data=data[1:]
        now = time.strftime('%Y-%m-%d-%H-%M-%S')
        global ruselt_path
        ruselt_path=Project_path.TestResult_path+now+self.__class__.__name__+".xls"
        self.writedata = WriteExcel()
        self.writedata.creattable("result")
    def runLogin(self,host):
        header=["case_num","explain","result","data","code"]  #第五个开始设置你需要的值(要和报文字典的key值对应)
        for n in range(len(header)):
            self.writedata.write_onlydata(0, n, header[n])
        for i in range(len(self.test_data)):
            list_data = self.test_data[i]
            testcase_num = self.test_data[i][0]
            expalin = self.test_data[i][2]
            url = self.test_data[i][3]
            type = self.test_data[i][4]
            expectation=self.test_data[i][5]
            m=6   #前面有几个非参数字段这里写几
            data=Change().list_dict(list_data,self.keys_list,m)
            result=Request(host).request(url,data,type)
            try:
                assert int(result["code"])==expectation,"结果与期望不一致"
                test_result = "Pass"
            except Exception as e:
                Logger().error("第%s条用例[%s]测试失败【%s】" % (testcase_num,expalin,e))
                test_result="Falie"
            else:
                Logger().info("第%s条用例[%s]测试通过" %(testcase_num,expalin))
            finally:
                self.writedata.write_onlydata(i+1, 0, testcase_num)
                self.writedata.write_onlydata(i+1, 1, expalin)
                self.writedata.write_onlydata(i+1, 2, test_result)
                self.writedata.write_onlydata(i+1, 3, str(result))
                for h in range(len(header)):
                    if header[h] in list(result.keys()):
                        self.writedata.write_onlydata(i+1, h, str(result[header[h]]))
        Logger().info("测试用例执行完成")
        self.writedata.save_excel(ruselt_path)
        Logger().info("测试结果写入[%s]成功"%ruselt_path)



test_data= Project_path.TestData_path + "Test_data.xls"
mode_path=Project_path.Conf_path+"interf_TestMode.conf"
http_conf_path=Project_path.Conf_path+"http.conf"
host=Read_conf(http_conf_path).get_value("HTTP","host")
mode=Read_conf(mode_path).get_value("Mode","login_mode")
if __name__ == '__main__':
    a=Login(test_data,mode).runLogin(host)







