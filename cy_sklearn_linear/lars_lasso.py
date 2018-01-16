import numpy as np
import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn import linear_model

diabetes = datasets.load_diabetes()
X = diabetes.data
y = diabetes.target
print("Computing regularization path using the LARS ...")

alphas, _, coefs = linear_model.lars_path(X, y, method='lasso', verbose=True)

xx = np.sum(np.abs(coefs.T), axis=1)
xx /= xx[-1]

plt.plot(xx, coefs.T)
ymin, ymax = plt.ylim()
plt.vlines(xx, ymin, ymax, linestyle='dashed')
plt.xlabel('|coef| / max|coef|')
plt.ylabel('Coefficients')
plt.title('LASSO Path')
plt.axis('tight')
plt.show()
