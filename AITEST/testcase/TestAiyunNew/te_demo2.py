import allure
import pytest
import time
import os

path=r"F:\git\myclone\AITEST\testcase\TestAiyunNew\1.txt"
def read_data(path):
    data=[]
    with open(path,"r",encoding='utf8') as f:
        for line in f.readlines():
            # print(line)
            data0=line.replace('\n','').split(',')
            data.append(data0)
    # global data
    return data

def write_data(path,str):
    with open(path, "a+", encoding='utf8') as f:
        f.write('\n'+str)
        f.close()

class TestDemo2:
    write_data(path, str)
    def setup_class(cls):
        str="1,2,3,4"

        # global data
        # data=read_data(path)

    @pytest.mark.parametrize('casenum,wavfail,asr,case', read_data(path))
    def test(self,casenum,wavfail,asr,case):
        print(casenum,wavfail,asr,case)
