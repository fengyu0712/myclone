import os,re

import jsonpath

path=r"F:\git\myclone\AITEST\testcase\TestAiyunNew\1.txt"
def read_data(path):
    data=[]
    with open(path,"r",encoding='utf8') as f:
        for line in f.readlines():
            # print(line)
            data0=line.replace('\n','').split(',')
            data.append(data0)
    return data

def write_data(path,str):
    with open(path, "a+", encoding='utf8') as f:
        f.write(str)
        f.close()

if __name__ == '__main__':
    # data="4,5,6,7"
    # write_data(path,'\n'+data)
    print(read_data(path))


