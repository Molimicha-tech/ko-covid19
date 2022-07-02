# encoding = 'utf-8'
# hashtag_count.py - Tag extraction results tag statistics
# Copyright (c) 2020-2025 TIAN

import csv
import pandas as pd
from collections import Counter

with open(".\\Data in the analysis process\\extractionResult_SVM.csv", 'r', encoding='UTF-8') as csvfile1:
    reader1 = csv.reader(csvfile1)
    result1 = list(reader1)

all_tags = []

for line in result1:
    if str(line[1]) != "nan" and str(line[1]) != "":
        tags = str(line[8]).strip().split(";")
    all_tags = all_tags + tags

result = Counter(all_tags)
d = sorted(result.items(), key=lambda x: x[1], reverse=True)

tag = pd.DataFrame({"tag": list(list(zip(*d))[0]), "count": list(list(zip(*d))[1])}, columns=["tag", "count"])

tag.to_csv(".\\Data in the analysis process\\tag_result.csv", index=False)
print("Finish!")