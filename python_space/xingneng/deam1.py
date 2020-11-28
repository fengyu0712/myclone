#!/usr/bin/env python
# coding:utf-8
import paramiko
import numpy as np
import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates
from numpy import datetime64
from itertools import islice
import re,os,time,shutil,logging
import threading,os


# path=os.getcwd()
data_path=os.path.join(os.getcwd(),"data")
# print(path)
pic_path=os.path.join(os.getcwd(),"picture")

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='parallel_test.log',
                filemode='w')

host1={"ip":"111.231.233.115",'port':2170,"username":"fengyu0712","passwd":"Li_121193252"}
# host2={"ip":"192.1689.1.102",'port':22,"username":"app","passwd":"pwd"}

#将host添加到HOST中进行监控
HOST=[host1]
def ssh2(host,cmd):
    result=[]
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        logging.info("connect to "+host['ip']+",user "+host['username']+",ssh")
        ssh.connect(host['ip'],int(host['port']),host['username'],host['passwd'],timeout=5)
        for m in cmd:
            logging.info(m)
            stdin,stdout,stderr = ssh.exec_command(m)
            out = stdout.readlines()
            #return out
            for o in out:
                logging.info(o)
                result.append(o)
        ssh.close()
    except Exception as e:
        logging.DEBUG(e)
    return out

#sftp,默认从对端home目录获取，放到本地当前目录
def sftpfile(host,getfiles,putfiles):
    try:
        logging.info("connnect to "+host['ip']+",user "+host['username']+",sftp")
        t=paramiko.Transport((host['ip'],int(host['port'])))
        t.connect(username=host['username'],password=host['passwd'])
        sftp =paramiko.SFTPClient.from_transport(t)
        if getfiles != None:
            for file in getfiles:
                logging.info("get "+file)
                file=file.replace("\n", "")
                sftp.get(file,file)
        if putfiles != None:
            for file in putfiles:
                file=file.replace("\n", "")
                logging.info("put "+file)
                sftp.put(file,file)
        t.close()
    except:
        import traceback
        traceback.print_exc()
        try:
            t.close()
        except Exception as e:
            logging.DEBUG(e)

def getmem():
    global host
    script='''
    #!/bin/bash
while true
`    do
        free|awk '/Mem/{print  '"/"$(date +%Y-%m-%d" "%T)/""'","$2/$3}'
        sleep 5
    done
    '''
    file_script = open('getmem.sh', 'w')
    file_script.write(script)
    file_script.close( )
    logging.info("monitor memory by shell script: getmem.sh")
    logging.info(script)
    for host in HOST:
        sftpfile(host,None,['getmem.sh'])

#测试完成后清理sar iostat,和获得cpu数据脚本进程。并加工结果文件。
def teardownps():
    cmd = ['killall sar',
           "ps -ef|grep getmem|grep -v grep|awk '{print $2}'|xargs kill -9",
           "df -h|awk '{print $4\",\"$5\",\"$6}' > ~/diskend.$(hostname).txt",
#           'df -h > ~/disk_end$(hostname).txt',
           'killall iostat',
           'sed -i -e "s/all//g" -e "/CPU/d" -e "/^$/d"  -r -e "s/\s{2,}/,/g" -e  "s/^/$(date +%Y-%m-%d) /g" cpu*.txt',
           'sed -i -e "/^$/d" -r -e "s/\s{2,}/,/g" -e  "s/^/$(date +%Y-%m-%d) /g" net*.txt']
    for host in HOST:
        ssh2(host,cmd)

#获取结果文件
def getresult():

    global data_path
    data_path=os.path.join(os.getcwd(),"data")
    for host in HOST:
        resultfile=ssh2(host,['ls cpu*.txt mem*.txt disk*.txt io*.txt net*.txt'])
        sftpfile(host,resultfile,None)
        for f in resultfile:
            f=f.replace("\n", "")
            shutil.move(f,data_path)


#使用sar，iostat和脚本获取性能数据
def monitor():
    getmem()
    os.environ["LC_TIME"]="POSIX"
    cmd = [
           'nohup sar 2 > ~/cpu$(hostname).txt &',
           'chmod u+x getmem.sh','nohup ~/getmem.sh >~/mem$(hostname).txt &',
           "df -k|awk '{print $4\",\"$5\",\"$6}' > ~/diskinit.$(hostname).txt",
#           'df -h > ~/disk_init$(hostname).txt',
           'nohup iostat -d -x -k 3 >~/io$(hostname).txt &',
           "nohup sar -n DEV 3 > ~/net$(hostname).txt &"]
    for host in HOST:
        ssh2(host,cmd)

