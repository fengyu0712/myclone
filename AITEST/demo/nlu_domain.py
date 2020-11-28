from common.http_request_new import Request
from common import read_xls_news
import Project_path
# import json
import os

excel_path = os.path.join(Project_path.TestData_path, 'nlu.xlsx')  # 映射关系表，命令词

result_path = os.path.join(Project_path.TestResult_path, 'result.xlsx')


def get_data(path, booknames=None):
    r = read_xls_news.Read_xls(path)
    if booknames is None:
        booknames = r.get_sheet_names()
    test_data = []
    for i in range(len(booknames)):
        data = r.read_data(booknames[i], start_line=2)
        test_data += data
        # print(data)
        i += 1
    w = r.copy_book()
    r.save_write(w, result_path)
    return test_data


def nlu(utterance):
    url = "https://nlu.sit.aimidea.cn:22012/nlu/v1"
    # data=dict()
    data = {
        "currentUtterance": "请马上关机",
        "sourceDevice": "空调",
        "multiDialog": "true",
        "slotMiss": "true",
        "suite": [
            "default"
        ],
        "deviceId": "4311026980750221",
        "userGroup": "meiju",
        "userGroupCredential": "b82063f4-d39b-4940-91c3-5b67d741b4d3",
        "customDeviceNames": "",
        "customRoomNames": ""
    }
    data["currentUtterance"] = utterance
    result = Request().requests(url, data, 'post')
    nlu_result = result.json()
    return nlu_result


def run():
    bookname = 'NLU'
    booknames = [bookname]
    test_data = get_data(excel_path, booknames)
    rr = read_xls_news.Read_xls(result_path)
    rw = rr.copy_book()
    for i in range(500):

        utterance = test_data[i][0]
        print(str(i)+":"+utterance)
        nlu_result = nlu(utterance)
        domain = nlu_result['intent']['domain']
        # intent_map={'Scenario':'场景','DeviceControl':'控制','Kitchen':'菜谱','general':'通用领域'}
        if domain != "general":
            result = "Pass"
        else:
            print(nlu_result)
            result = "Fail"
        rr.write_linedata(rw, i + 1, [domain, result], sheetname=bookname, col=1)
        rr.save_write(rw, result_path)


if __name__ == "__main__":
    run()
