class Assert():
    def equalvalue(self,realvalue,exceptvalue):
        assert realvalue == exceptvalue


    # exceptvalue: Ԥ�ڽ��
    # realvalue ʵ�ʽ��
    def containvalue(self,realvalue,exceptvalue):
        print(exceptvalue,realvalue)
        print(type(exceptvalue))
        print(exceptvalue.find(realvalue)!=-1)
        assert exceptvalue.find(realvalue)!=-1

