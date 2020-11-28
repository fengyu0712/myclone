import websocket
import time
import json
from websocket import ABNF
from common.log import Logger
from common.conf import Conf
import Project_path
# import ssl
import uuid

# ssl._create_default_https_context = ssl._create_unverified_context
conf_path = Project_path.conf_path
data0 = Conf(conf_path + "/ws.ini").get_value("WS", "content")

mid = uuid.uuid1().hex


def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    return time_stamp


class WsSingle:
    def __init__(self, url):
        websocket.enableTrace(True)
        self.ws = websocket.create_connection(url)  # 创建连接
        self.session_id = None
        Logger().info("WebSocket链接建立成功")

    def on_line(self):
        print("====>登录")
        onlinedata = {
            "topic": "cloud.online",
            "mid": uuid.uuid1().hex,
            "version": "3.0",
            "request": {
                "apiVer": "1.0.0",
                "timestamp": get_time_stamp,
                "paramsSignBase64": "mPDZcVBzfyIM4rWt3B9tgRsl1ys="
            },
            "params": {
                "productId": "1578471165",
                "sn": "00000031122240011922702600110000",
                "clientId": "eb2bb3607eb7393abe16abc5468822b2",
                "category": "0xDB",
                "model": "123",
                "id": "23454365465643",
                "ip": "0.0.0.0",
                "mac": "88e9fe5d3829"
            }
        }
        self.ws.send(json.dumps(onlinedata))
        return self.ws.recv()

    def keeplive(self):
        print("====>心跳检测")
        keeplive_data = {
            "request": {
            },
            "topic": "cloud.keeplive",
            "mid": uuid.uuid1().hex,
            "params": {
            },
            "version": "1.0"
        }

        self.ws.send(json.dumps(keeplive_data), ABNF.OPCODE_TEXT)
        return self.ws.recv()

    def speech(self, wavfile):
        print("====>发送语音")
        self.session_id = uuid.uuid1().hex
        record_id = uuid.uuid1().hex
        content = {
            "topic": "cloud.speech.trans",
            "mid": uuid.uuid1().hex,
            "version": "1.0",
            "request": {
                "timestamp": get_time_stamp,
                "sessionId": self.session_id,
                "recordId": record_id,
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
        try:
            with open(wavfile, 'rb') as f:
                while True:
                    data = f.read(3200)
                    if data:
                        # print(data)
                        self.ws.send(data, ABNF.OPCODE_BINARY)
                    if len(data) < 3200:
                        break
                    time.sleep(0.1)
        except Exception as e:
            Logger().error(e)
        else:
            self.ws.send('', ABNF.OPCODE_BINARY)
            self.speech_nlp()
            return self.ws.recv()

    def speech_nlp(self):
        print("===>NLP")
        data = {
            "topic": "cloud.speech.nlp.withText",
            "mid": uuid.uuid1().hex,
            "version": "1.0",
            "request": {
                "timestamp": get_time_stamp
            },
            "params": {
                "sessionId": self.session_id,
                "text": "",
                "nlpIsp": "dui"
            }
        }
        self.ws.send(json.dumps(data), ABNF.OPCODE_TEXT)
        return self.ws.recv()


wavfail = "F:\\python\\AITEST\\testdata\\test_audio\\002M30_36_010001.wav"
if __name__ == "__main__":
    sit_url = Conf(conf_path + "/ws.ini").get_value("SIT", "url")
    ws = WsSingle(sit_url)
    a = ws.on_line()
    print(a)
    # time.sleep(0.2)
    # # b = ws.keeplive()
    # # print(b)
    c = ws.speech(wavfail)
    print(c)

    time.sleep(2)
    # b = ws.keeplive()
    # print(b)
