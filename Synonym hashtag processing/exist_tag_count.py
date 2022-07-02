# exist_tag_count.py - Statistics on existing tags
# Copyright (c) 2020-2025 TIAN

import pandas as pd
from collections import Counter

data = pd.read_csv(".\\Data in the analysis process\\projectFilter_translated_0.csv")

all_tags = []
for line in data["topic"].values:
    if str(line) != "nan" and str(line) != "":
        tags = str(line).split(" ")
        all_tags.extend(tags)

result = Counter(all_tags)
d = sorted(result.items(), key=lambda x: x[1], reverse=True)

tag = pd.DataFrame({"tag": list(list(zip(*d))[0]), "count": list(list(zip(*d))[1])}, columns=["tag", "count"])

tag.to_csv(".\\Data in the analysis process\\tag.csv", index=False)
print("Finish!")