from Common.read_xls_news import Read_xls
from Common.mysql import MySql
from Common.conf import Read_conf

yidian="E:/python_space/1test/yidian.xls"

r_xls=Read_xls(yidian)
data=r_xls.read_data()
print(data)
yidian_db="E:/python_space/1test/yidian.conf"
config=Read_conf(yidian_db).get_value("YiDian","config")

sql1 = "INSERT INTO bp_event_copy VALUES(%s,%s,%s,'2018-05-23 13:51:56',%s,%s)"
sql2="Select * from bp_event"
MySql(config).insert_manydata(sql1,data)
a=MySql(config).read_data(sql2)
print(a[-1])

# for each in data:
#     sql="INSERT INTO bp_event VALUES(%s,%s,%s,'2018-05-23 13:51:56',%s,%s)"
#     MySql(config).insert_data(sql,tuple(each))
