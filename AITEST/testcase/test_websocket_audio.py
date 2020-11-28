#!/usr/bin/env python
# coding=utf-8
### websocket模块https://pypi.python.org/pypi/websocket-client
### wavfile是一个speex压缩的ogg文件,文件格式是Ogg data, Speex audio
import websocket
from websocket import ABNF
import time
import threading
import json
import ssl
import uuid

url = "ws://127.0.0.1:10002/cloud/connect"
# url = "wss://linkdit.aimidea.cn:10003/cloud/connect"
# url = "ws://linksit.aimidea.cn:10000/cloud/connect"
# url = "ws://link.uat.aimidea.cn:10000/cloud/connect"
# url = "wss://link.uat.aimidea.cn:10443/cloud/connect"
# url = "ws://link.aimidea.cn:10000/cloud/connect"
# url = "wss://link.aimidea.cn:10443/cloud/connect"

wavfile = 'opencooker.wav'
wavfile2 = 'audio/空白.wav'


def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - long(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    return time_stamp


def on_message(ws, message):
    print
    'Message>>>>>>>>>>>>>>>>>>>>>>>>'
    print
    get_time_stamp()
    print
    message
    print
    'Message<<<<<<<<<<<<<<<<<<<<<<<<'


#    if json.loads(message)["eof"] == 1:
#        print "terminate now!!"
#        ws.close()

def on_error(ws, error):
    print
    'error>>>>>>>>>>>>>>>>>>>>>>'
    print
    get_time_stamp()
    print
    error
    print
    'error<<<<<<<<<<<<<<<<<<<<<<'


def on_close(ws):
    print
    get_time_stamp()
    print
    "### closed ###"


# def on_data(ws, resp, datatype, ctnu):
#     print datatype

def on_open(ws):
    def run(*args):
        online = {
            "topic": "cloud.online",
            "mid": uuid.uuid1().hex,
            "version": "1.0",
            "request": {
                "timestamp": get_time_stamp()
            },
            "params": {
                "clientId": "12365e0e-df08-430d-a79e-4008d7054e5b",
                "id": "12365e0e-df08-430d-a79e-4008d7054e5b",
                "sn": "00000021122012243813008835770000",
                "category": "0xAC",
                "magicCode": "TSETIA"
            }
        }
        ws.send(json.dumps(online), ABNF.OPCODE_TEXT)
        time.sleep(0.2)

        sessionId = uuid.uuid1().hex
        recordId = uuid.uuid1().hex

        content = {
            "topic": "cloud.speech.trans",
            "mid": uuid.uuid1().hex,
            "version": "1.0",
            "request": {
                "timestamp": get_time_stamp(),
                "sessionId": sessionId,
                "recordId": recordId,
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
        print
        "send start 1: " + get_time_stamp()
        ws.send(json.dumps(content), ABNF.OPCODE_TEXT)

        step = 3200  # 如果audioType是wav，此处需要修改为3200
        with open(wavfile, 'rb') as f:
            while True:
                data = f.read(step)
                if data:
                    ws.send(data, ABNF.OPCODE_BINARY)
                if len(data) < step:
                    break
                time.sleep(0.1)
        ws.send('', ABNF.OPCODE_BINARY)
        print
        "send end 1: " + get_time_stamp()

        transTwo = False
        if transTwo:
            content = {
                "topic": "cloud.speech.trans",
                "mid": uuid.uuid1().hex,
                "version": "1.0",
                "request": {
                    "timestamp": get_time_stamp(),
                    "sessionId": sessionId,
                    "recordId": recordId,
                    "isMore": True,
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
            print
            "send start 2: " + get_time_stamp()
            ws.send(json.dumps(content), ABNF.OPCODE_TEXT)

            with open(wavfile2, 'rb') as f:
                while True:
                    data = f.read(step)
                    if data:
                        ws.send(data, ABNF.OPCODE_BINARY)
                    if len(data) < step:
                        break
                    time.sleep(0.1)
            ws.send('', ABNF.OPCODE_BINARY)
            print
            "send end 2: " + get_time_stamp()

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
