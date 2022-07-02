# translate.py - Translate data from other languages into English
# Copyright (c) 2020-2025 TIAN

import urllib.request
import urllib.parse
import json
import hashlib
import time
import pandas as pd
import csv

encoding = 'utf-8'
salt = '666'
appid =  ""
secret_key = ""

REQUEST_FAILED = -1

settings_regex = r"\s*\'.+\'\s*=>\s*.+"


def getMD5(content):
    m2 = hashlib.md5()
    m2.update(content.encode(encoding))
    return m2.hexdigest()


def getTranslateResponce(url, data):
    data = urllib.parse.urlencode(data).encode('utf-8')
    response = urllib.request.urlopen(url, data)
    return response.read().decode('utf-8')


def trans(content):
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    data = {}
    data['appid'] = appid
    data['salt'] = salt
    data['from'] = 'auto'
    data['to'] = 'en'
    data['q'] = content
    data['sign'] = getMD5(appid + content + salt + secret_key)
    # time.sleep(1)
    html = getTranslateResponce(url, data)
    target = json.loads(html)

    if target.get('error_code', REQUEST_FAILED) != REQUEST_FAILED:
        print('本次请求失败，原因为：', target['error_msg'])
        return "failfailfail"
    return target['trans_result'][0]['dst']


exist = pd.read_csv(".\\Data in the analysis process\\projectFilter_translated.csv")
ok_id = exist["id"].tolist()
# print(ok_id)

f = pd.read_excel('.\\Data in the analysis processl\\projectFilter.xlsx', sheet_name='项目筛选', header=0)
wait_id = f["id"].tolist()

result = []
fr = open(".\\Data in the analysis process\\projectFilter_translated.csv", 'a+', encoding='utf-8', newline='')
csv_writer = csv.writer(fr)

need_id = set(wait_id) - set(ok_id)
print(need_id)
print(len(ok_id))
print(len(wait_id))

for line in f.values:
    # print(line[0])
    if line[0] in need_id:
        print(line[0])
        if line[19] != 'en':
            if line[2] == "":
                content = "空"
            else:
                content = line[2]
            content = str(content).replace("\n", "").replace("\r", "")
            etext = trans(content)
            time.sleep(1.2)
        else:
            etext = str(line[2])
        if line[20] != 'en':
            if line[9] == "":
                content1 = "空"
            else:
                content1 = line[9]
            content1 = str(content1).replace("\n", "").replace("\r", "")
            etext1 = trans(content1)
            time.sleep(1)
        else:
            etext1 = str(line[9])
        if etext == "failfailfail" or etext1 == 'failfailfail':
            continue;
        if etext == "nan":
            etext = ''
        if etext1 == "nan":
            etext1 = ''
        introduction = etext + " " + etext1
        csv_writer.writerow(
            [line[0], line[1], etext, line[3], line[4], line[5], line[6], line[7], line[8], etext1, line[10],
             len(introduction), introduction, line[13], line[14], line[15], line[16], line[17], line[18], line[19],
             line[20], line[21]])
        time.sleep(1)
    # print(etext)
fr.close()

print("Finish")