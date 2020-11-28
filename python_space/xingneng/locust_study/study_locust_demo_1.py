from locust import HttpLocust, TaskSet, task
from locust.contrib.fasthttp import FastHttpUser
import subprocess
import json


class UserBehavior(TaskSet):

    def on_start(self):
        u"""
                      request_url：请求路径
                      request_params：请求头参数
                      request_json：请求json参数
        """
        self.request_url = "/nlu/v1"  # （待测试的路径）
        self.headers = {"Content-Type": "application/json"}
        self.data = {
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

    @task(1)
    def getTagVals(self):
        response = self.client.post(
            path=self.request_url,
            data=json.dumps(self.data),
            headers=self.headers
        )
        if response.status_code != 200:
            print("返回异常")
            print(u"请求返回状态码:", response.status_code)
        elif response.status_code == 200:
            print(u"返回正常")

        #这里可以编写自己需要校验的返回内容
        response_content = json.loads(response.content)
        if response_content["intent"]["domain"] == "DeviceControl":
            print (u"校验成功")
            print (json.dumps(response_content))

    # 性能测试配置


class MobileUserLocust(FastHttpUser):
    u"""
    min_wait ：用户执行任务之间等待时间的下界，单位：毫秒。
    max_wait ：用户执行任务之间等待时间的上界，单位：毫秒。
    """
    # weight = 3
    tasks = [UserBehavior]
    host = "https://nlu.sit.aimidea.cn:22012"  # （待测试的ip或者域名）
    min_wait = 1000
    max_wait = 3000


if __name__ == "__main__":
    import os
    os.system("locust -f F:\python\python_space\\xingneng\locust_study\study_locust_demo_1.py")