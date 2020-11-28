# coding:utf-8
from Common import log, read_xls_news
from Common import mypyaudio
# from Common.SimplifyASR import simplify_asr
import os
import re
import time
import serial
import serial.tools.list_ports
import Project_path

now = time.strftime('%Y-%m-%d-%H-%M-%S')
excel_path = os.path.join(Project_path.test_date_path, 'AI云端ASR测试用例_test.xlsx')  # 映射关系表，命令词
result_path = os.path.join(Project_path.test_result_path, '半双工ASRm45度噪音识别率测试--result%s.xls' % now)
wakeup_path = os.path.join(Project_path.test_audio_path, "002M30_36_010003.wav")  # #唤醒文件：你好小美的音频文件
cmd_path = "E:/ws/002M30_36/"

asr_mid_pattern = "text\":	\"(.*)\"[\\s\\S]*\"info\":	\"(.*)\""
wakeup_sign = "ev\":	\"wake up\""
in_fullduplex_sign = "full duplex mode"
asr_pattern = "text\":	\"(.*)\""

Log = log.Logger()
Log.info("=======================半双工链路ASR识别率测试========================")


class MySerial:
    def __init__(self, baudrate, serialname=None):
        plist = list(serial.tools.list_ports.comports())
        if len(plist) <= 0:
            print("The Serial port can't find!")
        else:
            plist_0 = list(plist[0])
            if serialname is None:
                serialname = plist_0[0]
            self.serialFd = serial.Serial(serialname, baudrate, timeout=60)
            print("check which port was really used >", self.serialFd.name)
            if self.serialFd.isOpen():
                print("Serial port open success")
            else:
                print("Serial port open failed")

    def recvcmd(self, timeout=None):
        if timeout is None:
            timeout = 10
        all_data = ""
        start_time = time.time()
        while True:
            end_time = time.time()
            if end_time - start_time < timeout:
                data = self.serialFd.read(self.serialFd.inWaiting())
                data = data.decode(encoding='utf-8', errors='ignore')
                Log.debug(data)
                if data != '':
                    all_data = all_data + data
            else:
                break
        return all_data

    def recv_data(self, pattern_list=None, checktime=None):
        if checktime is None:
            checktime = 10
        if pattern_list is None:
            pattern_list = []
        new_pattern_list = list(pattern_list)
        result_data = []
        start_time = time.time()
        while time.time() < start_time + checktime:
            data = self.serialFd.read(self.serialFd.inWaiting())
            data = data.decode(encoding='utf-8', errors='ignore')
            Log.debug(data)
            if data != '':
                if new_pattern_list:
                    for i in range(len(new_pattern_list)):
                        m = re.findall(new_pattern_list[0], data)
                        if not m:
                            break
                        if m[0]:
                            new_pattern_list.pop(0)
                            result_data.append(m[0])
                        else:
                            break
            time.sleep(1)
            if len(result_data) == len(pattern_list):
                break
        while len(result_data) < len(pattern_list):
            result_data.append(False)
        print("result_data测试结果：%s" % result_data)
        return result_data


s = MySerial(baudrate="961200")


def wakeup():
    if os.path.exists(wakeup_path):
        for i in range(3):
            mypyaudio.play_audio(wakeup_path)
            wakeup_result = s.recv_data(pattern_list=[wakeup_sign], checktime=5)
            if wakeup_result is None:
                Log.error("连续%s次未唤醒" % (i + 1))
                i += 1
            else:
                return True
    else:
        raise ("唤醒的音频文件不存在..." + wakeup_path)


def get_data(path, booknames=None):
    r = read_xls_news.Read_xls(path)
    if booknames is None:
        booknames = r.get_sheet_names()
    test_data = []
    for i in range(len(booknames)):
        data = r.read_data(booknames[i], start_line=3)
        test_data += data
        i += 1
    w = r.copy_book()
    r.save_write(w, result_path)
    return test_data


total_num = 0
asr_succese_num = 0
test_num = 0


def run():
    global test_num, asr_succese_num, total_num
    bookname = '002M30_36'
    booknames = [bookname]
    test_data = get_data(excel_path, booknames)
    for i in range(len(test_data)):
        Log.info("开始第%s条测试：%s" % (i + 1, test_data[i][:2]))
        except_value = test_data[i][1]
        wav_path = cmd_path + "/002M30_36_" + test_data[i][0] + ".wav"  # wav 路径
        test_result = "Fail"
        iswakeup = wakeup()
        if iswakeup is None:
            Log.error("連續三次未喚醒！")
        else:
            test_num += 1
            Log.info("唤醒成功，即将进入播放音频进行ASR测试")
            rr = read_xls_news.Read_xls(result_path)
            rw = rr.copy_book()
            Log.info("开始播放测试音频【%s】" % wav_path)
            mypyaudio.play_audio(wav_path)
            asr_log = s.recvcmd(10)
            asr_result = re.findall(asr_mid_pattern, asr_log)
            if asr_result[0]:
                asr = asr_result[0]
                mid = asr_result[1]
                if except_value == asr:
                    test_result = "Pass"
                    asr_succese_num += 1
            else:
                asr = False
                mid = False
            asr_succese_rate = "%.2f%%" % (asr_succese_num / test_num * 100)
            Log.info("用例【%s】ASR识别结果：%s" % (test_data[i][:2], asr))
            Log.info("用例【%s】ASR测试结果：%s" % (test_data[i][:2], test_result))
            Log.info(
                "当前一共执行测试【%s次】，正常执行【%s】，其中ASR识别正确【%s次】,识别率为：【%s】" % (
                    i + 1, test_num, asr_succese_num, asr_succese_rate))
            rr.write_linedata(rw, i + 2, [asr, test_result, mid], sheetname=bookname, col=3)
            rr.write_onlydata(rw, 0, 1, asr_succese_rate, sheetname=bookname)
            rr.save_write(rw, result_path)


if __name__ == "__main__":
    run()

    # from Common.send_mail import Mail
    # from Common.Zipfile import Zipfile
    # result = ""
    # try:
    #     run()
    # except Exception as e:
    #     result = "测试中断，原因：%s" % e
    # else:
    #     result = "全双工半双工链路ASR测试已完成，结果请查看附件"
    # finally:
    #     nowdate = time.strftime('%Y-%m-%d')
    #     logpath = os.path.join(Project_path.log_path, "%s.log" % nowdate)
    #     logzip_path = os.path.join(Project_path.log_path, "%s.log.zip" % nowdate)
    #     Zipfile(logpath, logzip_path)
    #     mail = Mail()
    #     mail.creat_mail(result)
    #     mail.add_attach1(result_path)
    #     logsize = round(os.path.getsize(logzip_path) / float(1024 * 1024), 2)
    #     if logsize < 20:
    #         mail.add_attach1(logzip_path)
    #     mail.sent_mail()
