# encoding = 'utf-8'
# text_preprocessing.py - Delete stop words and other special characters
# except English and numbers in the text
# Copyright (c) 2020-2025 TIAN

import csv
import nltk
from nltk.tokenize import MWETokenizer
import re
import pandas as pd


def segWords():
    # read data
    data = pd.read_csv('.\\Data in the analysis process\\projectFilter_translated_0.csv')  # 源文件路径（.csv）

    readme = pd.DataFrame(columns=data.columns.values)
    # read stop words
    stopList = open('.\\Data in the analysis process\\stopWords.txt', mode='r', encoding='utf-8')
    stopWords = []
    for line in stopList:
        stopWords.append(line.strip())
    if "on" in stopWords:
        print("123")

    # remove stop words
    i = 0;
    print(len(data.values))
    for item in data.values:
        content = str(item[12])
        words = '';
        strinfo = re.compile('["‘\+\-\[\]_\s`~!@#$^&?*()=|{}:;,./<>\'\\\\]')
        content = strinfo.sub(' ', content)
        seg_result = content.split(" ")

        for word in seg_result:
            word = word.strip()
            if word.lower() in stopWords:
                continue;
            else:
                an = re.search('[`~!@#$^&*%()=|{}:;,.<>《》/?！￥…（）【】‘；:”“\'。，、？]', word)
                ann = re.search('[\u4e00-\u9fa5]', word)
                en = re.search('[\u0041-\u005A,\u0061-\u007A,0-9]', word)
                if an or ann: continue
                if not en: continue
                if word.isdigit() or word == " ": continue
                words += word.lower().strip()
                words += " "
        i = i + 1
        print(i)
        # if words != '':
        readme = readme.append([{'id': item[0],
                                 'name': item[1],
                                 'description': item[2],
                                 'len_description': item[3],
                                 'url': item[4],
                                 'star': item[5],
                                 'fork': item[6],
                                 'issues': item[7],
                                 'topic': item[8],
                                 'readMe': item[9],
                                 'len_readMe': item[10],
                                 'length': item[11],
                                 'introduction': words.strip(),
                                 'owner': item[13],
                                 'ownerId': item[14],
                                 'ownerType': item[15],
                                 'createTime': item[16],
                                 'language': item[17],
                                 'lang_detail': item[18],
                                 'langId_description': item[19],
                                 'langId_readMe': item[20],
                                 'size': item[21]}], ignore_index=True)
    readme.to_csv('.\\Data in the analysis process\\projectFilter_translated_0_cleaned.csv', index=False)