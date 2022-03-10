from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

from constants import DATA_PATH, SOURCE_FORMAT

def winddir_abs_vs_windspeed(begin_date, end_date):
    df = pd.read_csv(DATA_PATH + '_01.' + SOURCE_FORMAT, index_col='PCTimeStamp',
                     usecols=['PCTimeStamp', 'Amb_WindSpeed_Avg', 'Amb_WindDir_Abs_Avg'])

    winddir = []
    windspeed = []
    timeList = []

    for index, row in df.iterrows():
        time = datetime.strptime(str(index), '%Y-%m-%d %H:%M:%S')
        if begin_date < time < end_date:
            windspeed.append(float(row['Amb_WindSpeed_Avg']))
            winddir.append(float(row['Amb_WindDir_Abs_Avg']))
            timeList.append(time)

    fig, ax = plt.subplots()
    ax.plot(timeList, winddir, color="red")
    ax.tick_params(axis='x',labelrotation=90)
    ax.set_xlabel("Time")
    ax.set_ylabel("Abs. Wind Dir", color="red")

    ax2 = ax.twinx()
    ax2.plot(timeList, windspeed, color="blue")
    ax2.set_ylabel("Wind Speed", color="blue")
    plt.suptitle('winddir_abs_vs_windspeed')
    plt.savefig('winddir_abs_vs_windspeed.png')
    plt.show()
