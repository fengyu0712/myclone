import websocket
import time
import json
import uuid
from websocket import ABNF
from common.log import Logger
from common.conf import Conf
import Project_path
# import ssl
import os



# ssl._create_default_https_context = ssl._create_unverified_context
conf_path = Project_path.conf_path

# data0 = Conf(os.path.join(conf_path,"device_protocol.ini")).get_value("3308", "online_data")


# 芳芳机器
# sn = "00000031122251059042507F12340000"
# clientId = "cf6411ef-976d-4292-a92a-1f0a765615b8"

# sn = "00000021122251157813008987000000"
# clientId = "test001"
# deviceID="3298544982176"
# category="AC"

sn = "000008311000VA022091500000289FGR"
clientId = "test002"
deviceID="160528699142378"
category="8"



class SimDevices:
    def __init__(self, url):
        # websocket.enableTrace(True)
        self.ws = websocket.create_connection(url)  # 创建连接
        Logger().info("WebSocket链接建立成功")

    def get_time_stamp(self):
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = "%s.%03d" % (data_head, data_secs)
        return time_stamp

    def on_line(self):
        print("====>登录")
        online_data_1 = {
            "topic": "cloud.online",
            "mid": uuid.uuid1().hex,
            "version": "1.0",
            "request": {
                "apiVer": "1.0.0",
                "timestamp": self.get_time_stamp(),

            },
            "params": {
                "id": deviceID,
                "sn": sn,
                "clientId": clientId,
                "category": category,
                "magicCode": "TSETIA"
            }
        }
        online_data_3 = {
            "topic": "cloud.online",
            "version": "3.0",
            "mid": uuid.uuid1().hex,
            "request": {
                "apiVer": "1.0.0",
                "timestamp": self.get_time_stamp(),
                "paramsSignBase64": "CD2leuWLTS81d4GSF1JqRrw/n8I="
            },
            "params": {
                "category": category,
                "clientId": clientId,
                "id": deviceID,
                "ip": "127.0.0.1",
                "mac": "f0:c9:d1:85:25:39",
                "model": "172",
                "productId": "1596681815",
                "sn": sn
            }
        }
        ota_check_data = {
            "topic": "cloud.ota.check",
            "mid": uuid.uuid1().hex,
            "version": "3.0",
            "request": {
                "timestamp": self.get_time_stamp(),
            },
            "params": {
                "sn": sn,
                "category": category,
                "model": "172",
                "id": deviceID,
                "clientId": clientId,
                "brand": "Midea",
                "hardwarePlat": "07",
                "hardwareVer": "01.01",
                "hardwareCategory": "03",
                "hardwareModel": "f4",
                "hardwareFullVer": "07.03.01.01.f4",
                "firmwareVer": "07.03.01.01.f4.20.10.05.01.06"
            }
        }
        audio_status_data = {
            "version": "3.0",
            "topic": "cloud.report.status",
            "mid": uuid.uuid1().hex,
            "category": category,
            "id": "3298544982176",
            "clientId": clientId,
            "sn": sn,
            "request": {
                "timestamp": self.get_time_stamp()
            },
            "params": {
                "status": [{
                    "class": "audio",
                    "audio": {
                        "level": "4",
                        "max": "99",
                        "min": "1",
                        "volume": "75"
                    }
                }]
            }
        }
        self.ws.send(json.dumps(online_data_3))
        # 全双工需要用到开机上报的版本信息
        self.ws.send(json.dumps(ota_check_data))
        # 上报音量信息等
        self.ws.send(json.dumps(audio_status_data))

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
            "version": "3.0"
        }

        self.ws.send(json.dumps(keeplive_data), ABNF.OPCODE_TEXT)
        return self.ws.recv()

    def speech(self, wavfile):
        print("====>发送语音")
        self.sessionId = uuid.uuid1().hex
        recordId = uuid.uuid1().hex
        content_3308 = {
            "version": "2.0",
            "topic": "cloud.speech.trans",
            "mid": uuid.uuid1().hex,
            "id": deviceID,
            "sn": sn,
            "clientId": clientId,
            "category": category,
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
        content_328 = {
            "version": "3.0",
            "topic": "cloud.speech.trans",
            "mid": uuid.uuid1().hex,
            "id": deviceID,
            "sn": sn,
            "clientId": clientId,
            "category": category,
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
                },
                "ttsIsp": "dui-real-sound",
                "nluIsp": "DUI",
                "asrIsp": "DUI",
                "serverVad": False,
                "accent": "mandarin",
                "mixedResEnable": "0"
            }
        }
        content_328_fullDuplex = {
            "version": "3.0",
            "topic": "cloud.speech.trans",
            "mid": uuid.uuid1().hex,
            "id": deviceID,
            "sn": sn,
            "clientId": clientId,
            "category": category,
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
                },
                "ttsIsp": "dui-real-sound",
                "nluIsp": "DUI",
                "asrIsp": "DUI",
                "serverVad": False,
                "accent": "mandarin",
                "fullDuplex": True
            }
        }

        self.ws.send(json.dumps(content_328), ABNF.OPCODE_TEXT)
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
        timeout = 5
        result_dit = {}
        try:
            for i in range(10 * timeout):
                result = self.ws.recv()
                if 'cloud.speech.trans.ack' in result:
                    result_dit['asr'] = result
                elif 'cloud.speech.reply' in result:
                    result_dit['nlg'] = result
                    break
                time.sleep(0.1)
                i += 1
        except Exception as e:
            result_dit = {'error': e}
            print(e)
        finally:
            if "asr" not in result_dit.keys():
                result_dit["asr"]="ASR获取超时"
            if "nlg" not in result_dit.keys():
                result_dit["nlg"]="NLG获取超时"
            return result_dit

    # def speechNlp(self):
    #     print("===>NLP")
    #     data = {
    #         "topic": "cloud.speech.nlp.withText",
    #         "mid": uuid.uuid1().hex,
    #         "version": "1.0",
    #         "request": {
    #             "timestamp": self.get_time_stamp()
    #         },
    #         "params": {
    #             "sessionId": self.sessionId,
    #             "text": "",
    #             "nlpIsp": "dui"
    #         }
    #     }
    #     self.ws.send(json.dumps(data), ABNF.OPCODE_TEXT)
    #     return self.ws.recv()

    def close(self):
        self.ws.close()
        Logger().info("WebSocket断开")


if __name__ == "__main__":
    url = Conf(conf_path + "/ws.ini").get_value("SIT", "url")
    print(url)
    wavfail =Project_path.TestData_path+"test_audio\\201M24_01_41_0001.wav"
    wavfail2 =Project_path.TestData_path+"test_audio\\237M32_08_41_0160.wav"
    wavfail3 =Project_path.TestData_path+"test_audio\\佛山的天气如何.wav"
    ws = SimDevices(url)
    a = ws.on_line()
    print(a)

    # time.sleep(2)
    # b = ws.speech(wavfail)
    # print(b)
    print("=====>====")
    # d = ws.speech(wavfail2)
    # print(d)
    # print("=====>====")
    # time.sleep(5)
    # f = ws.speech(wavfail2)
    # print(f)
    # print("=====>====")
    # time.sleep(5)
    # f = ws.speech(wavfail2)
    # print(f)
    # print("=====>====")
    # time.sleep(5)
    f = ws.speech(wavfail2)
    print(f)
    print("=====>====")
    time.sleep(2)
    f = ws.speech(wavfail3)
    print(f)

    ws.close()
    # print(f)
    # b = ws.keeplive()
    # print(b)
