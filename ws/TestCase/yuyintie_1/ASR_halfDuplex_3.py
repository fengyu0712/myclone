# -*- coding: UTF-8 -*-
from Common import log, read_xls_news
from Common import mypyaudio
# from Common.SimplifyASR import simplify_asr
import os
import re
import time
import serial
import serial.tools.list_ports
import Project_path
import multiprocessing
import threading

excel_path = os.path.join(Project_path.test_date_path, 'asr_case.xls')  # 映射关系表，命令词
wakeup_path = os.path.join(Project_path.test_audio_path, "002M30_36_010003.wav")  # #唤醒文件：你好小美的音频文件
cmd_path = "E:\\音频资源\\015"

asr_mid_pattern = "text\":	\"(.*)\"[\\s\\S]*\"info\":	\"(.*)\""
wakeup_sign = "ev\":	\"wake up\""
in_fullduplex_sign = "full duplex mode"
asr_pattern = "text\":	\"(.*)\""

serial_list = {"COM5": [115200, "\"ev\":	\"wake up\"", "语音贴2.0"],
               "COM7": ["921600", "\"ev\":	\"wake up\"", "语音贴1.0"]}


#

def myserial(baudrate, serialname):
    plist = list(serial.tools.list_ports.comports())
    if len(plist) <= 0:
        print("The Serial port can't find!")
    else:
        plist_0 = list(plist[0])
        if serialname is None:
            serialname = plist_0[0]
        serialFd = serial.Serial(serialname, baudrate, timeout=60)
        print("check which port was really used >", serialFd.name)
        if serialFd.isOpen():
            print("Serial port open success")
        else:
            print("Serial port open failed")


def recvcmd(serialFd, Log, timeout=None):
    if timeout is None:
        timeout = 10
    all_data = ""
    start_time = time.time()
    while True:
        end_time = time.time()
        if end_time - start_time < timeout:
            data = serialFd.read(serialFd.inWaiting())
            data = data.decode(encoding='utf-8', errors='ignore')
            if data:
                Log.debug(data)
                all_data = all_data + data
        else:
            break
    return all_data


def recv_data(serialFd, Log, pattern_list=None, checktime=None):
    if checktime is None:
        checktime = 10
    if pattern_list is None:
        pattern_list = []
    new_pattern_list = list(pattern_list)
    result_data = []
    start_time = time.time()
    while time.time() < start_time + checktime:
        data = serialFd.read(serialFd.inWaiting())
        data = data.decode(encoding='utf-8', errors='ignore')
        print(data)
        if data:
            # print(data)
            Log.debug(data)
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


# s = MySerial(baudrate="961200")


def wakeup(s, Log):
    if os.path.exists(wakeup_path):
        for i in range(3):
            mypyaudio.play_audio(wakeup_path)
            wakeup_result = recv_data(s,Log,pattern_list=[wakeup_sign], checktime=5)
            if not wakeup_result[0]:
                Log.error("连续%s次未唤醒" % (i + 1))
                i += 1
            else:
                return True
    else:
        raise ("唤醒的音频文件不存在..." + wakeup_path)


def get_data(path, result_path, booknames=None):
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


def t2(baudrate, serialname, product, logpath):
    global test_num, asr_succese_num, total_num
    Log = log.Logger(logpath)
    Log.info("=======================%s半双工链路ASR识别率测试========================" % product)
    # s = MySerial(buatrate, Log, serialname)
    print(1)
    s = serial.Serial(serialname, baudrate, timeout=60)
    print(2)
    # s = recvcmd(baudrate, Log, serialname, timeout=None)
    now = time.strftime('%Y-%m-%d-%H-%M-%S')
    result_path = os.path.join(Project_path.test_result_path, '%s-半双工ASRm45度噪音识别率测试--result%s.xls' % (product, now))
    bookname = '015'
    booknames = [bookname]
    print(1)
    test_data = get_data(excel_path, result_path, booknames=booknames)
    for i in range(len(test_data)):
        Log.info("开始第%s条测试：%s" % (i + 1, test_data[i][:2]))
        except_value = test_data[i][1]
        wav_path = os.path.join(cmd_path, test_data[i][0] + ".wav")  # wav 路径
        test_result = "Fail"
        iswakeup = wakeup(s, Log)
        if not iswakeup:
            Log.error("連續三次未喚醒！")
        else:
            test_num += 1
            Log.info("唤醒成功，即将进入播放音频进行ASR测试")
            rr = read_xls_news.Read_xls(result_path)
            rw = rr.copy_book()
            Log.info("开始播放测试音频【%s】" % wav_path)
            mypyaudio.play_audio(wav_path)
            asr_log =recvcmd(s,Log,10)
            asr_result = re.findall(asr_mid_pattern, asr_log)
            if asr_result:
                asr = asr_result[0]
                mid = asr_result[1]
                if except_value == asr:
                    test_result = "Pass"
                    asr_succese_num += 1
            else:
                asr = "False"
                mid = "False"
            asr_succese_rate = "%.2f%%" % (asr_succese_num / test_num * 100)
            Log.info("[%s]:用例【%s】ASR识别结果：%s" % (product, test_data[i][:2], asr))
            Log.info("[%s]:用例【%s】ASR测试结果：%s" % (product, test_data[i][:2], test_result))
            Log.info(
                "[%s]当前一共执行测试【%s次】，正常执行【%s】，其中ASR识别正确【%s次】,识别率为：【%s】" % (
                    product, i + 1, test_num, asr_succese_num, asr_succese_rate))
            rr.write_linedata(rw, i + 2, [asr, test_result, mid], sheetname=bookname, col=3)
            rr.write_onlydata(rw, 0, 1, asr_succese_rate, sheetname=bookname)
            rr.save_write(rw, result_path)


if __name__ == "__main__":
    from multiprocessing import Process
    now = time.strftime('%Y-%m-%d-%H-%M')
    serial_list = {"COM3": ["115200", "语音贴1.0"],"COM4": ["1500000", "3308"]}
    # serial_list = {"COM3": ["115200", "语音贴1.0"]}


    # print(len(serial_list))
    logpath1 = os.path.join(Project_path.log_path, "%s_%s.log" % ("语音贴1.0", now))
    logpath2 = os.path.join(Project_path.log_path, "%s_%s.log" % ("3308", now))
    result = []
    q = multiprocessing.Pool()
    q.apply_async(t2,args=("115200", "COM3", "语音贴1.0", logpath1,))
    q.apply_async(t2, args=("1500000", "COM4", "3308", logpath1,))
    # for key in serial_list.keys():
    #     listinfo = serial_list[key]
    #     protuct = listinfo[1]
    #     logpath = os.path.join(Project_path.log_path, "%s_%s.log" % (protuct, now))
    #     # s =MySerial(listinfo[0], Log, serialname=key)
    #     # serialFd = serial.Serial(key, listinfo[0], timeout=60)
    #     q.apply_async(t2, args=(listinfo[0], key, listinfo[1], logpath,))
    q.close()
    q.join()
    # threadlist = []
    # for key in serial_list.keys():
    #     listinfo=serial_list[key]
    #     protuct = listinfo[1]
    #     # serialFd = serial.Serial(key, listinfo[0], timeout=60)
    #     logpath = os.path.join(Project_path.log_path, "%s_%s.log" % (protuct, now))
    #     t = threading.Thread(target=t2, args=(listinfo[0], key, listinfo[1], logpath))
    #     threadlist.append(t)
    #     # t.start()
    #     # t.join()
    # for t in threadlist:
    #     t.start()
    #     time.sleep(0.5)
    #
    # for t in threadlist:
    #     t.join()

    # run()

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
