import threading
from  selenium import  webdriver
from time import sleep, ctime
class C_Driver():
    def driver(self,browser=None):
        print('start:%s' % ctime())
        print('browser:%s,' % browser)
        if browser ==None:   #默认谷歌浏览器
           driver = webdriver.Chrome()
        elif  browser == "Chrome":
           driver = webdriver.Chrome()
        elif browser == 'Firefox':
            driver = webdriver.Firefox()
        else:
            print("browser 参数有误，只能为Firefox和chrome")
        return driver
if __name__ == '__main__':
    # T_browser().baidu('chrome')


    # 启动参数（指定浏览器与百度收缩内容）
    list = ['chrome', 'Firefox']
    threads = []
    files = range(len(list))

    # 创建线程
    for b_name in list:
        t = threading.Thread(target=C_Driver().driver(b_name))
        threads.append(t)
    # 启动线程
    for t in files:
        threads[t].start()
    for t in files:
         threads[t].join()
    print('end:%s' % ctime())