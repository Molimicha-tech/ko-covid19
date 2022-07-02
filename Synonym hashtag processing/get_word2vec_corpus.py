# get_word2vec_corpus.py - Generating a word vector training corpus
# Copyright (c) 2020-2025 TIAN

import csv
import nltk
from nltk.tokenize import MWETokenizer
import pandas as pd


def segWordsCorpus():
    with open('.\\Data in the analysis process\\tag_std_0.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile);
        result = list(reader);
    data = pd.read_csv('.\\Data in the analysis process\\introduction.csv')#源文件路径（.csv）

    #readme = pd.DataFrame(columns=['id','name','description','url','star','fork','issues','topic','readMe','introduction','owner','ownerId','ownerType','createTime','language','lang_detail','langId'])
    f = open(".\\Data in the analysis process\\Word vector training corpus.txt","w",encoding="utf-8")

    corpusList = [];
    phraseList = [];
    for item in result:
        listWord = str(item[0]).split(" ");
        corpusList.append(tuple(listWord));
        phrase = listWord[0];
        i = 1
        while i < int(len(listWord)):
            phrase = phrase + '-' + listWord[i];
            i = i + 1;
        phraseList.append(phrase);

    tokenizer = MWETokenizer(corpusList, separator='-')

    i = 0;
    print(len(data.values))
    for item in data.values:
        content = str(item[0]);
        # print(content);
        seg_result = tokenizer.tokenize(nltk.word_tokenize(content.lower()));
        words = '';

        for word in seg_result:
            words += word.lower()
            words += " "
        i = i + 1
        print(i)
        f.write(words+"\n")

if __name__ == '__main__':
    segWordsCorpus()