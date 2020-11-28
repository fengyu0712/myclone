import  xlwt
class WriteExcel:
    def __init__(self):
        self.wb = xlwt.Workbook()
    def creattable(self,sheet_name):
        self.sheet=self.wb.add_sheet(sheet_name)
    def write_onlydata(self,row,col,vale):
        self.sheet.write(row,col,vale)
    def write_linedata(self,row,list_data):
        for i in range(len(list_data)):
            self.write_onlydata(row,i,list_data[i])
    def save_excel(self,path):
        self.wb.save(path)

if __name__=='__main__':
    w=WriteExcel()
    path1 = 'F:/python2/u_test/excel/test5.xls'
    a=['112','113','114','115']
    b='test'
    w.creattable(b)
    w.write_linedata(1,a)
    # for i in range(len(a)):
    #     w.write_onlydata(i,i,a[i])
    w.save_excel(path1)
