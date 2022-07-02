# encoding: utf-8
# model_select.py - Model select
# Copyright (c) 2020-2025 TIAN

from sklearn import metrics

def test_p(predictions, y_test):
    p = metrics.precision_score(y_test, predictions, average='samples')
    r = metrics.recall_score(y_test, predictions, average='samples')
    f1 = metrics.f1_score(y_test, predictions, average='samples')

    return p, r, f1