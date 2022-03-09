from datetime import datetime
import matplotlib.pyplot as plt

import pandas as pd

from constants import DATA_PATH, SOURCE_FORMAT, COLORS


def plotters(begin_date, end_date, timeList, index):
    temp = []
    if index < 10:
        file = DATA_PATH + '_0' + str(index) + '.' + SOURCE_FORMAT
    else:
        file = DATA_PATH + '_' + str(index) + '.' + SOURCE_FORMAT
    df = pd.read_csv(file, index_col='PCTimeStamp',
                     usecols=['PCTimeStamp', 'Amb_WindDir_Abs_Avg'])
    if not timeList:
        for i, row in df.iterrows():
            if begin_date < datetime.strptime(str(i), '%Y-%m-%d %H:%M:%S') < end_date:
                timeList.append(datetime.strptime(str(i), '%Y-%m-%d %H:%M:%S'))
                temp.append(float(row['Amb_WindDir_Abs_Avg']))
        plt.scatter(timeList, temp, color=COLORS[(index-1) % 8])
        print("Tribune " + str(index) + " has finished")
    else:
        for i, row in df.iterrows():
            if begin_date < datetime.strptime(str(i), '%Y-%m-%d %H:%M:%S') < end_date:
                temp.append(float(row['Amb_WindDir_Abs_Avg']))
        try:
            plt.scatter(timeList, temp, color=COLORS[(index-1) % 8])
            print("Tribune " + str(index) + " has finished")
        except:
            print("Tribune " + str(index) + " has failed")


def winddir_abs_comparison(begin_date, end_date):
    not_last_one = True
    index = 1
    timeList = []
    while not_last_one:
        try:
            plotters(begin_date, end_date, timeList, index)
            index = index + 1
        except:
            not_last_one = False
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
