import os, sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.dirname(os.path.dirname(os.path.dirname(curPath)))
sys.path.append(rootPath)  # 获取绝对路径，以便shell脚本跑
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import time, platform,json
from selenium.webdriver import DesiredCapabilities

from Common.conf import Read_conf
from Conf import Project_path
from Common.log import Logger

conf_path = Project_path.Conf_path + "web.ini"
url = Read_conf(conf_path).get_value("AI", "url")
login_account = Read_conf(conf_path).get_value("AI", "login_account")
password = Read_conf(conf_path).get_value("AI", "password")

account_location = "//input[@name='username']"
password_location = "//input[@name='password']"
login_button_location = "//span[text()='登录']/.."

login_labeling = "//h1[text()='标注任务']"
continue_ys = "//button[@class='el-button el-button--primary el-button--small button']"
start_ys = "//span[text()='开始验收']/.."
YES = "//span[text()='确定']"

# 加载启动项

chrome_options = webdriver.ChromeOptions()
# capabilities = DesiredCapabilities.CHROME.copy()
# #是否打开浏览器运行
# if platform.system() == "Linux" or "Ubuntu":
#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#
#     capabilities['acceptSslCerts'] = True
#     capabilities['acceptInsecureCerts'] = True
chrome_options.add_argument('headless')
chrome_options.add_argument('--disable-gpu')

asr_location = "//p[@class='markStrC']"
classifier_location = "//div[@class='dt_dropDown field']/p"

select_location = "//div[@class='examiner']//div[text()='%s']"
# driver = webdriver.Chrome(options=chrome_options,desired_capabilities=capabilities)
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)


# print(driver.page_source)
n1 = 0
def login(account, password):
    global n1
    try:
        WebDriverWait(driver, 5, 0.2).until(EC.visibility_of_element_located((By.XPATH, account_location)))
    except Exception as e:
        if n1>3:
            driver.quit()
            raise e
        else:
            print(n1)
            n1 += 1
            driver.refresh()
    else:
        driver.find_element_by_xpath(account_location).clear()
        driver.find_element_by_xpath(account_location).send_keys(account)
        driver.find_element_by_xpath(password_location).send_keys(password)
        driver.find_element_by_xpath(login_button_location).click()


def into_ys():
    try:
        WebDriverWait(driver, 10, 0.5).until(EC.visibility_of_element_located((By.XPATH, login_labeling)))
        Logger().info("登录成功")
    except Exception as e:
        Logger().error("登录异常:%s" % e)
        raise e
    try:
        WebDriverWait(driver, 5, 0.2).until(EC.element_to_be_clickable((By.XPATH, continue_ys)))
    except Exception as e:
        driver.quit()
        raise e
    else:
        driver.find_element_by_xpath(continue_ys).click()
        Logger().info("点击验收任务按钮")
    try:
        WebDriverWait(driver, 10, 0.2).until(EC.element_to_be_clickable((By.XPATH, start_ys)))
    except Exception as e:
        driver.quit()
        raise e
    else:
        driver.find_element_by_xpath(start_ys).click()
        Logger().info("点击开始验收按钮")

    try:
        WebDriverWait(driver, 10, 0.2).until(EC.element_to_be_clickable((By.XPATH, YES)))
    except Exception as e:
        driver.quit()
        raise e
    else:

        driver.find_element_by_xpath(YES).click()
        Logger().info("点击确定按钮")

    # 得到selenium打开的浏览器的所有句柄
    time.sleep(5)
    all_hand = driver.window_handles
    # 切换句柄
    driver.switch_to_window(all_hand[-1])
    Logger().info("切换到验收页面")


def get_asr():
    keys={"通用领域":'publicDomain',"美的领域":'mideaDomain'}
    try:
        WebDriverWait(driver, 5, 0.2).until(EC.element_to_be_clickable((By.XPATH, asr_location)))
    except Exception as e:
        raise e
    else:
        asr = driver.find_element_by_xpath(asr_location).text
        classifier = driver.find_element_by_xpath(classifier_location).text.split("-")[0]
    return {'asr': asr, 'classifier': keys.get(classifier)}


def nlu(asr):
    from Common.http_request_new import Request
    url = "https://nlu.sit.aimidea.cn:22012/nlu/v1"
    data = {"currentUtterance": asr, "sourceDevice": "空调", "multiDialog": "false", "slotMiss": "false",
            "suite": ["default"], "deviceId": "9049230323909912", "userGroup": "meiju",
            "userGroupCredential": "b82063f4-d39b-4940-91c3-5b67d741b4d3", "customDeviceNames": "",
            "customRoomNames": ""}
    response=Request().requests(url,data,"post")
    return response


def ys():
    result={"0":'合格',"1":'不合格'}
    asr = ''
    try:
        WebDriverWait(driver, 3, 0.2).until(EC.element_to_be_clickable((By.XPATH, asr_location)))
    except:
        Logger().info("等待超时，重新刷新页面")
        driver.refresh()
        ys()
    else:
        asr = get_asr()
        Logger().info("当前验收语料：【%s】,标记人员执行结果是：【%s】" % (asr.get('asr'),asr.get('classifier')))
    nlu_result = nlu(asr.get('asr')).text
    Logger().info("当前验收语料：【%s】的NLU分类器结果是：%s" % (asr.get('asr'), json.loads(nlu_result)['classifier']))
    result_key='0'
    try:
        assert json.loads(nlu_result)['classifier']==asr.get('classifier')
    except:
        result_key=input("【%s】 选择 【%s】  与NLU分类器结果不一致，请人工判断（0：合格，1：不合格）："%(asr.get('asr'),asr.get('classifier')))
    else:
        result_key = '0'
    finally:
        driver.find_element_by_xpath(select_location % result.get(result_key)).click()
    Logger().info("当前语料：【%s】点击验收【%s】按钮" % (asr.get('asr'),result.get(result_key)))



def run():
    login(login_account, password)
    into_ys()
    for i in range(500):
        ys()
        time.sleep(1)
        i += 1
    driver.quit()

if __name__ == "__main__":
    run()
