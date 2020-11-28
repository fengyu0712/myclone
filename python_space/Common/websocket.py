# from socket import create_connection
# import json, time, threading
import websocket



ws = websocket.create_connection('ws://linksit.aimidea.cn:10000/cloud/connect')


# reload(sys)
# sys.setdefaultencoding("utf8")


# config = {
#     'HOST': '127.0.0.1',
#     'PORT': 10086
# }
# pip install websocket-client

# class Client():
#     def __init__(self):
#         # 调用create_connection方法，建立一个websocket链接
#         # 链接地址请修改成你自己需要的
#
#         self.ws = create_connection('ws://linksit.aimidea.cn:10000/cloud/connect',timeout=30,source_address=None)
#         # 建一个线程，监听服务器发送给客户端的数据
#         self.trecv = threading.Thread(target=self.recv)
#         self.trecv.start()
#
#     # 发送方法，聊天输入语句时调用，此处默认为群聊ALL
#     def send(self, data):
#         # 这里定义的消息体要换成你自己的消息体，变成你需要的。
#         msg = json.dumps(data)
#         self.ws.send(msg)
#
#     # 接收服务端发送给客户的数据，只要ws处于连接状态，则一直接收数据
#     def recv(self):
#         try:
#             while self.ws.connected:
#                 result = self.ws.recv()
#                 return ("received msg:" + str(result))
#         except Exception as e:
#             pass
#
#     # 关闭时，发送QUIT方法，退出ws链接
#     def close(self):
#         # 具体要知道你自己退出链接的消息体是什么，如果没有，可以不写这个方法
#         msg = {
#             "type": "QUIT",
#             "username": "johanna",
#             "content": "byebye,everyone"
#         }
#         msg = json.dumps(msg)
#         self.ws.send(msg)
#
#
#
# url='ws://linksit.aimidea.cn:10000/cloud/connect'
# if __name__ == '__main__':
#
#     c = Client()
#     # 当输入非exit时，则持续ws链接状态，如果exit，则关闭链接
#     while True:
#         content = input("please input(input exit to exit):")
#         if content == "exit":
#             c.close()
#             break
#         else:
#             c.send(content)
#             time.sleep(1)