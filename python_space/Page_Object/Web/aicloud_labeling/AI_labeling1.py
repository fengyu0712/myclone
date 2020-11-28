import os, sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.dirname(os.path.dirname(os.path.dirname(curPath)))
sys.path.append(rootPath)  # 获取绝对路径，以便shell脚本跑
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import time, json, urllib3, requests

url = "http://aicloud-labeling.midea.com/login"
login_account = "ys0004"
password = "123456"

account_location = "//input[@name='username']"
password_location = "//input[@name='password']"
login_button_location = "//span[text()='登录']/.."

login_labeling = "//a[text()='202006ASR文本标注0722']"
continue_ys = "//button[@class='el-button el-button--primary el-button--small button']"
start_ys = "//span[text()='开始验收']/.."
YES = "//span[text()='确定']"

# 加载启动项

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)  #禁止加载图片
chrome_options.add_argument('headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)



asr_location = "//p[@class='markStrC']"
classifier_location = "//div[@class='dt_dropDown field']/p"

select_location = "//div[@class='examiner']//div[text()='%s']"
# driver = webdriver.Chrome(options=chrome_options,desired_capabilities=capabilities)

# print(driver.page_source)
n1 = 0


def login(account, password):
    global n1
    try:
        WebDriverWait(driver, 5, 0.2).until(EC.visibility_of_element_located((By.XPATH, account_location)))
    except Exception as e:
        if n1 > 3:
            driver.quit()
            raise e
        else:
            print(n1)
            n1 += 1
            driver.refresh()
            login(account, password)
    else:
        driver.find_element_by_xpath(account_location).clear()
        driver.find_element_by_xpath(account_location).send_keys(account)
        driver.find_element_by_xpath(password_location).send_keys(password)
        driver.find_element_by_xpath(login_button_location).click()


def into_ys():
    try:
        WebDriverWait(driver, 10, 0.5).until(EC.visibility_of_element_located((By.XPATH, login_labeling)))
        print("登录成功")
    except Exception as e:
        print("登录异常:%s" % e)
        raise e
    try:
        WebDriverWait(driver, 5, 0.2).until(EC.element_to_be_clickable((By.XPATH, login_labeling)))
    except Exception as e:
        driver.quit()
        raise e
    else:
        driver.find_element_by_xpath(login_labeling).click()
        print("点击任务详情按钮")
    try:
        WebDriverWait(driver, 10, 0.2).until(EC.element_to_be_clickable((By.XPATH, start_ys)))
    except Exception as e:
        driver.quit()
        raise e
    else:
        driver.find_element_by_xpath(start_ys).click()
        print("点击开始验收按钮")

    try:
        WebDriverWait(driver, 10, 0.2).until(EC.element_to_be_clickable((By.XPATH, YES)))
    except Exception as e:
        driver.quit()
        raise e
    else:
        driver.find_element_by_xpath(YES).click()
        print("点击确定按钮")

    # 得到selenium打开的浏览器的所有句柄
    time.sleep(5)
    all_hand = driver.window_handles
    # 切换句柄
    driver.switch_to_window(all_hand[-1])
    print("切换到验收页面")


def get_asr():
    keys = {"通用领域": 'publicDomain', "美的领域": 'mideaDomain'}
    try:
        WebDriverWait(driver, 5, 0.2).until(EC.element_to_be_clickable((By.XPATH, asr_location)))
    except Exception as e:
        raise e
    else:
        asr = driver.find_element_by_xpath(asr_location).text
        classifier = driver.find_element_by_xpath(classifier_location).text.split("-")[0]
    asr_result = {'asr': asr, 'classifier': keys.get(classifier)}
    return asr_result


def myrequests(url, data, type, headers=None, cookies=None):
    if headers == None and type.upper() == "POST":
        headers = {"Content-Type": "application/json"}
    if cookies == None:
        cookies = ""
    if type.upper() == "GET":
        try:
            urllib3.disable_warnings()
            response = requests.get(url, params=data, headers=headers, cookies=cookies,
                                    verify=False)  # https verify=False
            status_code = response.status_code
        except Exception as  e:
            print(e)
        else:
            if status_code == 200:
                print(u"%s请求成功" % url)
            else:
                print("请求出错【status:%s】" % status_code)
            return response
    elif type.upper() == "POST":
        try:
            urllib3.disable_warnings()
            response = requests.post(url, data=json.dumps(data), headers=headers, cookies=cookies,
                                     verify=False)  # https verify=False
            status_code = response.status_code
        except Exception as  e:
            print(e)
        else:
            if status_code == 200:
                print(u"%s请求成功" % url)
            else:
                print(u"请求出错【status:%s】" % status_code)
            return response
    else:
        print(u"请求类型错误")


def nlu(asr):
    url = "https://nlu.sit.aimidea.cn:22012/nlu/v1"
    data = {"currentUtterance": asr, "sourceDevice": "", "multiDialog": "false", "slotMiss": "false",
            "suite": ["default"], "deviceId": "9049230323909912", "userGroup": "meiju",
            "userGroupCredential": "b82063f4-d39b-4940-91c3-5b67d741b4d3", "customDeviceNames": "",
            "customRoomNames": ""}
    try:
        response = myrequests(url, data, "post")
    except Exception as e:
        response=e
    return response


#设置超时输入默认合格

def ys():
    result = {"0": '合格', "1": '不合格'}
    try:
        WebDriverWait(driver, 3, 0.2).until(EC.element_to_be_clickable((By.XPATH, asr_location)))
    except:
        print("等待超时，重新刷新页面")
        driver.refresh()
        ys()
    else:
        asr = get_asr()
        print(asr)
        print("当前验收语料：【%s】,标记人员执行结果是：【%s】" % (asr.get('asr'), asr.get('classifier')))
        nlu_result = nlu(asr.get('asr')).text
        print("当前验收语料：【%s】的NLU分类器结果是：%s" % (asr.get('asr'), json.loads(nlu_result)['classifier']))
        result_key = '0'
        try:
            assert json.loads(nlu_result)['classifier'] == asr.get('classifier')
        except:
            error_path = "D:\\Users\lijq36\Desktop\error.txt"
            with open(error_path, 'a+') as f:
                f.write("【%s】  NLU分类器结果是：【%s】人工标注是【%s】 \n " % (
                    asr.get('asr'), json.loads(nlu_result)['classifier'], asr.get('classifier')))
            result_key = input("【%s】  NLU分类器结果是：【%s】人工标注是【%s】，请人工判断（0：合格，1：不合格）：" % (
                asr.get('asr'), json.loads(nlu_result)['classifier'], asr.get('classifier')))

            from threading import Thread
            def timeerInput():
                input("【%s】  NLU分类器结果是：【%s】人工标注是【%s】，请人工判断（0：合格，1：不合格）：" % (
                    asr.get('asr'), json.loads(nlu_result)['classifier'], asr.get('classifier')))

            result_key = Thread(target=timeerInput)
            result_key.daemon = True
            result_key.start()
            time.sleep(10)
        finally:
            if result_key != "1":
                result_key = "0"
            try:
                WebDriverWait(driver, 5, 0.2).until(EC.element_to_be_clickable((By.XPATH, select_location % result.get(result_key))))
            except Exception as e:
                driver.refresh()
                ys()
                print("验收按钮超时未加载，重新验收该项")
            else:
                driver.find_element_by_xpath(select_location % result.get(result_key)).click()
        print("当前语料：【%s】点击验收【%s】按钮" % (asr.get('asr'), result.get(result_key)))


def run(num):
    login(login_account, password)
    into_ys()
    for i in range(num):
        print(i+1)
        ys()
        time.sleep(0.5)
        i += 1
    driver.quit()


if __name__ == "__main__":
    run(2000)
