from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

from constants import DATA_PATH, SOURCE_FORMAT


def winddir_relative_arg_hours(begin_date, end_date):
    df = pd.read_csv(DATA_PATH + '_01.' + SOURCE_FORMAT, index_col='PCTimeStamp',
                     usecols=['PCTimeStamp', 'Amb_WindDir_Relative_Avg'])
    timeList = {}
    winddir = []
    hours = []
    for index, row in df.iterrows():
        time = datetime.strptime(str(index), '%Y-%m-%d %H:%M:%S')
        if begin_date < time < end_date:
            date = index.split(' ')
            hour = date[1].split(':')[0]
            if hour in timeList.keys():
                timeList[hour].append(float(row['Amb_WindDir_Relative_Avg']))
            else:
                timeList[hour] = [float(row['Amb_WindDir_Relative_Avg'])]
    for k, v in timeList.items():
        hours.append(k)
        winddir.append(sum(v) / len(v))
    plt.plot(hours, winddir)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
