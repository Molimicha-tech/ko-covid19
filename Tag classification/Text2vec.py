# encoding: utf-8
# Text2vec.py - Text vectorization
# Copyright (c) 2020-2025 TIAN

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2  # 卡方检验
import numpy as np
from sklearn import preprocessing

def text2vec():
    data_df = pd.read_csv(
        ".\\Data in the analysis process\\projectFilter_translated_0_cleaned_std_selected.csv")  # 源文件路径（.csv）
    # data_df=data_df[~(data_df['introduction'].isnull())] #删掉空行
    # data_df=data_df[~(data_df['topic'].isnull())] #删掉空行

    introduction_list = data_df["introduction"].values.tolist()
    url_list = data_df["url"].values.tolist()

    train_data_index = data_df[(data_df["tag_count"]) > 0].index.tolist()
    wait_data_index = data_df[(data_df["tag_count"]) <= 0].index.tolist()

    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 1),
                                 token_pattern=r"\b[\u0041-\u005A,\u0061-\u007A,0-9]{0,1}[\u0041-\u005A,\u0061-\u007A]{1,20}[\u0041-\u005A,\u0061-\u007A,-,0-9]{0,2}\b",
                                 analyzer="word",
                                 max_features=5000)
    introduction_matrix = vectorizer.fit_transform(introduction_list)
    r_m = introduction_matrix.todense()

    train_data = []
    wait_data = []
    train_label = []
    for index in train_data_index:
        train_data.append(np.array(r_m[index])[0])
        train_label.append(data_df.iloc[index, 8])
    for index in wait_data_index:
        wait_data.append(np.array(r_m[index])[0])
    train_data = np.array(train_data)
    wait_data = np.array(wait_data)


    def count_topic(topics):
        topic_set = []
        for i in topics:
            for j in i.split(";"):
                topic_set.append(j)
        topic = [i for i in topic_set if topic_set.count(i) > 0]
        return list(set(topic))


    tags = []
    topics = count_topic(train_label)
    length = len(topics)
    for i in train_label:  # data_df["topic"].values.tolist():
        tag = np.zeros(length)
        for j in i.split(";"):
            if j in topics:
                tag[topics.index(j)] = 1
        tags.append(tag)
    tags = np.array(tags)
    print(tags)
    print(length)

    features = []
    for i in range(len(tags[0])):
        target = tags[:, i]
        model1 = SelectKBest(chi2, k=30)
        model1 = model1.fit(train_data, target)
        # print(model1.get_support())
        features.append(model1.get_support())

    features = np.array(features)
    feature = []
    for i in range(len(features[0])):
        f = features[:, i]
        if True in f:
            feature.append(i)

    np.savez_compressed(".\\Data in the analysis process\\feature_index", wait_data)

    feature_names = vectorizer.get_feature_names()
    feature_name = []
    ff = []
    wait_f = []
    for i in feature:
        feature_name.append(feature_names[i])
        ff.append(train_data[:, i])
        wait_f.append(wait_data[:, i])
    print(feature_name)
    ff = np.array(ff)
    ff = ff.transpose()
    wait_f = np.array(wait_f)
    wait_f = wait_f.transpose()

    scaler = preprocessing.MinMaxScaler()
    ff = scaler.fit_transform(ff)
    print(ff)

    np.savez_compressed(".\\Data in the analysis process\\wait_data", wait_f)
    return ff, tags, wait_data_index, wait_f, topics