from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

from constants import DATA_PATH, SOURCE_FORMAT, COLORS


################ Wind Direction Relative Avg. ########################
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


################ Wind Direction Relative Avg. Based on Hours ########################
def winddir_relative_avg_hours(begin_date, end_date):
    df = pd.read_csv(DATA_PATH + '_01.' + SOURCE_FORMAT, index_col='PCTimeStamp',
                     usecols=['PCTimeStamp', 'Amb_WindDir_Relative_Avg', 'HCnt_Avg_Run'])
    df = df[df["HCnt_Avg_Run"] >= 300]
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
    plt.xlabel("Hours")
    plt.ylabel("Rel. Wind Dir")
    plt.suptitle('winddir_relative_avg_hours')
    plt.savefig('winddir_relative_avg_hours.png')
    plt.show()


################ Wind Direction Relative Avg. For All Turbines ########################
def plotters1(begin_date, end_date, index, hcnt):
    if index < 10:
        file = DATA_PATH + '_0' + str(index) + '.' + SOURCE_FORMAT
    else:
        file = DATA_PATH + '_' + str(index) + '.' + SOURCE_FORMAT
    df = pd.read_csv(file,
                     usecols=['PCTimeStamp', 'Amb_WindDir_Relative_Avg', 'HCnt_Avg_Run'])
    df = df[df["HCnt_Avg_Run"] >= hcnt]
    df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'])
    df = df[(df["PCTimeStamp"] >= begin_date)]
    df = df[(df["PCTimeStamp"] <= end_date)]
    plt.scatter(df["PCTimeStamp"], df["Amb_WindDir_Relative_Avg"], color=COLORS[(index - 1) % 8], s=0.2)
    print("Turbine " + str(index) + " has finished")


def winddir_relative_avg_for_all_turbine(begin_date, end_date, hcnt):
    not_last_one = True
    index = 1
    while not_last_one:
        try:
            plotters1(begin_date, end_date, index, hcnt)
            index = index + 1
        except:
            not_last_one = False
    plt.xticks(rotation=90)
    plt.xlabel("Time")
    plt.ylabel("Rel. Wind Dir")
    plt.suptitle('winddir_relative_avg_for_all_turbine')
    plt.savefig('winddir_relative_avg_for_all_turbine.png')
    plt.show()

################ Power Curve ########################
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


###################### Wind Direction vs. Wind Speed #################
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
###################### Wind Direction Absolute Comprasion #################
def plotters2(begin_date, end_date, index):
    temp = []
    timeList = []
    if index < 10:
        file = DATA_PATH + '_0' + str(index) + '.' + SOURCE_FORMAT
    else:
        file = DATA_PATH + '_' + str(index) + '.' + SOURCE_FORMAT
    df = pd.read_csv(file, index_col='PCTimeStamp',
                     usecols=['PCTimeStamp', 'Amb_WindDir_Abs_Avg', 'HCnt_Avg_Run'])
    df = df[df["HCnt_Avg_Run"] >= 300]
    for i, row in df.iterrows():
        if begin_date < datetime.strptime(str(i), '%Y-%m-%d %H:%M:%S') < end_date:
            timeList.append(datetime.strptime(str(i), '%Y-%m-%d %H:%M:%S'))
            temp.append(float(row['Amb_WindDir_Abs_Avg']))
    plt.scatter(timeList, temp, color=COLORS[(index - 1) % 8], s=0.2)
    print("Tribune " + str(index) + " has finished")


def winddir_abs_comparison(begin_date, end_date):
    not_last_one = True
    index = 1
    while not_last_one:
        try:
            plotters2(begin_date, end_date, index)
            index = index + 1
        except:
            not_last_one = False
    plt.xticks(rotation=90)
    plt.xlabel("Time")
    plt.ylabel("Abs Wind Dir")
    plt.suptitle('winddir_abs_comparison')
    plt.savefig('winddir_abs_comparison.png')
    plt.show()

############## Variable Hcnt Figures ######################
def hcnt_avg_run(begin_date, end_date, hcnt):
    power_curve(begin_date, end_date, hcnt)
    winddir_relative_avg(begin_date, end_date, hcnt)
    winddir_relative_avg_for_all_turbine(begin_date, end_date, hcnt)




