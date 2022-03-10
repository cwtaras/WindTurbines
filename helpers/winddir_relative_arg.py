from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

from constants import DATA_PATH, SOURCE_FORMAT


def winddir_relative_arg(begin_date, end_date):
    df = pd.read_csv(DATA_PATH + '_01.' + SOURCE_FORMAT, index_col='PCTimeStamp',
                     usecols=['PCTimeStamp', 'Amb_WindDir_Relative_Avg'])
    timeList = []
    winddir = []
    for index, row in df.iterrows():
        time = datetime.strptime(str(index), '%Y-%m-%d %H:%M:%S')
        if begin_date < time < end_date:
            timeList.append(time)
            winddir.append(float(row['Amb_WindDir_Relative_Avg']))
    plt.plot(timeList, winddir)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
