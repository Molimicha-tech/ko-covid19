# encoding = 'utf-8'
# Co-word_clustering.py - Co-word clustering
# Copyright (c) 2020-2025 TIAN

import pandas as pd
import numpy as np
import math
from sklearn.cluster import SpectralClustering
import sklearn.metrics

def Generate_coword_matrix():
    f = open(".\\Data in the analysis process\\data_analysis\\main_class.txt")
    line = f.readline()
    key_tag = []
    while line:
        key_tag.append(line.replace("\n", ""))
        line = f.readline()
    f.close()

    word_set = pd.read_csv(".\\Data in the analysis process\\extractionResult_SVM.csv")
    word_set = word_set[~(word_set['topic'].isnull())]
    # sametag = pd.read_csv("E:\\新冠数据\\数据530\\标签抽取\\标签共现分析\\同义替换.csv")
    # sametagdic = dict(zip(sametag["label"].values, sametag["replace by"].values))
    tag_set = pd.read_csv(".\\Data in the analysis process\\tag_result.csv")
    tag_set_dic = dict(zip(tag_set["tag"].values, tag_set["count"].values))
    # key_tag = tag_set[tag_set["count"]>1]["tag"].values.tolist()


    table = np.zeros((len(key_tag), len(key_tag)))

    bian_set = {}

    for i in word_set["topic"].values:
        w = i.split(";")
        # for item in range(0,len(w)):
        #    if w[item] in sametagdic.keys():
        #        w[item]= sametagdic[w[item]]
        # w = list(set(w))
        for j in range(0, len(w) - 1):
            if w[j] not in key_tag: continue
            for k in range(j + 1, len(w)):
                if w[k] not in key_tag: continue
                table[key_tag.index(w[j])][key_tag.index(w[k])] += 1
                table[key_tag.index(w[k])][key_tag.index(w[j])] += 1

    for m in range(0, len(key_tag)):
        table[m][m] = tag_set_dic[key_tag[m]]
        # table[m][m] = 0

    network = pd.DataFrame(table)

    network.columns = key_tag

    network.to_csv(".\\Data in the analysis process\\data_analysis\\Co-occurrence-table-exist.csv", index=False)
    print("Finish")

    # Ochiia
    s_table = np.zeros((len(key_tag), len(key_tag)))
    for j in range(0, len(key_tag) - 1):
        print("正在处理……")
        for k in range(j + 1, len(key_tag)):
            s = table[j][k] / (math.sqrt(table[j][j]) * math.sqrt(table[k][k]))
            # s = table[j][k]/(table[j][j]+table[k][k]-table[j][k])
            s_table[j][k] = s
            s_table[k][j] = s

    for m in range(0, len(key_tag)):
        s_table[m][m] = 1

    s_network = pd.DataFrame(s_table)

    s_network.columns = key_tag
    s_network.to_csv(".\\Data in the analysis process\\data_analysis\\s-table-manual.csv", index=False)
    print("Finish")
    return s_table,table,key_tag

def ac(k,dist_matrix):
    y_pred = SpectralClustering(k, affinity='precomputed', assign_labels='discretize').fit_predict(dist_matrix)
    # y_pred = AffinityPropagation(random_state=15,affinity='precomputed',preference=-1).fit_predict(dist_matrix)
    # print(list(y_pred))
    # print(list(y_pred).count(0))
    print(k)
    print("n_clusters=", k, "score:", sklearn.metrics.calinski_harabasz_score(dist_matrix, y_pred))


def get_cluster_num():
    s_table = pd.read_csv(".\\Data in the analysis process\\data_analysis\\s-table-manual.csv")
    dist_matrix = s_table.values

    for k in range(2, 16):
        ac(k, dist_matrix)

def Clustering(s_table,table,key_tag):
    # s_table = pd.read_csv("C:\\Users\\Administrator\\Desktop\\s-table-manual.csv")
    # dist_matrix = s_table.values
    otable = pd.read_csv(".\\Data in the analysis process\\data_analysis\\s-table-manual.csv")
    ctable = otable.values
    tag_set = pd.read_csv(".\\Data in the analysis process\\tag_result.csv")
    tag_set_dic = dict(zip(tag_set["tag"].values, tag_set["count"].values))

    y_pred = SpectralClustering(4, affinity='precomputed', assign_labels='discretize').fit_predict(ctable)
    print(y_pred)
    print("n_clusters=", 4, "score:", sklearn.metrics.calinski_harabasz_score(ctable, y_pred))

    tag = list(s_table.columns)

    # create vosViewer file
    vmap = pd.DataFrame(columns=['id', 'label', 'cluster', 'weight'])
    biantable = pd.DataFrame(columns=["source", "aim", "w"])
    for item in tag:
        index = tag.index(item)
        vmap = vmap.append(
            {'id': index, 'label': item, 'cluster': y_pred[index] + 1, 'weight': tag_set_dic[key_tag[index]]},
            ignore_index=True)
    vmap.to_csv(".\\Data in the analysis process\\data_analysis\\map-exist-1.csv", index=False)

    for i in range(0, len(tag) - 1):
        for j in range(i + 1, len(tag)):
            if table[i][j] != 0:
                biantable = biantable.append({"source": i, "aim": j, "w": ctable[i][j]}, ignore_index=True)
    biantable.to_csv(".\\Data in the analysis process\\data_analysis\\network-exist-1.csv", index=False)
    print("Finish!")

if __name__ == '__main__':
    s_table,table,key_tag = Generate_coword_matrix()
    get_cluster_num()
    Clustering(s_table,table,key_tag)