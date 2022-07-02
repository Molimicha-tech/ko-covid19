import pandas as pd
import itertools

def load_data(path):
    result=[]
    data = pd.read_csv(path)
    for line in data.values:
        #line=line.strip('\n')
        if str(line[8])=="nan":continue
        topics = line[8].split(";")
        if "covid 19" in topics:
            topics.remove("covid 19")
        if len(topics)>1:
            result.append(topics)
    return result

def code_translate(dataset):
    items = set(itertools.chain(*dataset))
    str_to_index = {}
    index_to_str = {}
    for index, item in enumerate(items):
        str_to_index[item] = index
        index_to_str[index] = item
    print("字符串到编号:", list(str_to_index.items())[:5])
    print("编号到字符串:", list(index_to_str.items())[:5])

    for i in range(len(dataset)):
        for j in range(len(dataset[i])):
            dataset[i][j] = str_to_index[dataset[i][j]]
    for i in range(10):
        print(i + 1, dataset[i], sep="->")
    return index_to_str

def buildC1(dataset):
    item1=set(itertools.chain(*dataset))
    return [frozenset([i]) for i in item1]

def ck_to_lk(dataset,ck,min_support):
    support={}
    for row in dataset:
        for item in ck:
            if item.issubset(row):
                support[item]=support.get(item,0)+1
    total=len(dataset)
    return {k:v/total for k,v in support.items() if v/total>=min_support}

def lk_to_ck(lk_list):
    ck=set()
    lk_size=len(lk_list)
    if lk_size>1:
        k=len(lk_list[0])
        for i,j in itertools.combinations(range(lk_size),2):
            t=lk_list[i]|lk_list[j]
            if len(t)==k+1:
                ck.add(t)
    return ck

def get_L_all(dataset,min_support):
    c1=buildC1(dataset)
    L1=ck_to_lk(dataset,c1,min_support)
    L_all=L1
    Lk=L1
    while len(Lk)>1:
        lk_key_list=list(Lk.keys())
        ck=lk_to_ck(lk_key_list)
        Lk=ck_to_lk(dataset,ck,min_support)
        print("loading......")
        if len(Lk)>0:
            L_all.update(Lk)
        else:
            break
        if len(list(Lk.keys())[0])>=2:break
    return L_all

def rules_from_item(item):
    #定义规则左侧的列表
    left=[]
    for i in range(1,len(item)):
        left.extend(itertools.combinations(item,i))
    return [(frozenset(le),frozenset(item.difference(le))) for le in left]

def rules_from_L_all(L_all,min_confidence):
    rules=[]
    for lk in L_all:
        if len(lk)>1:
            rules.extend(rules_from_item(lk))
    result=[]
    for left,right in rules:
        support=L_all[left|right]
        confidence=support/L_all[left]
        lift=confidence/L_all[right]
        if confidence>=min_confidence:
            result.append({"左侧":left,"右侧":right,"支持度":support,"置信度":confidence,"提升度":lift})
    return result

def apriori(dataset,min_support,min_confidence):
    L_all=get_L_all(dataset,min_support)
    rules=rules_from_L_all(L_all,min_confidence)
    return rules

def change(item, index_to_str):
    li=list(item)
    for i in range(len(li)):
        li[i]=index_to_str[li[i]]
    return li

def id2tag():
    # 读取核心主题标签
    f = open(".\\Data in the analysis process\\data_analysis\\class1.txt")
    line = f.readline()
    key_tag = []
    while line:
        key_tag.append(line.replace("\n", ""))
        line = f.readline()
    f.close()

    clean_rules = pd.DataFrame(columns=["左侧", "右侧", "关联规则", "支持度", "置信度", "提升度"])

    df = pd.DataFrame(rules)
    df = df.reindex(["左侧", "右侧", "支持度", "置信度", "提升度"], axis=1)
    df["左侧"] = df["左侧"].apply(change)
    df["右侧"] = df["右侧"].apply(change)

    rule_list = []

    for line in df.values:
        r = line[0] + line[1]
        flag = True
        for i in list(set(r)):
            if i not in key_tag:
                flag = False
        if flag == False:
            continue
        if set(r) in rule_list:
            continue
        else:
            rule_list.append(set(r))
            clean_rules = clean_rules.append([{"左侧": ";".join(line[0]),
                                               "右侧": ";".join(line[1]),
                                               "关联规则": ";".join(line[0]) + " => " + ";".join(line[1]),
                                               "支持度": line[2], "置信度": line[3], "提升度": line[4]}], ignore_index=True)

    df.to_csv(".\\Data in the analysis process\\data_analysis\\Association rules_1.csv", index=False)
    clean_rules.to_csv(".\\Data in the analysis process\\data_analysis\\Association rules_clean_1.csv", index=False)
    print("Finish!")

def to_vosViwer():
    chart_data = pd.read_csv(".\\Data in the analysis process\\data_analysis\\Association rules_clean_1.csv")
    class_data = pd.read_csv(".\\Data in the analysis process\\data_analysis\\map-exist-1.csv")

    # 点
    node = pd.DataFrame(columns=["Id", "Label", "cluster", "weight"])
    # 边
    edge = pd.DataFrame(columns=["Source", "Target", "weight"])

    n = {}
    for line in chart_data.values:
        item = line[0].split(";") + line[1].split(";")
        for i in item:
            if i in n.keys():
                n[i] += 1
            else:
                n[i] = 1
    Id = 0
    for item in n.keys():
        node = node.append([{"Id": Id,
                             "Label": item,
                             "cluster": class_data[class_data["label"] == item]["cluster"].values[0],
                             "weight": n[item]}], ignore_index=True)
        Id += 1
    e = {}
    for line in chart_data.values:
        left = line[0].split(";")
        right = line[1].split(";")
        for l in left:
            for r in right:
                ee1 = str(node[node["Label"] == l]["Id"].values[0]) + ";" + str(
                    node[node["Label"] == r]["Id"].values[0])
                ee2 = str(node[node["Label"] == r]["Id"].values[0]) + ";" + str(
                    node[node["Label"] == l]["Id"].values[0])
                if ee1 in e.keys():
                    e[ee1] += 1
                elif ee2 in e.keys():
                    e[ee2] += 1
                else:
                    e[ee1] = line[5]
    for item in e.keys():
        edge = edge.append([{"Source": item.split(";")[0],
                             "Target": item.split(";")[1],
                             "weight": e[item]}], ignore_index=True)

    node.to_csv(".\\Data in the analysis process\\data_analysis\\Association rules_node_1.csv", index=False)
    edge.to_csv(".\\Data in the analysis process\\data_analysis\\Association rules_edge_1.csv", index=False)
    print("Finish!")

if __name__ == '__main__':
    dataset = load_data(".\\Data in the analysis process\\extractionResult_SVM.csv")
    print(len(dataset))
    print(dataset[:10])
    index_to_str = code_translate(dataset)
    rules = apriori(dataset, 0.002, 0.2)
    to_vosViwer()


