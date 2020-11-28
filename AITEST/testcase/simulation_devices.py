import websocket, time, json
from websocket import ABNF
from common.log import Logger
from common.conf import Conf
import Project_path
import ssl
import uuid
import threading

ssl._create_default_https_context = ssl._create_unverified_context
conf_path = Project_path.conf_path
data0 = Conf(conf_path + "/ws.ini").get_value("WS", "content")

mid = uuid.uuid1().hex


class SimDdevices:
    def __init__(self, url):
        websocket.enableTrace(True)
        self.ws = websocket.create_connection(url)  # 创建连接
        Logger().info("WebSocket链接建立成功")

    def get_time_stamp(self):
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = "%s.%03d" % (data_head, data_secs)
        return time_stamp

    # @pytest.mark.flaky(reruns=2, reruns_delay=redis_case)  # 重试机制
    def on_line(self):
        print("====>登录")
        onlineData = {
            "topic": "cloud.online",
            "mid": uuid.uuid1().hex,
            "version": "1.0",
            "request": {
                "apiVer": "1.0.0",
                "timestamp": self.get_time_stamp()
            },
            "params": {
                "productId": "1578471165",
                "sn": "00000021122251157813008987000000",
                "clientId": "ed091219-a1c0-4993-9076-099641c34c6a",
                "category": "0xAC",
                "model": "TSETIA",
                "id": "23454365465643",
                "ip": "0.0.0.0",
                "mac": "88e9fe5d3829"
            }
        }
        self.ws.send(json.dumps(onlineData), ABNF.OPCODE_BINARY)
        return self.ws.recv()

    def keeplive(self):
        print("====>心跳检测")
        keepLiveData = {
            "request": {
            },
            "topic": "cloud.keeplive",
            "mid": uuid.uuid1().hex,
            "params": {
            },
            "version": "3.0"
        }

        self.ws.send(json.dumps(keepLiveData), ABNF.OPCODE_TEXT)
        return self.ws.recv()

    def speech(self, wavfile, step=None):
        print("====>发送语音")
        self.sessionId = uuid.uuid1().hex
        recordId = uuid.uuid1().hex
        # if content == None:
        #     content = eval(data0)
        if step == None:  # 如果audioType是wav，此处需要修改为3200
            step = 3200
        #
        content = {
            "version": "2.0",
            "topic": "cloud.speech.trans",
            "mid": uuid.uuid1().hex,
            "id": "3298544982176",
            "sn": "00000021122251157813008987000000",
            "clientId": "eb2bb3607eb7393abe16abc5468822b2",
            "category": "AC",
            "request": {
                "apiVer": "1.0.0",
                "sessionId": self.sessionId,
                "recordId": recordId,
                "isMore": False
            },
            "params": {
                "audio": {
                    "audioType": "wav",
                    "sampleRate": 16000,
                    "channel": 1,
                    "sampleBytes": 2
                }
            }
        }

        self.ws.send(json.dumps(content), ABNF.OPCODE_TEXT)
        with open(wavfile, 'rb') as f:
            while True:
                data = f.read(3200)
                if data:
                    # print(data)
                    self.ws.send(data, ABNF.OPCODE_BINARY)
                if len(data) < 3200:
                    break
                time.sleep(0.1)
        self.ws.send('', ABNF.OPCODE_BINARY)
        self.speechNlp()
        result = self.ws.recv()
        return result

        # return self.ws.recv()

    def speechNlp(self):
        print("===>NLP")
        data = {
            "topic": "cloud.speech.nlp.withText",
            "mid": uuid.uuid1().hex,
            "version": "1.0",
            "request": {
                "timestamp": self.get_time_stamp()
            },
            "params": {
                "sessionId": self.sessionId,
                "text": "",
                "nlpIsp": "dui"
            }
        }
        self.ws.send(json.dumps(data), ABNF.OPCODE_TEXT)
        return self.ws.recv()
    # def runsingle(self, wavfile, content=None, step=None):
    #     if content == None:
    #         content = eval(data0)
    #     if step == None:  # 如果audioType是wav，此处需要修改为3200
    #         step = 3200
    #     self.ws.send(json.dumps(content))
    #     try:
    #         with open(wavfile, 'rb') as f:
    #             while True:
    #                 data = f.read(step)
    #                 if data:
    #                     # print(data)
    #                     self.ws.send(data, ABNF.OPCODE_BINARY)
    #                 if len(data) < step:
    #                     break
    #                 time.sleep(0.01)
    #     except Exception as e:
    #         Logger().error(e)
    #     else:
    #         self.ws.send('', ABNF.OPCODE_BINARY)
    #         result = self.ws.recv()
    #         return result
    #
    # def close(self):
    #     self.ws.close()
    #     Logger().info("WebSocket链接关闭")
    #


if __name__ == "__main__":
    url = Conf(conf_path + "/ws.ini").get_value("SIT", "url")
    wavfile2 = "F:\\python\AITEST\\testdata\\test_audio\\201M24_01_41_0001.wav"
    d = SimDdevices(url)
    # d.on_line()
    # print(d)
    d.speech(wavfile2)
    # # d.speechNlp()
    print(d)
    # time.sleep(2)
