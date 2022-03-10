import csv
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

from constants import DATA_PATH, SOURCE_FORMAT, COLORS


def plotters(begin_date, end_date, index, hcnt):
    temp = []
    timeList = []
    if index < 10:
        file = DATA_PATH + '_0' + str(index) + '.' + SOURCE_FORMAT
    else:
        file = DATA_PATH + '_' + str(index) + '.' + SOURCE_FORMAT
    df = pd.read_csv(file, index_col='PCTimeStamp',
                     usecols=['PCTimeStamp', 'Amb_WindDir_Relative_Avg', 'HCnt_Avg_Run'])
    df = df[df["HCnt_Avg_Run"] >= hcnt]
    for i, row in df.iterrows():
        if begin_date < datetime.strptime(str(i), '%Y-%m-%d %H:%M:%S') < end_date:
            timeList.append(datetime.strptime(str(i), '%Y-%m-%d %H:%M:%S'))
            temp.append(float(row['Amb_WindDir_Relative_Avg']))
    plt.scatter(timeList, temp, color=COLORS[(index - 1) % 8], s=0.2)
    print("Turbine " + str(index) + " has finished")


def winddir_relative_avg_for_all_turbine(begin_date, end_date, hcnt):
    not_last_one = True
    index = 1
    while not_last_one:
        try:
            plotters(begin_date, end_date, index, hcnt)
            index = index + 1
        except:
            not_last_one = False
    plt.xticks(rotation=90)
    plt.xlabel("Time")
    plt.ylabel("Rel. Wind Dir")
    plt.suptitle('winddir_relative_avg_for_all_turbine')
    plt.savefig('winddir_relative_avg_for_all_turbine.png')
    plt.show()
