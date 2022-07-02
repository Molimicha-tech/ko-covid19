from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import KFold
import numpy as np

from model_select import test_p
from Text2vec import text2vec

def ten_flod(ff,tags,P,R,F):
    kf = KFold(n_splits=10,shuffle=True,random_state=15).split(ff)
    for train_idx, valid_idx in kf:
        X_train = ff[train_idx]
        y_train = tags[train_idx]
        X_test = ff[valid_idx]
        y_test = tags[valid_idx]
        model = OneVsRestClassifier(MultinomialNB(alpha=0.2))
        print(len(train_idx),len(valid_idx))
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        p,l,r = test_p(predictions,y_test)
        print(p,l,r,2*p*r/(p+r))
        P.append(p)
        R.append(r)
        F.append(2*p*r/(p+r))
    return np.mean(P),np.mean(R),np.mean(F)

if __name__ == '__main__':
    P = []
    R = []
    F = []
    ff, tags, wait_data_index, wait_f, topics = text2vec()
    p,r,f = ten_flod(np.array(ff),tags,P,R,F)
    print("KNN result：P:%.03f,R:%.03f,F:%.03f"%(p,r,f))