import sys
from sklearn import linear_model

print(sys.path)
###https://mp.weixin.qq.com/s?__biz=MzA4MjEyNTA5Mw==&mid=2652566667&idx=1&sn=cc9fe5dde35237b2f117ef46d409c705&chk
# sm=8464dcc1b31355d7f85ad8f5f889ca13e0737dc5b4f105468abe16f0c99cbf2314fd4b6edc7a&mpshare=1&scene=23&srcid=1101xfT5ohvNPyvVJY8kstVm#rd
# 普通最小二乘法

reg = linear_model.LinearRegression()
reg.fit([[0, 0], [1, 1], [2, 2]], [0, 1, 2])
coef = reg.coef_
print(coef)
print(reg.intercept_)
print(type(coef))

##ridge岭回归
# 缩减技术 解决矩阵不满秩 和过拟合
# 增加惩罚项 限制回归系数的绝对值
reg = linear_model.Ridge(alpha=.5)
reg.fit([[0, 0], [0, 0], [1, 1]], [0, .1, 1])
print(reg.coef_)

# 交叉验证
# 获取合适的惩罚系数
reg = linear_model.RidgeCV(alphas=[0.1, 0.2, 0.5, 0.7, 1.0, 10.0])
reg.fit([[0, 0], [0, 0], [1, 1]], [0, .1, 1])
print(reg.alpha_)

##lossa
##坐标下降算法coordinate descent
##惩罚项不是回归系数的二阶和而是绝对值的和
reg = linear_model.Lasso(alpha=0.1)
reg.fit([[0, 0], [1, 1]], [0, 1])

print(reg.coef_)
print(reg.intercept_)
reg.predict([[1, 1]])

##lossa交叉验证
reg = linear_model.LassoCV(alphas=[0.1, 0.0])
reg.fit([[0, 0], [1, 1], [2, 2]], [0, 1, 2])
print(reg.alpha_)

