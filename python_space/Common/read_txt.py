def ReadDatadet(infile):
    f=open(infile,'r',encoding='utf-8')
    sourceInLine=f.readlines()
    dataset=[]
    for line in sourceInLine:
        temp1=line.strip('\n')
        temp2=temp1.split(',')
        dataset.append(temp2)
    return dataset
if __name__=="__main__":
    infile='E:\python_space\TestCase\yidian2.0.4页面事件埋点.txt'
    data=ReadDatadet(infile)
    print(data)