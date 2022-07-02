# encoding: utf-8
# replace_hashtags.py - Use the synonym dictionary to replace the synonym
# hashtags in the original hashtags
# Copyright (c) 2020-2025 TIAN

import pandas as pd

data = pd.read_csv(".\\Data in the analysis process\\projectFilter_translated_0_cleaned.csv")
sametag = pd.read_csv(".\\Data in the analysis process\\Thesaurus.csv")
yuanshitag = pd.read_csv(".\\Data in the analysis process\\tag.csv")
tagset = yuanshitag["tag"].values

sametagdic = dict(zip(sametag["label"].values, sametag["replace by"].values))

data_std = pd.DataFrame()

for item in data.values:
    tags = str(item[8]).split(" ")
    #if str(line[4]) != 'nan':
    #    tags.append(line[4].lower().replace(" ",""))
    for i in tags:
        if i not in tagset:
            tags.remove(i)
            continue
        if i in sametagdic.keys():
            tags[tags.index(i)] = sametagdic[i]
    for i in tags:
        tags[tags.index(i)] = tags[tags.index(i)].replace("-"," ")
    tags_std = list(set(tags))
    #data_std = data_std.append([{'url':line[0],'topic':";".join(tags_std),'introduction':line[2],'createTime':str(line[3])[:10],'lang':line[4],'tagNum':len(tags_std),'star':line[5]}],ignore_index=True)
    data_std = data_std.append([{
        'id':item[0],
        'name':item[1],
        'description':item[2],
          'len_description':item[3],
          'url':item[4],
          'star':item[5],
          'fork':item[6],
          'issues':item[7],
          'topic':";".join(tags_std),
          'readMe':item[9],
          'len_readMe':item[10],
          'length':item[11],
          'introduction':item[12],
          'owner':item[13],
          'ownerId':item[14],
          'ownerType':item[15],
          'createTime':item[16],
          'language':item[17],
          'lang_detail':item[18],
          'langId_description':item[19],
          'langId_readMe':item[20],
          'size':item[21]}],ignore_index=True)

data_std.to_csv(".\\Data in the analysis process\\projectFilter_translated_0_cleaned_std.csv",index=False)
print("Finish!")