# encoding: utf-8
# select_core_tags.py - Statistics of synonymous substitution and
# word frequency, and then the selection of core topic tags.
# Calculate the proportion of cumulative word frequency in Excel
# and select the core hashtags
# Copyright (c) 2020-2025 TIAN

import pandas as pd
from collections import Counter


def count():
    data = pd.read_csv(".\\Data in the analysis process\\projectFilter_translated_0_cleaned_std.csv")

    all_tags = []
    for line in data["topic"].values:
        if str(line) != "nan" and str(line) != "":
            tags = str(line).split(";")
            all_tags.extend(tags)

    result = Counter(all_tags)
    d = sorted(result.items(), key=lambda x: x[1], reverse=True)

    tag = pd.DataFrame({"tag": list(list(zip(*d))[0]), "count": list(list(zip(*d))[1])}, columns=["tag", "count"])

    tag.to_csv(".\\Data in the analysis process\\tag_std_0.csv", index=False)
    print("Finish!")

def count_core_tags():
    data = pd.read_csv(".\\Data in the analysis process\\projectFilter_translated_0_cleaned_std.csv")
    yuanshitag = pd.read_csv(".\\Data in the analysis process\\frequent_tag.csv")
    tagset = yuanshitag["tag"].values

    data_std = pd.DataFrame()

    for item in data.values:
        tags = str(item[8]).split(";")

        tags_std = []
        for i in tags:
            if i in tagset:
                tags_std.append(i)

        data_std = data_std.append([{
            'id': item[0],
            'name': item[1],
            'description': item[2],
            'len_description': item[3],
            'url': item[4],
            'star': item[5],
            'fork': item[6],
            'issues': item[7],
            'topic': ";".join(tags_std),
            'readMe': item[9],
            'len_readMe': item[10],
            'length': item[11],
            'introduction': item[12],
            'owner': item[13],
            'ownerId': item[14],
            'ownerType': item[15],
            'createTime': item[16],
            'language': item[17],
            'lang_detail': item[18],
            'langId_description': item[19],
            'langId_readMe': item[20],
            'size': item[21]}], ignore_index=True)

    data_std.to_csv(".\\Data in the analysis process\\projectFilter_translated_0_cleaned_std_selected.csv", index=False)
    print("Finish!")

if __name__ == '__main__':
    count()
    count_core_tags()