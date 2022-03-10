import csv
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

from constants import DATA_PATH, SOURCE_FORMAT


def power_curve(begin_date, end_date, hcnt):
    df = pd.read_csv(DATA_PATH + '_01.' + SOURCE_FORMAT, index_col='PCTimeStamp',
                     usecols=['PCTimeStamp', 'Grd_Prod_Pwr_Avg', 'Amb_WindSpeed_Avg', 'HCnt_Avg_Run'])
    wind_speed = []
    power = []
    df = df[df["HCnt_Avg_Run"] >= hcnt]
    for index, row in df.iterrows():
        if begin_date < datetime.strptime(str(index), '%Y-%m-%d %H:%M:%S') < end_date:
            wind_speed.append(float(row['Amb_WindSpeed_Avg']))
            power.append(float(row['Grd_Prod_Pwr_Avg']))
    plt.scatter(wind_speed, power, s=0.1, color='b')
    plt.xlabel("Wind Speed")
    plt.ylabel("Power")
    plt.suptitle('power_curve')
    plt.savefig('power_curve.png')
    plt.show()

