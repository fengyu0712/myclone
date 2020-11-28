import websocket
from threading import Thread
import time,os
import sys
import json
import _thread
import xlrd
from xlutils.copy import copy
product_id = '278575321' #填入产品Id
apikey = 'x' #填入apikey
url = 'wss://hn.dui.ai/dds/v1/test?serviceType=websocket&productId='+product_id

# excel_path="E:\python_space\Source\websocket_test\AI云端ASR测试用例.xlsx"
result_path="E:\python_space\Source\websocket_test\AI云端ASR测试用例执行结果.xlsx"
excel_path="E:\python_space\Source\websocket_test\AI云端ASR测试用例.xlsx"
#音频文件路径
cmd_path="E:/ws/002M30_36"
# cmd_path="E:\python_space\Source\websocket_test/test"
sheetName="002M30_36"

# 获取数据
data = xlrd.open_workbook(excel_path)
# 获取sheet
table = data.sheet_by_name(sheetName)

# 获取总行数
nrows =table.nrows
index=2
except_value=""  #预期结果
print("nows:"+ str(nrows))


success_total=0
fail_total=0
total=0


class MyWebsocket(websocket.WebSocketApp):
    def on_message(self, message):
        print('Message>>>>>>>>>>>>>>>>>>>>>>>>')
        print(message)
        mJson = json.loads(message)
        if 'eof' in message:
            text = mJson['text']
            global index, success_total, fail_total, total

            print(index)
            print("返回值:", text)
            text = str(text).replace(' ', '')
            print(text)
            table.put_cell(index, 2, 1, text, format)
            total = total + 1
            except_value = table.cell(index, 1).value
            print("期望：", except_value)
            if (except_value == text):
                table.put_cell(index, 3, 1, str(True), format)
                success_total = success_total + 1
            else:
                table.put_cell(index, 3, 1, str(False), format)
                fail_total = fail_total + 1
            index = index + 1
            if (index == nrows):
                sucess_rate = (success_total / total) * 100
                sucess_rate_value = "{:.2f}%".format(sucess_rate)
                table.put_cell(0, 1, 1, sucess_rate_value, format)
                wb = copy(data)
                wb.save(result_path)
        print('Message<<<<<<<<<<<<<<<<<<<<<<<<')

    def on_error(self, error):
        print('error>>>>>>>>>>>>>>>>>>>>>>')
        print(error)
        wb = copy(data)
        wb.save(result_path)
        print('error<<<<<<<<<<<<<<<<<<<<<<')

    def on_close(self):
        print("### closed ###")

    def on_open(self):
        def run(*args):
            for i in range(index, nrows):
                wav_value = table.cell(i, 0).value  # wav文件值
                if wav_value.strip() == '':
                    continue

                wav_value = sheetName + "_" + wav_value + ".wav"
                print("aaaaaaa" + wav_value)
                wav_path = cmd_path + "/" + wav_value  # wav 路径
                if (os.path.exists(wav_path) == False):
                    continue

                except_value = table.cell(i, 1).value  # 预期结果值
                content = {
                    "topic": "recorder.stream.start",
                    "recordId": "21354578ijhgbvdrt35",
                    "audio": {
                        "audioType": "wav",
                        "sampleRate": 16000,
                        "channel": 1,
                        "sampleBytes": 2
                    },
                    "asrParams": {
                        "enableVAD": False,
                        "realBack": False,
                        "toneEnable": True
                    },
                    "aiType": "asr"

                }
                ws.send(json.dumps(content))
                step = 3200  # 如果audioType是wav，此处需要修改为3200
                with open(wav_path, 'rb') as f:
                    while True:
                        data = f.read(step)
                        if data:
                            ws.send(data, websocket.ABNF.OPCODE_BINARY)
                        if len(data) < step:
                            break
                        time.sleep(0.1)
                ws.send('', websocket.ABNF.OPCODE_BINARY)
                time.sleep(0.1)

        _thread.start_new_thread(run, ())
        # Thread(target=run).start()


if __name__ == "__main__":
    websocket.enableTrace(True)
    # if len(sys.argv) < 2:
    #     host = url
    # else:
    #     host = sys.argv[1]
    ws = MyWebsocket(url,on_message = MyWebsocket.on_message,
                          on_error = MyWebsocket.on_error,
                          on_close = MyWebsocket.on_close)
    ws.on_open = MyWebsocket.on_open
    ws.run_forever()