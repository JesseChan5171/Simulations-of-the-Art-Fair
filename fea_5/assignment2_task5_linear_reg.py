from sklearn import linear_model
import statsmodels.api as sm
import pandas as pd

df = pd.read_csv("dataf.csv")

X = df[['bo_num','exp_pro', "exp_vis"]]
Y = df['total_tra']

print(X)
regr = linear_model.LinearRegression()
regr.fit(X, Y)
print('Intercept: \n', regr.intercept_)
print('Coefficients: \n', regr.coef_)

