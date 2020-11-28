from  Common.read_xls_news import Read_xls
from  Common.write_xls import WriteExcel
from Common.http_request import Request
from  Common.list_dict import Change
from Common.conf import Read_conf
from Conf import Project_path
from Common.log import Logger
import time
from ddt import ddt,feed_data,unpack,data,add_test,_add_tests_from_data

test_data_path= Project_path.TestData_path + "Test_data.xls"
mode_path=Project_path.Conf_path+"interf_TestMode.conf"
http_conf_path=Project_path.Conf_path+"http.conf"
host=Read_conf(http_conf_path).get_value("HTTP","host")
mode=Read_conf(mode_path).get_value("Mode","login_mode")


now = time.strftime('%Y-%m-%d-%H-%M')
row=1
@ddt
class Interfere():
    def __init__(self):
        self.Log=Logger()
        self.r = Read_xls(test_data_path)
        self.writedata = WriteExcel()
    def sheet_books(self):
        self.books = self.r.get_workbook()
        return self.books
    def get_data(self,bookname):
        # self.r = Read_xls(test_data_path)
        # books = self.r.get_workbook()
        test_data=[]
        self.test_datas = self.r.read_data(bookname, 1)
        keys_list = self.r.read_data(bookname, 0)[0]
        if mode == 1:
            Logger().info("[mode:1],本次测试执行基本流测试用例")
            for i in range(len(self.test_datas)):
                if self.test_datas[i][1] == 1:
                    test_data.append(self.test_datas[i])
                    i += 1
                else:
                    continue
        elif mode == 0:
            Logger().info("[mode:0],本次测试执行全部测试用例")
            test_data = self.test_datas
        datas=[]
        datas.append(keys_list)
        datas.append(test_data)
        return datas
    def test_run( self,book_name,test_data,keys_list):
        # 创建表格,建立表头
        self.writedata.creattable(book_name)
        self.header = ["case_num", "explain", "result", "data", "code"]  # 第四个开始设置你需要的值(要和报文字典的key值对应)
        for n in range(len(self.header)):
            self.writedata.write_onlydata(0, n, self.header[n])
        for tdata in test_data:
            global row
            ruselt_path = Project_path.TestResult_path + now + self.__class__.__name__ + ".xls"
            testcase_num = tdata[0]
            explain = tdata[2]
            url = tdata[3]
            type = tdata[4]
            expectation = tdata[5]
            m = 6  # 前面有几个非参数字段这里写几
            data = Change().list_dict(tdata, keys_list, m)
            result = Request(host).request(url, data, type)
            try:
                assert result["code"] == expectation, "与期望值不符"
                test_result = "Pass"
            except Exception as e:
                self.Log.error("第%s条用例[%s]测试失败【%s】" % (testcase_num, explain, e))
                test_result = "Faile"
                raise e
            else:
                self.Log.info("第%s条用例[%s]测试通过" % (testcase_num, explain))
            finally:
                self.writedata.write_onlydata(row, 0, testcase_num)
                self.writedata.write_onlydata(row, 1, explain)
                self.writedata.write_onlydata(row, 2, test_result)
                self.writedata.write_onlydata(row, 3, str(result))
                for h in range(len(self.header)):
                    if self.header[h] in list(result.keys()):
                        self.writedata.write_onlydata(row, h, str(result[self.header[h]]))
                row += 1
                self.writedata.save_excel(ruselt_path)
        row = 1


if __name__=="__main__":
    a=Interfere()
    b=a.sheet_books()
    for bookname in b:
        # a.creat_book(bookname)
        t=a.get_data(bookname)
        k=t[0]
        d=t[1]
        a.test_run(bookname,d,k)


