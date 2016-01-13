from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import AdaBoostRegressor
from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline


class Regressor(BaseEstimator):

    def __init__(self):
        base_estimator = RandomForestRegressor(n_estimators=10)
        self.clf = AdaBoostRegressor(base_estimator=base_estimator, n_estimators=100)

    def fit(self, X, y):
        self.clf.fit(X, y)

    def predict(self, X):
        return self.clf.predict(X)
