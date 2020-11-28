import requests, json, pytest
from Common.log import Logger
# from  bs4 import BeautifulSoup
import urllib3, time


class Request():
    def __init__(self, host=None):
        if host is None:
            self.host = ''
        else:
            self.host = host

    # @pytest.mark.flaky(reruns=2, reruns_delay=redis_case)  # 重试机制
    def requests(self, url, data, type, headers=None, cookies=None):
        url = self.host + url
        if headers == None and type.upper() == "POST":
            headers = {"Content-Type": "application/json"}
        if cookies == None:
            cookies = ""
        if type.upper() == "GET":
            Logger().debug(u"%s正在进行【GET】请求" % url)
            Logger().debug("body:" + str(data))
            try:
                urllib3.disable_warnings()
                response = requests.get(url, params=data, headers=headers, cookies=cookies,
                                        verify=False)  # https verify=False
                status_code = response.status_code
            except Exception as  e:
                Logger().error(e)
            else:
                if status_code == 200:
                    Logger().info(u"%s请求成功" % url)
                else:
                    Logger().error("请求出错【status:%s】" % status_code)
                Logger().debug("response:" + response.text)
                return response
        elif type.upper() == "POST":
            Logger().debug(u"%s正在进行【POST】请求" % url)
            Logger().debug("body:" + str(data))
            try:
                urllib3.disable_warnings()
                response = requests.post(url, data=json.dumps(data), headers=headers, cookies=cookies,
                                         verify=False)  # https verify=False
                status_code = response.status_code
            except Exception as  e:
                Logger().error(e)
            else:
                if status_code == 200:
                    Logger().info(u"%s请求成功" % url)
                else:
                    Logger().error(u"请求出错【status:%s】" % status_code)
                Logger().debug("response:" + response.text)

                return response
        else:
            Logger().error(u"请求类型错误")

    def downloads(self, url, save_path):
        resource = requests.get(self.host + url, stream=True)
        with open(save_path, 'wb') as fh:
            # fh.write(resource.content)
            for chunk in resource.iter_content(chunk_size=100):
                fh.write(chunk)

    def downloadFile(self, url, save_path):
        headers = {'Proxy-Connection': 'keep-alive'}
        r = requests.get(url, stream=True, headers=headers)
        length = float(r.headers['content-length'])
        f = open(save_path, 'wb')
        count = 0
        count_tmp = 0
        time1 = time.time()
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
                count += len(chunk)
                if time.time() - time1 > 1:
                    p = count / length * 100
                    speed = (count - count_tmp) / 1024 / 1024 / 2
                    count_tmp = count
                    print(save_path + ': ' + '{:.2f}'.format(p) + '%' + ' Speed: ' + '{:.2f}'.format(speed) + 'M/S')
                    time1 = time.time()
        f.close()


if __name__ == "__main__":
    # url = "https://nlu.sit.aimidea.cn:22012/nlu/v1"
    data = {
        "currentUtterance": "洗衣机帮我洗衣服，关机",
        "sourceDevice": "空调 ",
        "multiDialog": "false",
        "slotMiss": "false",
        "suite": [
            "multi"],
        "deviceId": "8711253015442522",
        "userGroup": "meiju",
        "userGroupCredential": "b82063f4-d39b-4940-91c3-5b67d741b4d3",
        "customDeviceNames": "",
        "customRoomNames": ""
    }
    #
    # response = Request().requests(url, data, "post")
    # a = json.dumps(response.json(), ensure_ascii=False, indent=4)
    # print(a)

    #============================================
    url="http://down.360safe.com/setup.exe"
    req=Request()
    save_path="E:\AITEST\\111.exe"
    req.downloadFile(url,save_path)
