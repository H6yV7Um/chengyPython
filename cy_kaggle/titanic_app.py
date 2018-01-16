from cy_kaggle import cy_titanic
import numpy as np

features, x_train, y = cy_titanic.load_dataset()

remove_features_index = [0, 2, 7, 9]
features = np.delete(features, remove_features_index, axis=0)
x_train = np.delete(x_train, remove_features_index, axis=1)


params = {'male': '1', 'female': '0', 'S': '0', 'Q': '1', 'C': '2'}
col_index = [1, -1]
fixed_missing_X = cy_titanic.fix_missing(x_train, col_index, params)

cy_titanic.auto_norm(fixed_missing_X)