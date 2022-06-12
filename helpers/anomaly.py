import numpy as np
import pandas as pd
import scipy as stats
from scipy.stats import chi2
import matplotlib
import math
import matplotlib.pyplot as plt
from numpy import percentile
from pyod.models.cblof import CBLOF
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN


from constants import DATA_PATH, SOURCE_FORMAT, COLORS, DATA_PATH

def isolation_forest(begin_date, end_date):
    df = pd.read_csv(DATA_PATH + '_01.' + SOURCE_FORMAT,
                     usecols=['PCTimeStamp', 'Grd_Prod_Pwr_Avg', 'Amb_WindSpeed_Avg', 'HCnt_Avg_Run'])
    df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'])
    df = df[(df["PCTimeStamp"] >= begin_date) & (df["PCTimeStamp"] <= end_date)]
    df = df[df["HCnt_Avg_Run"] >= 300]
    isolation_forest = IsolationForest(n_estimators=100)
    isolation_forest.fit(df['Amb_WindSpeed_Avg'].values.reshape(-1, 1))
    xx = np.linspace(df['Amb_WindSpeed_Avg'].min(), df['Amb_WindSpeed_Avg'].max(), len(df)).reshape(-1, 1)
    anomaly_score = isolation_forest.decision_function(xx)
    outlier = isolation_forest.predict(xx)
    plt.figure(figsize=(10, 4))
    plt.plot(xx, anomaly_score, label='anomaly score')
    plt.fill_between(xx.T[0], np.min(anomaly_score), np.max(anomaly_score),
                     where=outlier == -1, color='r',
                     alpha=.4, label='outlier region')
    plt.legend()
    plt.ylabel('anomaly score')
    plt.xlabel('Amb_WindSpeed_Avg')
    plt.show()

# !!! doesnt work  !!!
def cluster_based(begin_date, end_date):
    df = pd.read_csv(DATA_PATH + '_01.' + SOURCE_FORMAT,
                     usecols=['PCTimeStamp', 'Grd_Prod_Pwr_Avg', 'Amb_WindSpeed_Avg', 'HCnt_Avg_Run'])
    df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'])
    df = df[(df["PCTimeStamp"] >= begin_date) & (df["PCTimeStamp"] <= end_date)]
    df = df[["Grd_Prod_Pwr_Avg", "Amb_WindSpeed_Avg"]]
    outliers_fraction = 0.01
    xx, yy = np.meshgrid(np.linspace(0, 1, 100), np.linspace(0, 1, 100))
    clf = CBLOF(contamination=outliers_fraction, check_estimator=False, random_state=0)
    clf.fit(df)
    scores_pred = clf.decision_function(df) * -1
    y_pred = clf.predict(df)
    n_inliers = len(y_pred) - np.count_nonzero(y_pred)
    n_outliers = np.count_nonzero(y_pred == 1)
    print(y_pred)

    print('OUTLIERS:', n_outliers, 'INLIERS:', n_inliers)


def dbscan(begin_date, end_date):
    df = pd.read_csv(DATA_PATH + '_01.' + SOURCE_FORMAT,
                     usecols=['PCTimeStamp', 'Grd_Prod_Pwr_Avg', 'Amb_WindSpeed_Avg', 'HCnt_Avg_Run'])
    df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'])
    df = df[(df["PCTimeStamp"] >= begin_date) & (df["PCTimeStamp"] <= end_date)]
    df = df[df["HCnt_Avg_Run"] >= 300]
    df = df[["Grd_Prod_Pwr_Avg", "Amb_WindSpeed_Avg"]]
    dbscan = DBSCAN(eps=1.8, min_samples=3).fit(df)
    labels = dbscan.labels_
    plt.scatter(df["Amb_WindSpeed_Avg"], df['Grd_Prod_Pwr_Avg'], c=labels, cmap="plasma")  # plotting the clusters
    plt.xlabel("Amb_WindSpeed_Avg")  # X-axis label
    plt.ylabel('Grd_Prod_Pwr_Avg')  # Y-axis label
    plt.show()

def mahalanobis(begin_date, end_date):
    df = pd.read_csv(DATA_PATH + '_01.' + SOURCE_FORMAT,
                     usecols=['PCTimeStamp', 'Grd_Prod_Pwr_Avg', 'Amb_WindDir_Relative_Avg', 'HCnt_Avg_Run', 'Rtr_RPM_Avg'])
    df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'])
    df = df[(df["PCTimeStamp"] >= begin_date) & (df["PCTimeStamp"] <= end_date)]
    df = df[df["HCnt_Avg_Run"] >= 300]
    df = df[["Grd_Prod_Pwr_Avg", "Amb_WindDir_Relative_Avg", "Rtr_RPM_Avg"]]

    y_mu = df - df.mean()
    cov = np.cov(df.values.T)
    inv_covmat = np.linalg.inv(cov)
    left = np.dot(y_mu, inv_covmat)
    mahal = np.dot(left, y_mu.T)
    df['Mahalanobis'] = mahal.diagonal()
    df['p'] = 1 - chi2.cdf(df['Mahalanobis'], 3)
    df = df[df["p"] <= 0.1]
    print(df)
