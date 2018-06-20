import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from sklearn.metrics import precision_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score, StratifiedKFold, learning_curve

import warnings

warnings.filterwarnings('ignore')


train_df = pd.read_csv('data/train.csv')
test_df = pd.read_csv('data/test.csv')
combine_df = pd.concat([train_df, test_df])
train_df.groupby(train_df.Name.apply(lambda x: len(x)))['Survived'].mean().plot()


train_df.Cabin = train_df.Cabin.fillna('None')
train_df.groupby(train_df.Cabin.apply(lambda x: x[0]))['Survived'].mean().plot()
