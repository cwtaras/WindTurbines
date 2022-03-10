from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

from constants import DATA_PATH, SOURCE_FORMAT


def winddir_relative_avg(begin_date, end_date, hcnt):
    df = pd.read_csv(DATA_PATH + '_01.' + SOURCE_FORMAT, index_col='PCTimeStamp',
                     usecols=['PCTimeStamp', 'Amb_WindDir_Relative_Avg', 'HCnt_Avg_Run'])
    df = df[df["HCnt_Avg_Run"] >= hcnt]
    timeList = []
    winddir = []
    for index, row in df.iterrows():
        time = datetime.strptime(str(index), '%Y-%m-%d %H:%M:%S')
        if begin_date < time < end_date:
            timeList.append(time)
            winddir.append(float(row['Amb_WindDir_Relative_Avg']))
    plt.scatter(timeList, winddir, s=0.2)
    plt.xticks(rotation=90)
    plt.xlabel("Time")
    plt.ylabel("Rel. Wind Dir")
    plt.suptitle('winddir_relative_avg')
    plt.savefig('winddir_relative_avg.png')
    plt.show()


