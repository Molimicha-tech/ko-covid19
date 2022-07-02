# encoding: utf-8
# get_similar_hashtags.py - Get the 10 most semantically similar topic tags for
# each tag, as well as edit the topic tags that are one-fifth of the word length away
# Copyright (c) 2020-2025 TIAN

from gensim.models import word2vec
import pandas as pd
import numpy as np


def edit_distance(word1, word2):
    len1 = len(word1)
    len2 = len(word2)
    dp = np.zeros((len1 + 1, len2 + 1))
    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            delta = 0 if word1[i - 1] == word2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j - 1] + delta, min(dp[i - 1][j] + 1, dp[i][j - 1] + 1))
    return dp[len1][len2]


# load model
model = word2vec.Word2Vec.load('.\\Data in the analysis process\\word2vecAll.model')

word_dic = pd.read_csv(".\\Data in the analysis process\\tag.csv")

result_df = pd.DataFrame(columns=["tag1", "tag2", "s"])

tags = word_dic["tag"].values

for i in range(0, len(tags) - 1):
    print(i)
    for j in range(i + 1, len(tags)):
        if edit_distance(tags[i], tags[j]) / len(tags[i]) < 0.2:
            result_df = result_df.append([{"tag1": tags[i], "tag2": tags[j]}], ignore_index=True)

# print(model.wv.vocab)
vocab = model.wv.vocab

for i in range(0, len(tags)):
    if tags[i] in vocab:
        res = model.most_similar(tags[i], topn=10)
        for j in res:
            if j[0] in tags and j[1] > 0.5:
                result_df = result_df.append([{"tag1": tags[i], "tag2": j[0], "s": j[1]}], ignore_index=True)
        print(i)
result_df.to_csv(".\\Data in the analysis process\\Most_similar_words.csv")