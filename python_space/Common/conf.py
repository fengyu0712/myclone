import configparser
import os
import sys
class Read_conf:
    def __init__(self,path):
        self.cf = configparser.ConfigParser()
        self.cf.read(path, encoding='utf-8')
    def get_value(self,section,option):
        value=self.cf.get(section,option)
        return eval(value)
    #eval 自动转换返回类型
    def get_int(self,section,option):
        value=self.cf.getint(section,option)
        return value


# if __name__=='__main__':
#     mm = {"a": 1, "b": 2}
#     print(type(mm))
#     section="Path"
#     option="projectfail"
#     path="E:\python_space\Conf\project_path.conf"
#     print(type(path))
#     m=Read_conf(path).get_value(section,option)
#     print(type(m),m)