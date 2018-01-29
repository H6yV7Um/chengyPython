import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

from cy_kaggle import cy_titanic

features, x_train, y = cy_titanic.load_dataset()

remove_features_index = [0, 2, 7, 9]
features = np.delete(features, remove_features_index, axis=0)
x_train = np.delete(x_train, remove_features_index, axis=1)

params = {'male': '1', 'female': '0', 'S': '0', 'Q': '1', 'C': '2'}
col_index = [1, -1]
fixed_missing_X = cy_titanic.fix_missing(x_train, col_index, params)
y = y.astype(float)

x_shape = fixed_missing_X.shape
new_x = np.zeros((x_shape[0], x_shape[1] - 1))
for i in range(6):
    if i < 3:
        new_x[:, i] = fixed_missing_X[:, i]
    elif i == 3:
        new_x[:, i] = fixed_missing_X[:, i] + fixed_missing_X[:, i + 1]
    else:
        new_x[:, i] = fixed_missing_X[:, i + 1]

X_train, X_test, y_train, y_test = train_test_split(new_x, y, random_state=4)

param_grid = {'C': [1e2, 7e2, 1e4],
              'gamma': [0.0001, 0.0002, ]}
clf = GridSearchCV(SVC('rbf'), param_grid)
clf.fit(new_x, y)

print("Best estimator found by grid search:")
print(clf.best_estimator_)

score = cross_val_score(clf, fixed_missing_X, y, cv=5, scoring='accuracy')
print(score)
