from selenium import webdriver
 # 测试用例
from time import sleep, ctime
import threading
class T_browser():
    def baidu(self,b_name=None):
        print('start:%s' % ctime())
        print('browser:%s,' % b_name)
        if b_name ==None:
           driver = webdriver.Chrome()
        elif  b_name == "chrome":
           driver = webdriver.Chrome()
        elif b_name == 'ff':
            driver = webdriver.Firefox()
        else:
            print("browser 参数有误，只能为Firefox和chrome")
        driver.get("http://www.baidu.com")
        sleep(2)
        driver.close()
if __name__ == '__main__':
    # T_browser().baidu('chrome')


    # 启动参数（指定浏览器与百度收缩内容）
    list = [ 'chrome','ff']
    threads = []
    files = range(len(list))

    # 创建线程
    for b_name in list:
        t = threading.Thread(target=T_browser().baidu(b_name))
        threads.append(t)
    # 启动线程
    for t in files:
        threads[t].start()
    for t in files:
         threads[t].join()
    print('end:%s' % ctime())