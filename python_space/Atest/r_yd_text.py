from Common.read_txt import ReadDatadet
from Common.write_xls import WriteExcel

infile='E:\python_space\TestCase\yidian2.0.4页面事件埋点.txt'
data=ReadDatadet(infile)
xls_path='E:\yidian.xls'
sheet_name='埋点'
w=WriteExcel()
w.creattable(sheet_name)
for i in range(len(data)):
    w.write_linedata(i,data[i])
w.save_excel(xls_path)


