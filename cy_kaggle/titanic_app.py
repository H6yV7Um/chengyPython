from cy_kaggle import cy_titanic
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

from sklearn import svm
import time

features, x_train, y = cy_titanic.load_dataset()

remove_features_index = [0, 2, 7, 9]
features = np.delete(features, remove_features_index, axis=0)
x_train = np.delete(x_train, remove_features_index, axis=1)

params = {'male': '1', 'female': '0', 'S': '0', 'Q': '1', 'C': '2'}
col_index = [1, -1]
fixed_missing_X = cy_titanic.fix_missing(x_train, col_index, params)

# 分割数据
X_train, X_test, y_train, y_test = train_test_split(fixed_missing_X, y, random_state=4)

param_grid = {'C': [4e2, 5e2, 6e2, 7e2, 8e2],
              'gamma': [0.001], }
t0 = time.time()
svc = svm.SVC(kernel='rbf', class_weight='balanced')
clf = GridSearchCV(svc, param_grid)
clf.fit(X_train, y_train)
print("done in %0.3fs" % (time.time() - t0))
print("Best estimator found by grid search:")
print(clf.best_estimator_)
### the best params is C=700
best_clf = clf.best_estimator_
score = clf.score(X_test, y_test)
print(score)

test_features, test_set = cy_titanic.load_testset()
remove_features_index = [0, 2, 7, 9]
test_f = np.delete(test_features, remove_features_index, axis=0)
test_x = np.delete(test_set, remove_features_index, axis=1)
params = {'male': '1', 'female': '0', 'S': '0', 'Q': '1', 'C': '2'}
col_index = [1, -1]
test_fixed_missing_X = cy_titanic.fix_missing(test_x, col_index, params)

predict_y=clf.predict(test_fixed_missing_X)

with open('data/new_svc_result.csv', 'w') as result_file:
    result_file.write("PassengerId,Survived" + "\n")
    for pid, flag in zip(test_set[:, 0], predict_y):
        result_file.write(pid + "," + str(int(flag)) + "\n")