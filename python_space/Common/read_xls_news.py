import xlrd
from Conf import Project_path

from  Common.log import Logger

class Read_xls():
    def __init__(self,filepath):
        self.workbook = xlrd.open_workbook(filepath)

    def get_workbook(self):
        booknames=self.workbook.sheet_names()
        return booknames
    def read_data(self,bookname=None,start_line=None):  #start_line 数据起止行
        if start_line==None:
            start_line=0
        if bookname==None:
            bookname=self.get_workbook()[0]
        result=[]
        shell_obj = self.workbook.sheet_by_name(bookname)
        nrow=shell_obj.nrows
        for i in  range(start_line,nrow):
            try:
                row_value=shell_obj.row_values(i)
                row_values=[]
                for each in  row_value:
                    if isinstance(each,float):
                        each=int(each)
                    else:
                        each=each
                    row_values.append(each)
                result.append(row_values)
            except Exception as  e:
                Logger().error(e)
        return result

if __name__=="__main__":
    test_data = Project_path.TestData_path + "Test_data.xls"
    r=Read_xls(test_data)
    a = r.read_data()
    print(a)
    # a=r.get_workbook()
    # for each in a:
    #     bookname=each
    #     b=r.read_data(bookname,1)
    #     print(b)








