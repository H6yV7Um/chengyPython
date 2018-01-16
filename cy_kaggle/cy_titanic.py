import csv

import numpy as np
from sklearn.preprocessing import Imputer


def load_testset():
    dataset = []
    with open('/Users/nali/IdeaProjects/chengxiaoyPython/cy_kaggle/data/test.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            dataset.append(row)
    dataset = np.array(dataset)
    features = dataset[0, :]
    x_train = dataset[1:, :]
    return features, x_train


def load_dataset():
    dataset = []
    with open('/Users/nali/IdeaProjects/chengxiaoyPython/cy_kaggle/data/train.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            dataset.append(row)
    dataset = np.array(dataset)
    y = dataset[1:, 1]
    features = np.delete(dataset[0, :], 1, axis=0)
    x_train = np.delete(dataset[1:, :], 1, axis=1)
    return features, x_train, y


def fix_missing(dataset, cols, params):
    key_set = set(params.keys())
    for row_index in range(len(dataset)):
        for col in cols:
            if dataset[row_index, col] in key_set:
                dataset[row_index, col] = params[dataset[row_index, col]]
    dataset = np.where(dataset != '', dataset, np.nan)
    dataset = dataset.astype(float)
    imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
    return imp.fit_transform(dataset)


def auto_norm(dataset):
    """
    将数据集归一化
    减去最小值后除以均值
    :param dataset:
    :return:
    """
    min_val = dataset.min(0)
    max_val = dataset.max(0)
    range_val = max_val - min_val
    m = dataset.shape[0]
    normDataSet = np.zeros(np.shape(dataset))
    # 数组每个元素减去该列的最小值
    normDataSet = dataset - np.tile(min_val, (m, 1))
    # 再除以范围获得归一化矩阵
    normDataSet = normDataSet / np.tile(range_val, (m, 1))
    return normDataSet, range_val, min_val
