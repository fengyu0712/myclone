import xlrd
from Conf import Project_path

from  Common.log import Logger
# path='E:/python2/u_test/excel/test.xls'
#
# workbook=xlrd.open_workbook(path)  #打开表格
#
# shell_obj=workbook.sheet_by_index(0)  #定位表单
# shell_obj1=workbook.sheet_by_name("me")
#
# ncol=shell_obj.ncols  #行数
# nrow=shell_obj.nrows   #列数
# print(nrow,ncol)
#
# row_value=shell_obj.row_values(2)
# print(row_value)
# cell_values=shell_obj.cell_value(0,0)
# print(cell_values)

class Read_xls():
    def read_data(self,filepath,booknum=None):
        if booknum is None:
            booknum=0
        result=[]
        workbook = xlrd.open_workbook(filepath)
        shell_obj = workbook.sheet_by_index(booknum)
        nrow=shell_obj.nrows
        for i in  range(0,nrow):
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
    a=Read_xls().read_data(test_data,1)
    print(a)







