import pandas as pd
import numpy as np

tag_cluster = pd.read_csv(".\\Data in the analysis process\\data_analysis\\tag_cluster.csv")

data = pd.read_csv(".\\Data in the analysis process\\extractionResult_SVM.csv")
data = data[~(data['topic'].isnull())]

result = pd.DataFrame(columns=["tag", "cluster", "mounth", "count"])
tag_list = tag_cluster["tag"].values.tolist()
table = np.zeros((len(tag_list), 9))

data["year"] = data['createTime'].apply(lambda x: x[:4])
data["mounth"] = data["createTime"].apply(lambda x: x[5:6])
data.head()

for m in range(1, 10):
    for line in data[(data["year"] == "2020") & (data["mounth"] == str(m))]["topic"].values:
        tags = line.split(";")
        for item in tags:
            if item in tag_list:
                table[tag_list.index(item)][m - 1] += 1

for t in range(0, len(tag_list)):
    for m in range(0, 9):
        cluster = tag_cluster[tag_cluster["tag"] == tag_list[t]]["cluster"].values[0]
        result = result.append([{"tag": tag_list[t], "cluster": cluster, "mounth": m + 1, "count": table[t][m]}])

result.head()
result.to_csv(".\\Data in the analysis process\\data_analysis\\Cluster label statistics.csv", index=False)

g = result.groupby(by=['cluster', 'mounth']).agg({'count': np.mean})
h = g.reset_index()
h.to_csv(".\\Data in the analysis process\\data_analysis\\Category monthly average word frequency.csv", index=False)
print("Finish！")