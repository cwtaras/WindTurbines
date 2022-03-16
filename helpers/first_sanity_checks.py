from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

from constants import DATA_PATH, SOURCE_FORMAT, COLORS


# Wind speed-dependent table. Calculate the observed yaw
# misalignment for each wind speed and adjust each value in the table
# accordingly.
def speed_to_relative_avg(begin_date, end_date, hcnt):
    df = pd.read_csv(DATA_PATH + '_01.' + SOURCE_FORMAT,
                     usecols=['PCTimeStamp', 'Amb_WindDir_Relative_Avg', 'HCnt_Avg_Run', 'Amb_WindSpeed_Avg'])
    df = df[df["HCnt_Avg_Run"] >= hcnt]
    df["zscore"] = (df["Amb_WindDir_Relative_Avg"] - df["Amb_WindDir_Relative_Avg"].mean())/df["Amb_WindDir_Relative_Avg"].std(ddof=0)
    df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'])
    df = df[(df["PCTimeStamp"] >= begin_date) & (df["PCTimeStamp"] <= end_date) &
            (df["zscore"] > 2) & (df["Amb_WindSpeed_Avg"] > 3)]
    fig, ax = plt.subplots()
    df.plot("Amb_WindSpeed_Avg", "Amb_WindDir_Relative_Avg", kind='scatter', ax=ax, c='red', marker='x')
    plt.show()