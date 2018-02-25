import csv

import numpy as np
from sklearn.ensemble import RandomForestRegressor
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


def set_missing_ages(df):
    """
    使用随机森林预测缺失的年龄
    :param df:
    :return:
    """

    # 把已有的数值型特征取出来丢进Random Forest Regressor中
    age_df = df[['Age', 'Fare', 'Parch', 'SibSp', 'Pclass']]

    # 乘客分成已知年龄和未知年龄两部分
    known_age = age_df[age_df.Age.notnull()].as_matrix()
    unknown_age = age_df[age_df.Age.isnull()].as_matrix()

    # y即目标年龄
    y = known_age[:, 0]

    # X即特征属性值
    X = known_age[:, 1:]

    # fit到RandomForestRegressor之中
    rfr = RandomForestRegressor(random_state=0, n_estimators=2000, n_jobs=-1)
    rfr.fit(X, y)

    # 用得到的模型进行未知年龄结果预测
    predictedAges = rfr.predict(unknown_age[:, 1::])

    # 用得到的预测结果填补原缺失数据
    df.loc[(df.Age.isnull()), 'Age'] = predictedAges

    return df, rfr


def set_Cabin_type(df):
    df.loc[(df.Cabin.notnull()), 'Cabin'] = "Yes"
    df.loc[(df.Cabin.isnull()), 'Cabin'] = "No"
    return df
