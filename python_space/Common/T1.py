from ws4py.client.threadedclient import WebSocketClient
import time,json

class DummyClient(WebSocketClient):
    def opened(self):
        self.send("www.baidu.com")

    def closed(self, code, reason=None):
        return ("Closed down", code, reason)

    def received_message(self, m):
        return (m)


data={
    "topic": "cloud.connect",
    "mid": "6aad0b12-2192-4b90-8f40-08a2bc0b5c2a",
    "version": "1.0",
    "request": {
        "apiVer": "1.0.0",
        "timestamp": 1234567890,
        "pki":"fndjsafhop3u8rheowfh"
    },
    "params": {
        "sn": "0000DB11138104887174101101740000",
        "category": "0xDB",
        "model": "123",
        "id": "23454365465643",
        "ip": "0.0.0.0",
        "mac": "88e9fe5d3829",
        "random": "545623"
    }
}
if __name__ == '__main__':
    try:
        ws = WebSocketClient('ws://linksit.aimidea.cn:10000/cloud/connect', protocols=['chat'])
        ws.connect()
        print(ws.received_message("连接成功"))  #
        # ws.run_forever()
        print("连接成功")
    except KeyboardInterrupt:
        ws.close()
        print("失败了")
    ws.send(json.dumps(data))
    # print(ws.recv())
    time.sleep(10)
    ws.close()