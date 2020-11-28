import re

def regular(expression,str,n=None):
    if n==None:
        n=1
    pattern=re.compile(expression)
    result=re.findall(pattern,str)
    # result=pattern.findall(str)
    # pipei=pattern.search(str)
    # result=pipei.group(n).strip()
    return result

if __name__=='__main__':
    # a="正确答案：AB   您的答案：未作答"
    # b='：([^"]+)   您'
    # answer=regular(b,a)
    # print(answer)
    # list=[]
    # for each in answer:
    #     list.append(each)
    # print(list)
    # teststr = "mts:'1301765',province:'河南',catName:'中国联通',telString:'13017659465',areaVid:'30500',ispVid:'137815084',carrier:'河南联通'"
    # # teststr=1
    # r='([^?"]+):'
    # result=regular(r,teststr)
    # s="%s"%result
    # print(type("%s"%result))
    # print(result)
    s1="{'mts':'1301765','province':'河南','catName':'中国联通','telString':'13017659465','areaVid':'30500','ispVid':'137815084','carrier':'河南联通'}"
    r1="{(.+?):|,(.+?):"
    result1=regular(r1,s1)
    print(result1)

    result2 = re.findall(r1, s1)
    # result1=regular(r1,s1)
    print(result2)