def showCPU():
    global data_path,pic_path
    cpuindex=['time','user','nice','system','iowait','steal','idle']
    pattern = re.compile(r'cpu.*.txt')
    for cpudatafile in os.listdir(data_path):
        match = pattern.match(cpudatafile)
        if match:
            logging.info("handle "+cpudatafile)
            #通过numpy.genfromtxt加载数据
            cpudata=np.genfromtxt(fname=os.path.join(data_path,cpudatafile),
                          names=cpuindex,
                          dtype='S19,float,float,float,float,float,float',
                          delimiter=",")
            logging.info(cpudata)
            pic=0
            plt.figure(figsize=(8,12)) #指定图像大小
            for index in cpuindex:
                pic+=1
                if pic==1:
                    testime=cpudata[index].astype(datetime64).copy() #转换时间类型
                if pic>1:
                    logging.info("draw "+cpudatafile.split(".")[0]+" "+index+" ..................................")
                    plt.sca(plt.subplot(len(cpuindex),1,pic))
                    plt.setp(plt.xticks()[1], rotation=30, ha='right')
                    plt.subplots_adjust(left=0.08, right=0.95, wspace=0.25, hspace=1.10)
                    plt.plot(testime,cpudata[index], color='r', linewidth=1)
                    plt.xlabel("time:s")
                    plt.ylabel(index+":%")
                    plt.title("CPU used(%): "+index)
            logging.info("save the picture to "+os.path.join(pic_path,cpudatafile.split(".")[0]+".jpg"))
            plt.savefig(os.path.join(pic_path,cpudatafile.split(".")[0]+".jpg")) #保存图像
            plt.close()   #必须close，否则会缓存到下个图像中

#测试用例
import requests
def testcase():
    url="http://bkt.jeagine.com/api/user/signin"
    data = {'account': '130000000000', 'appKey': 'all', 'category_id': 80, 'password': 123456, 'terminal': 2}
    # print("第%s次请求"%n)
    try:
        requests.get(url, data)
    except Exception as e:
        print(e)
    else:
        print("请求成功")



class testThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self,runtimer,duration=None):
        threading.Thread.__init__(self)
        # self.testpath=testpath
        self.runtimer=runtimer
        self.duration=duration

    def run(self):
        #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        #测试场景。把若干个测试用例加到里面组成测试场景。如果duration为None，则表示一次性并发。
        #否则为持续并发测试。持续时间duration单位为秒。
        # suite = unittest.TestSuite()
        # TestResult=unittest.TestResult()
        logging.info("run...............................................")
        logging.info("running times: "+str(self.runtimer))
        logging.info("running last(seconds): "+str(self.duration))
        # logging.info("running testpath: "+str(self.testpath))
        # CreateSuite(self.testpath)
        # for testcase in self.testpath:
        #     suite.addTest(test_login1.LoginTest(testcase))
        if self.duration==None:
            for timer in range(self.runtimer):
                testcase()
                timer = timer + 1
                # suite.run(TestResult)
        else:
            startime=time.mktime(time.localtime())
            cost=0
            while cost<=self.duration:
                for timer in range(self.runtimer):
                    timer=timer+1
                    testcase()
                    # suite.run(TestResult)
                endtime=time.mktime(time.localtime())
                cost=endtime-startime
                print(startime,endtime,cost)
                # timer=1

        # passrate=100-len(TestResult.failures)/TestResult.testsRun*100
        #
        # logging.info("fail the test: "+str(TestResult.failures))
        # logging.info("total fail: "+str(len(TestResult.failures)))
        # logging.info("total run: "+str(TestResult.testsRun))
        # logging.info("TestCases Pass Rate: "+str(passrate)+"%")


if __name__ == "__main__":
    if not os.path.exists("./picture"):
        os.mkdir("./picture")

    if not os.path.exists("./data"):
        os.mkdir("./data")
    else:
        os.rename("data","data"+time.strftime("%Y%m%d%H%M%S", time.localtime()))
        os.mkdir("./data")
    #定义测试用例，组成一个测试场景
    # testscene1=['testcase1','testcase2']
    #testscene1=['testcase3']
    # testscene2=['testcase2','testcase3']
    # testpath="E:\python_space/xingneng/test_login1.py"
    # testpath=['testlogin']
    #利用线程进行并发测试，三个参数分别表示测试场景、并发次数和持续时间，None表示一次并发
    thread1 = testThread(10)
    # thread2 = testThread(testscene2,100,100)

    monitor()
    thread1.start()
    thread1.join()
    teardownps()
    getresult()


    showCPU()
