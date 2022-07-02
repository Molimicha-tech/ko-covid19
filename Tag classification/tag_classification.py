# encoding: utf-8
# tag_classification.py - Hashtag classification
# Copyright (c) 2020-2025 TIAN

from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
import pandas as pd
import numpy as np

from Text2vec import text2vec

model = OneVsRestClassifier(OneVsRestClassifier(SVC(class_weight="balanced",kernel="rbf")),
                                    n_jobs=-1)
ff, tags, wait_data_index, wait_f, topics = text2vec()
model.fit(ff,tags)

data_source = pd.read_csv(
    ".\\Data in the analysis process\\projectFilter_translated_0_cleaned_std_selected.csv")  # 源文件路径（.csv）
values = data_source.values

for i in range(len(wait_data_index)):
    index = wait_data_index[i]
    print(index)
    predictions = model.predict(np.array([wait_f[i]]))
    r = []
    for j in range(len(predictions[0])):
        if predictions[0][j] == 1:
            r.append(topics[j])

    # print(data_source.iloc[int(index),8])
    values[index, 8] = ";".join(r)
    print(";".join(r))
OK = pd.DataFrame(values, columns=list(data_source.columns))
OK.to_csv(".\\Data in the analysis process\\extractionResult_SVM.csv", index=False)