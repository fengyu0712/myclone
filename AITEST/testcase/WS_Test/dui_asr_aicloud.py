# coding=utf-8
import os
from websocket import ABNF
import websocket, time, json, os, gc
import datetime
import uuid


#url = 'ws://dds-hb.dui.ai/dds/v1/test?serviceType=websocket&productId=278580818'
#url='wss://dds.dui.ai/dds/v2/test?serviceType=websocket&productId=278582256&apikey=674059aea679477db4f91cbf6ef72f5a&deviceName=midea216ff1f6-1203-44b6-abf2-824a27e12b6c&communicationType=fullDuplex'
#url='ws://dds.dui.ai/dds/v2/test?serviceType=websocket&productId=278582256&apikey=674059aea679477db4f91cbf6ef72f5a&deviceName=mideacf6411ef-976d-4292-a92a-1f0a765615b7'
#wavrootpath="D:/audio_file/wav音频/015/"

#url = "ws://127.0.0.1:10002/cloud/connect"
url = "ws://linksit.aimidea.cn:10000/cloud/connect"
wavrootpath="/data2/015/"

class Mywebscoket():
    def __init__(self,url,rootpath):
        self.wavpath=rootpath
        self.address=url
        self.step=3200
        #self.logfile="D:/1.log"
        self.logfile="D:/1.log"

    def write_fileinfo(self,lines):
        with open(self.logfile, 'a+', encoding="utf-8") as f:
            f.writelines(lines)
            f.writelines("\n")

    def get_time_stamp(self):
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = "%s.%03d" % (data_head, data_secs)
        return time_stamp

    def start_websocket(self):
        try:
            if not os.path.exists(self.wavpath):
                print("文件路径不存在,路径为：" ,self.wavpath)
                return

            ws = websocket.create_connection(self.address, timeout=30)
            result_asr = self.sendData(ws, self.wavpath)  # 获取预期结果
            print(result_asr )
            gc.collect()
            ws.close()

        except Exception as e:
            print(e)
            print("异常...")
        finally:
            gc.collect()
            #ws.close()

    def sendData(self, ws, wav_path):
        try:
            online = {
                "topic": "cloud.online",
                "mid": uuid.uuid1().hex,
                "version": "1.0",
                "request": {
                     "apiVer": "1.0.0",
                      "timestamp": 1234567890

                },
                "params": {
                    "clientId": "37bd7bee7aab1e5cb6e28ba04144c760",
                    "id": "12365e0e-df08-430d-a79e-4008d7054e5b",
                    "sn": "00000031122012507072402A00550000",
                    "category": "0xAC",
                    "magicCode": "TSETIA"
                }
            }

            ws.send(json.dumps(online), ABNF.OPCODE_TEXT)
            sessionId = uuid.uuid1().hex
            recordId = uuid.uuid1().hex
            content_328 = {
                "version": "3.0",
                "topic": "cloud.speech.trans",
                "mid": uuid.uuid1().hex,
                "id": "3298544982176",
                "sn": "00000021122251157813008987000000",
                "clientId": "ed091219-a1c0-4993-9076-099641c34c6a",
                "category": "AC",
                "request": {
                    "apiVer": "1.0.0",
                    "sessionId": sessionId,
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
            content = {
            "version": "2.0",
            "topic": "cloud.speech.trans",
            "mid": uuid.uuid1().hex,
            "id": "3298544982176",
            "sn": "00000021122251157813008987010000",
            "clientId": "eb2bb3607eb7393abe16abc5468822b3",
            "category": "AC",
            "request": {
                "apiVer": "1.0.0",
                "sessionId": sessionId,
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
            print("send start 1: " + self.get_time_stamp())
            ws.send(json.dumps(content), ABNF.OPCODE_TEXT)
            with open(wav_path, 'rb') as f:
                while True:
                    data = f.read(self.step)
                    if data:
                        ws.send(data, ABNF.OPCODE_BINARY)
                    if len(data) < self.step:
                        break
                    time.sleep(0.1)
            ws.send('', ABNF.OPCODE_BINARY)
            i = 0
            result=""
            while (i < 20):
                result = ws.recv()
                print(result)
                if 'tts' in result:
                    break
                time.sleep(0.1)
                i = i + 1
            return result
        except Exception as e:
            print("异常%s"%e)



    def on_message(self, message):
        return message


if __name__=="__main__":
    wavfail = "F:\\python\AITEST\\testdata\\test_audio\\201M24_01_41_0001.wav"
    #print( datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S.%f"))
    Mywebscoket(url,wavfail).start_websocket()