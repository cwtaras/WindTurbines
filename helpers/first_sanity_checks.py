import pickle
import time
import matplotlib.pyplot as plt
import pandas as pd
from openpyxl import Workbook

import plotly.express as px

from constants import DATA_PATH, SOURCE_FORMAT, COLORS, DATA_PATH_EFE
pd.set_option('display.max_columns', None)

# Wind speed-dependent table. Calculate the observed yaw
# misalignment for each wind speed and adjust each value in the table
# accordingly.
# 1 years data
#speed_to_relative_avg(begin_date, end_date, hcnt, main_df, ('_0' + str(i)), sanity_naming)
def speed_to_relative_avg(begin_date, end_date, hcnt, turbineNo, sanity_naming=None, df=None):
    before = time.time()
    if df is None:
        try:
            df = pickle.load(open(f"pickles/{str(begin_date.strftime('%Y%b%d'))}_{str(end_date.strftime('%Y%b%d'))}_speed_relative_avg_{turbineNo}.pickle", "rb"))
        except (OSError, IOError, EOFError) as e:
            df = pd.read_csv(DATA_PATH_EFE + turbineNo + '.' + SOURCE_FORMAT,
                             usecols=['PCTimeStamp', 'Amb_WindDir_Relative_Avg', 'HCnt_Avg_Run', 'Amb_WindSpeed_Avg', 'Grd_Prod_Pwr_Avg','Rtr_RPM_Avg', 'Nac_Temp_Avg', 'Amb_Temp_Avg'])
            df = df[df["HCnt_Avg_Run"] >= hcnt]
            means = df[["Amb_WindSpeed_Avg", "Amb_WindDir_Relative_Avg"]].groupby(["Amb_WindSpeed_Avg"]).mean()
            means.columns = ['mean_speed']
            std = df[["Amb_WindSpeed_Avg", "Amb_WindDir_Relative_Avg"]].groupby(["Amb_WindSpeed_Avg"]).std()
            std.columns = ['std_speed']
            df = df.join(means, on='Amb_WindSpeed_Avg', how="left")
            df = df.join(std, on='Amb_WindSpeed_Avg', how="left")
            df["zscore_speed"] = (df["Amb_WindDir_Relative_Avg"] - df["mean_speed"]) / df["std_speed"]
            df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'])
            df = df[(df["PCTimeStamp"] >= begin_date) & (df["PCTimeStamp"] <= end_date) &
                    (abs(df["zscore_speed"]) > 3.75) & (df["Amb_WindSpeed_Avg"] > 5)]
            df = df[["Amb_WindSpeed_Avg", "Amb_WindDir_Relative_Avg", "mean_speed", "std_speed","zscore_speed", 'Grd_Prod_Pwr_Avg', "PCTimeStamp", 'Rtr_RPM_Avg','Nac_Temp_Avg', 'Amb_Temp_Avg']]
            pickle.dump(df, open(f"pickles/{str(begin_date.strftime('%Y%b%d'))}_{str(end_date.strftime('%Y%b%d'))}_speed_relative_avg_{turbineNo}.pickle", "wb"))
            fig, ax = plt.subplots()
            df.plot("Amb_WindSpeed_Avg", "Amb_WindDir_Relative_Avg", kind='scatter', ax=ax, c='red', marker='x')
            df.plot("Amb_WindSpeed_Avg", "mean_speed", kind='scatter', ax=ax, c='blue', marker='x')
            df.plot("Amb_WindSpeed_Avg", "std_speed", kind='scatter', ax=ax, c='green', marker='x')
            plt.show()
    else:
        try:
            df = pickle.load(open(f"pickles/{str(begin_date.strftime('%Y%b%d'))}_{str(end_date.strftime('%Y%b%d'))}_{sanity_naming}_{turbineNo}.pickle", "rb"))
        except (OSError, IOError, EOFError) as e:
            means = df[["Amb_WindSpeed_Avg", "Amb_WindDir_Relative_Avg"]].groupby(["Amb_WindSpeed_Avg"]).mean()
            means.columns = ['mean_speed']
            std = df[["Amb_WindSpeed_Avg", "Amb_WindDir_Relative_Avg"]].groupby(["Amb_WindSpeed_Avg"]).std()
            std.columns = ['std_speed']
            df = df.join(means, on='Amb_WindSpeed_Avg', how="left")
            df = df.join(std, on='Amb_WindSpeed_Avg', how="left")
            df["zscore_speed"] = (df["Amb_WindDir_Relative_Avg"] - df["mean_speed"]) / df["std_speed"]
            df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'])
            df = df[(df["PCTimeStamp"] >= begin_date) & (df["PCTimeStamp"] <= end_date) &
                    (abs(df["zscore_speed"]) > 5) & (df["Amb_WindSpeed_Avg"] > 5)]
            df = df[["Amb_WindSpeed_Avg", "Amb_WindDir_Relative_Avg", "mean_speed", "std_speed","zscore_speed", 'Grd_Prod_Pwr_Avg', "PCTimeStamp", "Rtr_RPM_Avg",'Nac_Temp_Avg', 'Amb_Temp_Avg']]
            pickle.dump(df, open(f"pickles/{str(begin_date.strftime('%Y%b%d'))}_{str(end_date.strftime('%Y%b%d'))}_{sanity_naming}_{turbineNo}.pickle", "wb"))
    df['turbine_no'] = turbineNo
    end = time.time()
    print("finished in:" + str(end-before))
    return df

# 1 year interval 2020-1-1
# All turbines are taken consideration and if some different relative average, it can be seem.
def all_turbines_yaw_misaligment(begin_date, end_date, sanity_naming=None, df=None):
    # master df
    if df is None:
        try:
            df = pickle.load(open(f"pickles/{str(begin_date.strftime('%Y%b%d'))}_{str(end_date.strftime('%Y%b%d'))}_{sanity_naming}.pickle", "rb"))
            f, (ax1) = plt.subplots(nrows=1, ncols=1)
            ax1.set_title('Errors')
            ax1.set_ylabel('Yaw Misalignment')
            ax1.set_xlabel('Time')
            ax1.scatter(df.index.values, df["Amb_WindDir_Relative_Avg"], c='red')
            ax1.plot(df.index.values, df["average_power"], c='blue')
        except (OSError, IOError, EOFError) as e:
            f, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
            ax1.set_title('16 turbines')
            ax2.set_title('Errors')
            ax2.set_xlabel('Time')
            ax2.set_ylabel('Yaw Misalignment')
            df = pd.read_csv(DATA_PATH_EFE + '_01.' + SOURCE_FORMAT,
                             usecols=['PCTimeStamp', 'Amb_WindDir_Relative_Avg', 'HCnt_Avg_Run'])
            df = df[df["HCnt_Avg_Run"] >= 300]
            df = df[["PCTimeStamp","Amb_WindDir_Relative_Avg"]]
            df["Amb_WindDir_Relative_Avg"] = pd.to_numeric(df["Amb_WindDir_Relative_Avg"], downcast="float")
            df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'])
            df = df[(begin_date <= df['PCTimeStamp']) & (df['PCTimeStamp'] <= end_date)]
            ax1.scatter(df["PCTimeStamp"], df["Amb_WindDir_Relative_Avg"], color=COLORS[(1) % 8], s=0.2)
            # df = df[begin_date <= pd.to_datetime(df['PCTimeStamp'])]
            # df = df[pd.to_datetime(df['PCTimeStamp']) <= end_date]
            df['turbine_no'] = "_01"

            #for other turbines
            for i in range(2, 17):
                if i < 10:
                    file = DATA_PATH_EFE + '_0' + str(i) + '.' + SOURCE_FORMAT
                else:
                    file = DATA_PATH_EFE + '_' + str(i) + '.' + SOURCE_FORMAT

                df_temp = pd.read_csv(file,
                                      usecols=['PCTimeStamp', 'Amb_WindDir_Relative_Avg', 'HCnt_Avg_Run'])

                df_temp = df_temp[df_temp["HCnt_Avg_Run"] >= 300]
                df_temp["Amb_WindDir_Relative_Avg"] = pd.to_numeric(df_temp["Amb_WindDir_Relative_Avg"], downcast="float")
                df_temp = df_temp[["PCTimeStamp", "Amb_WindDir_Relative_Avg"]]
                df_temp['PCTimeStamp'] = pd.to_datetime(df_temp['PCTimeStamp'])
                df_temp = df_temp[(begin_date <= df_temp['PCTimeStamp']) & (df_temp['PCTimeStamp'] <= end_date)]
                if i < 10:
                    df_temp['turbine_no'] = ('_0' + str(i))
                else:
                    df_temp['turbine_no'] = ('_' + str(i))
                ax1.scatter(df_temp["PCTimeStamp"], df_temp["Amb_WindDir_Relative_Avg"], color=COLORS[(i - 1) % 8], s=0.2)
                df = pd.concat([df, df_temp], axis=0)
                print(str(i) + "   finished")
            avg_df = df[["PCTimeStamp", "Amb_WindDir_Relative_Avg"]].groupby(df['PCTimeStamp']).agg(
                average_power=pd.NamedAgg(column="Amb_WindDir_Relative_Avg", aggfunc="mean"),
                standart_deviaton=pd.NamedAgg(column="Amb_WindDir_Relative_Avg", aggfunc="std"))
            df.set_index('PCTimeStamp', inplace=True)
            df = pd.merge(df, avg_df, left_index=True, right_index=True, how='left')
            df["zscore"] = (df["Amb_WindDir_Relative_Avg"] - df["average_power"]) / df[
                "standart_deviaton"]
            df = df[(abs(df["zscore"]) > 3.7)]
            pickle.dump(df, open(f"pickles/{str(begin_date.strftime('%Y%b%d'))}_{str(end_date.strftime('%Y%b%d'))}_{sanity_naming}.pickle", "wb"))
            ax2.scatter(df.index.values, df["Amb_WindDir_Relative_Avg"], c='red')
            ax2.plot(df.index.values, df["average_power"], c='blue')
    else:
        try:
            df = pickle.load(open(
                f"pickles/{str(begin_date.strftime('%Y%b%d'))}_{str(end_date.strftime('%Y%b%d'))}_{sanity_naming}.pickle",
                "rb"))
            f, (ax1) = plt.subplots(nrows=1, ncols=1)
            ax1.set_title('Errors')
            ax1.scatter(df.index.values, df["Amb_WindDir_Relative_Avg"], c='red')
            ax1.scatter(df.index.values, df["average_misalignment"], c='blue')
        except (OSError, IOError, EOFError) as e:
            f, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
            ax1.set_title('16 turbines')
            ax2.set_title('Errors')
            avg_df = pd.read_csv(DATA_PATH_EFE + '_01.' + SOURCE_FORMAT,
                             usecols=['PCTimeStamp', 'Amb_WindDir_Relative_Avg', 'HCnt_Avg_Run'])
            avg_df = avg_df[avg_df["HCnt_Avg_Run"] >= 300]
            avg_df = avg_df[["PCTimeStamp", "Amb_WindDir_Relative_Avg"]]
            avg_df["Amb_WindDir_Relative_Avg"] = pd.to_numeric(avg_df["Amb_WindDir_Relative_Avg"], downcast="float")
            avg_df['PCTimeStamp'] = pd.to_datetime(avg_df['PCTimeStamp'])
            avg_df = avg_df[(begin_date <= avg_df['PCTimeStamp']) & (avg_df['PCTimeStamp'] <= end_date)]
            ax1.scatter(avg_df["PCTimeStamp"], avg_df["Amb_WindDir_Relative_Avg"], color=COLORS[(1) % 8], s=0.2)
            # df = df[begin_date <= pd.to_datetime(df['PCTimeStamp'])]
            # df = df[pd.to_datetime(df['PCTimeStamp']) <= end_date]

            # for other turbines
            for i in range(2, 17):
                if i < 10:
                    file = DATA_PATH_EFE + '_0' + str(i) + '.' + SOURCE_FORMAT
                else:
                    file = DATA_PATH_EFE + '_' + str(i) + '.' + SOURCE_FORMAT

                df_temp = pd.read_csv(file,
                                      usecols=['PCTimeStamp', 'Amb_WindDir_Relative_Avg', 'HCnt_Avg_Run'])

                df_temp = df_temp[df_temp["HCnt_Avg_Run"] >= 300]
                df_temp["Amb_WindDir_Relative_Avg"] = pd.to_numeric(df_temp["Amb_WindDir_Relative_Avg"],
                                                                    downcast="float")
                df_temp = df_temp[["PCTimeStamp", "Amb_WindDir_Relative_Avg"]]
                df_temp['PCTimeStamp'] = pd.to_datetime(df_temp['PCTimeStamp'])
                df_temp = df_temp[(begin_date <= df_temp['PCTimeStamp']) & (df_temp['PCTimeStamp'] <= end_date)]
                ax1.scatter(df_temp["PCTimeStamp"], df_temp["Amb_WindDir_Relative_Avg"], color=COLORS[(i - 1) % 8],
                            s=0.2)
                avg_df = pd.concat([avg_df, df_temp], axis=0)
                print(str(i) + "   finished")
            avg_df = avg_df[["PCTimeStamp", "Amb_WindDir_Relative_Avg"]].groupby(avg_df['PCTimeStamp']).agg(
                average_misalignment=pd.NamedAgg(column="Amb_WindDir_Relative_Avg", aggfunc="mean"),
                std_misalignment=pd.NamedAgg(column="Amb_WindDir_Relative_Avg", aggfunc="std"))
            if 'PCTimeStamp' != df.index.name:
                df.set_index('PCTimeStamp', inplace=True)
            df = pd.merge(df, avg_df, left_index=True, right_index=True, how='left')
            df["zscore"] = (df["Amb_WindDir_Relative_Avg"] - df["average_misalignment"]) / df[
                "std_misalignment"]
            df = df[(abs(df["zscore"]) > 3.2)]
            pickle.dump(df, open(
                f"pickles/{str(begin_date.strftime('%Y%b%d'))}_{str(end_date.strftime('%Y%b%d'))}_{sanity_naming}.pickle",
                "wb"))
            ax2.scatter(df.index.values, df["Amb_WindDir_Relative_Avg"], c='red', s=0.5)
            ax2.scatter(df.index.values, df["average_misalignment"], c='blue')
    plt.gcf().autofmt_xdate()
    plt.show()
    return df

def turbine_yaw_avg_comprasion(begin_date, end_date):
    dfs_lst = []
    for i in range(1, 17):
        if i < 10:
            file = DATA_PATH_EFE + '_0' + str(i) + '.' + SOURCE_FORMAT
        else:
            file = DATA_PATH_EFE + '_' + str(i) + '.' + SOURCE_FORMAT

        df = pd.read_csv(file, usecols=['PCTimeStamp', 'Amb_WindDir_Relative_Avg', 'HCnt_Avg_Run'])
        df = df[df["HCnt_Avg_Run"] >= 300]
        df = df[["PCTimeStamp", "Amb_WindDir_Relative_Avg"]]
        df["Amb_WindDir_Relative_Avg"] = pd.to_numeric(df["Amb_WindDir_Relative_Avg"], downcast="float")
        df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'])
        df = df[(begin_date <= df['PCTimeStamp']) & (df['PCTimeStamp'] <= end_date)]
        dfs_lst.append(df)
        print(str(i) + "   finished")

    master_df = pd.concat(dfs_lst, axis=0)
    master_df = master_df.groupby(master_df['PCTimeStamp']).mean()
    for df in dfs_lst:
        df = df.groupby(df['PCTimeStamp']).mean()
        df.reset_index(inplace=True)
    master_df.reset_index(inplace=True)

    turb_dict = {}
    for i in range(16):
        val = 0
        for index, row in master_df.iterrows():
            try:
                if not pd.isnull(dfs_lst[i].loc[dfs_lst[i]['PCTimeStamp'] == row['PCTimeStamp'], "Amb_WindDir_Relative_Avg"]).values.any():
                    val= val + abs(row["Amb_WindDir_Relative_Avg"]-dfs_lst[i].loc[dfs_lst[i]['PCTimeStamp'] == row['PCTimeStamp'], "Amb_WindDir_Relative_Avg"].values[0])
            except:
                continue
        turb_dict[i] = val

    sorted_dict = {}
    sorted_keys = sorted(turb_dict, key=turb_dict.get)  # [1, 3, 2]

    for w in sorted_keys:
        sorted_dict[w] = turb_dict[w]

    for k, v in sorted_dict.items():
        print(str(k+1) + ". Turbine: " + str(v/len(master_df.index)))

def yaw_misaligment_min_max(begin_date, end_date):
    dfs_lst = []
    for i in range(1, 17):
        if i < 10:
            file = DATA_PATH + '_0' + str(i) + '.' + SOURCE_FORMAT
        else:
            file = DATA_PATH + '_' + str(i) + '.' + SOURCE_FORMAT

        df = pd.read_csv(file, usecols=['PCTimeStamp', 'Amb_WindDir_Relative_Avg', 'HCnt_Avg_Run'])
        df = df[df["HCnt_Avg_Run"] >= 300]
        df = df[["PCTimeStamp", "Amb_WindDir_Relative_Avg"]]
        df["Amb_WindDir_Relative_Avg"] = pd.to_numeric(df["Amb_WindDir_Relative_Avg"], downcast="float")
        df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'])
        df = df[(begin_date <= df['PCTimeStamp']) & (df['PCTimeStamp'] <= end_date)]
        dfs_lst.append(df)
        print(str(i) + "   finished")

    master_df = pd.concat(dfs_lst[0:15], axis=0)
    max_df = master_df.groupby(master_df['PCTimeStamp']).max()
    min_df = master_df.groupby(master_df['PCTimeStamp']).min()
    for df in dfs_lst:
        df = df.groupby(df['PCTimeStamp']).mean()
        df.reset_index(inplace=True)
    max_df.reset_index(inplace=True)
    min_df.reset_index(inplace=True)

    plt.figure(dpi = 300)
    plt.plot(max_df['PCTimeStamp'], max_df["Amb_WindDir_Relative_Avg"], color="red" , linewidth=0.4)
    plt.plot(min_df['PCTimeStamp'], min_df["Amb_WindDir_Relative_Avg"], color="green", linewidth=0.4)
    plt.plot(dfs_lst[15]['PCTimeStamp'], dfs_lst[15]["Amb_WindDir_Relative_Avg"], color="black", linewidth=0.4)
    plt.xticks(rotation=90)
    plt.show()

# 1 year interval
#Power Curve : Rüzgar Hızı / Üretilen power grafiğinden sapan datalar hata bildirir.( Buzlanma vs. olabilir)
# power_curve_sanity_check(begin_date,end_date, hcnt, '_01', sanity_naming, main_df)
#def speed_to_relative_avg(begin_date, end_date, hcnt, turbineNo, sanity_naming=None, df=None):

def power_curve_sanity_check(begin_date, end_date, hcnt, turbineNo, sanity_naming=None, df=None):
    before = time.time()
    if df is  None:
        try:
            df = pickle.load(open(
                f"pickles/{str(begin_date.strftime('%Y%b%d'))}_{str(end_date.strftime('%Y%b%d'))}_power_curve_{turbineNo}.pickle",
                "rb"))
        except (OSError, IOError, EOFError) as e:
            df = pd.read_csv(DATA_PATH_EFE + turbineNo + '.' + SOURCE_FORMAT,
                             usecols=['PCTimeStamp', 'Grd_Prod_Pwr_Avg', 'Amb_WindSpeed_Avg', 'HCnt_Avg_Run', 'Rtr_RPM_Avg', 'Nac_Temp_Avg', 'Amb_Temp_Avg'])
            df = df[(df["HCnt_Avg_Run"] >= hcnt) & (df["Amb_WindSpeed_Avg"] >= 5)]
            avg_df = df[["Grd_Prod_Pwr_Avg", "Amb_WindSpeed_Avg"]].groupby(df['Amb_WindSpeed_Avg']).agg(average_power=pd.NamedAgg(column="Grd_Prod_Pwr_Avg", aggfunc="mean"),
                                                                                                        standart_deviaton=pd.NamedAgg(column="Grd_Prod_Pwr_Avg", aggfunc="std"))
            df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'])
            df = df[(df["PCTimeStamp"] >= begin_date) & (df["PCTimeStamp"] <= end_date)]
            df.set_index('Amb_WindSpeed_Avg', inplace=True)
            df = pd.merge(df, avg_df, left_index=True, right_index=True, how='left')
            df["zscore_power"] = (df["Grd_Prod_Pwr_Avg"] - df["average_power"]) / df["standart_deviaton"]
            df = df[abs(df["zscore_power"]) >= 3.7]
            try:
                pickle.dump(df, open(
                    f"pickles/{str(begin_date.strftime('%Y%b%d'))}_{str(end_date.strftime('%Y%b%d'))}_power_curve_{turbineNo}.pickle", "wb"))
            except (OSError, IOError, EOFError) as e:
                print(e)
            fig, ax = plt.subplots()
            df = df.reset_index()
            df.plot("Amb_WindSpeed_Avg", "Grd_Prod_Pwr_Avg", kind='scatter', ax=ax, c='red', marker='x')
            df.plot("Amb_WindSpeed_Avg", "average_power", ax=ax, c='blue')
            plt.show()
    else:
        try:
            df = pickle.load(open(
                f"pickles/{str(begin_date.strftime('%Y%b%d'))}_{str(end_date.strftime('%Y%b%d'))}_{sanity_naming}_{turbineNo}.pickle",
                "rb"))
        except (OSError, IOError, EOFError) as e:
            temp_df = pd.read_csv(DATA_PATH_EFE + turbineNo + '.' + SOURCE_FORMAT,
                             usecols=['Grd_Prod_Pwr_Avg', 'Amb_WindSpeed_Avg', 'HCnt_Avg_Run'])
            temp_df = temp_df[(temp_df["HCnt_Avg_Run"] >= 300)].drop(columns=['HCnt_Avg_Run'])
            df = df[(df["Amb_WindSpeed_Avg"] >= 5) & (df["turbine_no"] == turbineNo)]
            avg_df = temp_df.groupby(temp_df['Amb_WindSpeed_Avg']).agg(
                average_power=pd.NamedAgg(column="Grd_Prod_Pwr_Avg", aggfunc="mean"),
                standart_deviaton=pd.NamedAgg(column="Grd_Prod_Pwr_Avg", aggfunc="std"))
            df.set_index('Amb_WindSpeed_Avg', inplace=True)
            df = pd.merge(df, avg_df, left_index=True, right_index=True, how='left')
            df["zscore_power"] = (df["Grd_Prod_Pwr_Avg"] - df["average_power"]) / df["standart_deviaton"]
            df = df[abs(df["zscore_power"]) >= 3]
            try:
                pickle.dump(df, open(
                    f"pickles/{str(begin_date.strftime('%Y%b%d'))}_{str(end_date.strftime('%Y%b%d'))}_{sanity_naming}_{turbineNo}.pickle",
                    "wb"))
            except (OSError, IOError, EOFError) as e:
                print(e)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    end = time.time()
    df['turbine_no'] = turbineNo
    print("finished in: " + str(end-before))
    return df

def average_calculator(begin_date, end_date):
    df = pd.read_csv(DATA_PATH_EFE + '_01.' + SOURCE_FORMAT,
                     usecols=['PCTimeStamp', 'Rtr_RPM_Avg', 'HCnt_Avg_Run', 'Amb_WindSpeed_Avg'])
    df = df[(df["HCnt_Avg_Run"] >= 300) & (df["Amb_WindSpeed_Avg"] < 11) & (df["Amb_WindSpeed_Avg"] > 1)]
    df = df[["PCTimeStamp", "Rtr_RPM_Avg"]]
    df["Rtr_RPM_Avg"] = pd.to_numeric(df["Rtr_RPM_Avg"], downcast="float")

    # for other turbines
    for i in range(2, 17):
        if i < 10:
            file = DATA_PATH_EFE + '_0' + str(i) + '.' + SOURCE_FORMAT
        else:
            file = DATA_PATH_EFE + '_' + str(i) + '.' + SOURCE_FORMAT

        df_temp = pd.read_csv(file,
                              usecols=['PCTimeStamp', 'Rtr_RPM_Avg', 'HCnt_Avg_Run', 'Amb_WindSpeed_Avg'])

        df_temp = df_temp[df_temp["HCnt_Avg_Run"] >= 300 & (df_temp["Amb_WindSpeed_Avg"] < 11) & (
                df_temp["Amb_WindSpeed_Avg"] > 1)]
        df_temp["Rtr_RPM_Avg"] = pd.to_numeric(df_temp["Rtr_RPM_Avg"], downcast="float")
        df_temp = df_temp[["PCTimeStamp", "Rtr_RPM_Avg"]]
        df = pd.concat([df, df_temp], axis=0)
        print(str(i) + "   finished")

    df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'])
    df = df[(begin_date <= df['PCTimeStamp']) & (df['PCTimeStamp'] <= end_date)]
    avg_df = df[["PCTimeStamp", "Rtr_RPM_Avg"]].groupby(df['PCTimeStamp']).agg(
        average_rpm=pd.NamedAgg(column="Rtr_RPM_Avg", aggfunc="mean"),
        standart_deviaton_rpm=pd.NamedAgg(column="Rtr_RPM_Avg", aggfunc="std"))
    return avg_df, df

#Helper function
def rpm_calculator(begin_date, end_date, power_df=None, sanity_naming=None):
    if power_df is None:
        avg_df, df = average_calculator(begin_date, end_date)
        df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'])
        df.set_index('PCTimeStamp', inplace=True)
        df = pd.merge(df, avg_df, left_index=True, right_index=True, how='left')
        df["zscore"] = (df["Rtr_RPM_Avg"] - df["average_rpm"]) / df["standart_deviaton_rpm"]
        df = df[(abs(df["zscore"]) > 3.75)]
        pickle.dump(df, open(
            f"pickles/{str(begin_date.strftime('%Y%b%d'))}_{str(end_date.strftime('%Y%b%d'))}_rpm_yaw_misalignment.pickle",
            "wb"))
    else:
        df = power_df
        df = df[(df['Amb_WindSpeed_Avg'] <= 11)]
        avg_df, temp = average_calculator(begin_date, end_date)
        df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'])
        df.set_index('PCTimeStamp', inplace=True)
        df = pd.merge(df, avg_df, left_index=True, right_index=True, how='left')
        df["zscore"] = (df["Rtr_RPM_Avg"] - df["average_rpm"]) / df["standart_deviaton_rpm"]
        df = df[(abs(df["zscore"]) > 1.5)]  # 3.7 without correlation , 3 with
    if power_df is not None:
        pickle.dump(df, open(
            f"pickles/{str(begin_date.strftime('%Y%b%d'))}_{str(end_date.strftime('%Y%b%d'))}_{sanity_naming}.pickle",
            "wb"))
    else:
        pickle.dump(df, open(
            f"pickles/{str(begin_date.strftime('%Y%b%d'))}_{str(end_date.strftime('%Y%b%d'))}_{sanity_naming}.pickle", "wb"))
    return df

# 1 year interval
# If wind-tribunes are well-aligned, in our case it is, their rpm should be close.
# if it is not, there may be yaw error.
def rpm_yaw_misalignment(begin_date, end_date, df=None, sanity_naming=None):
    if df is None:
        try:
            df = pickle.load(open(
                f"pickles/{str(begin_date.strftime('%Y%b%d'))}_{str(end_date.strftime('%Y%b%d'))}_rpm_yaw_misalignment.pickle",
                "rb"))
        except (OSError, IOError, EOFError) as e:
            df = rpm_calculator(begin_date, end_date)
    else:
        try:
            df = pickle.load(open(
                f"pickles/{str(begin_date.strftime('%Y%b%d'))}_{str(end_date.strftime('%Y%b%d'))}_{sanity_naming}.pickle",
                "rb"))
        except (OSError, IOError, EOFError) as e:
            df = rpm_calculator(begin_date, end_date, df, sanity_naming)
    plt.scatter(df.index.values, df["Rtr_RPM_Avg"], c='red')
    plt.scatter(df.index.values, df["average_rpm"], c='blue')
    plt.gcf().autofmt_xdate()
    plt.xlabel('Time')
    plt.ylabel("Rtr_RPM_Avg")
    plt.show()
    return df

def nac_temp_avg(begin_date, end_date, sanity_naming=None, df=None):
    # master df
    if df is None:
        try:
            df = pickle.load(open(f"pickles/{str(begin_date.strftime('%Y%b%d'))}_{str(end_date.strftime('%Y%b%d'))}_{sanity_naming}.pickle", "rb"))
            f, (ax1) = plt.subplots(nrows=1, ncols=1)
            ax1.set_title('Errors')
            ax1.set_ylabel('Temperature Difference')
            ax1.set_xlabel('Time')
            ax1.scatter(df.index.values, df["temp_difference"], c='red')
            ax1.plot(df.index.values, df["average_Nac_Temp_Avg"], c='blue')
        except (OSError, IOError, EOFError) as e:
            f, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
            ax1.set_title('16 turbines')
            ax2.set_title('Errors')
            ax2.set_xlabel('Time')
            ax2.set_ylabel('Temperature Difference')
            df = pd.read_csv(DATA_PATH_EFE + '_01.' + SOURCE_FORMAT,
                             usecols=['PCTimeStamp', 'Nac_Temp_Avg', 'HCnt_Avg_Run', 'Amb_Temp_Avg'])
            df = df[df["HCnt_Avg_Run"] >= 300]
            df["temp_difference"] = abs(df["Nac_Temp_Avg"]-df['Amb_Temp_Avg'])
            df["temp_difference"] = pd.to_numeric(df["temp_difference"], downcast="float")
            df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'])
            df = df[(begin_date <= df['PCTimeStamp']) & (df['PCTimeStamp'] <= end_date)]
            df = df[["PCTimeStamp", "temp_difference"]]
            ax1.scatter(df["PCTimeStamp"], df["temp_difference"], color=COLORS[(1) % 8], s=0.2)
            df['turbine_no'] = "_01"

            #for other turbines
            for i in range(2, 17):
                if i < 10:
                    file = DATA_PATH_EFE + '_0' + str(i) + '.' + SOURCE_FORMAT
                else:
                    file = DATA_PATH_EFE + '_' + str(i) + '.' + SOURCE_FORMAT

                df_temp = pd.read_csv(file,
                                      usecols=['PCTimeStamp', 'Nac_Temp_Avg', 'HCnt_Avg_Run', 'Amb_Temp_Avg'])

                df_temp = df_temp[df_temp["HCnt_Avg_Run"] >= 300]
                df_temp["temp_difference"] = abs(df_temp["Nac_Temp_Avg"] - df_temp['Amb_Temp_Avg'])
                df_temp["temp_difference"] = pd.to_numeric(df_temp["temp_difference"], downcast="float")
                df_temp = df_temp[["PCTimeStamp", "temp_difference"]]
                df_temp['PCTimeStamp'] = pd.to_datetime(df_temp['PCTimeStamp'])
                df_temp = df_temp[(begin_date <= df_temp['PCTimeStamp']) & (df_temp['PCTimeStamp'] <= end_date)]
                if i < 10:
                    df_temp['turbine_no'] = ('_0' + str(i))
                else:
                    df_temp['turbine_no'] = ('_' + str(i))
                ax1.scatter(df_temp["PCTimeStamp"], df_temp["temp_difference"], color=COLORS[(i - 1) % 8], s=0.2)
                df = pd.concat([df, df_temp], axis=0)
                print(str(i) + "   finished")
            avg_df = df[["PCTimeStamp", "temp_difference"]].groupby(df['PCTimeStamp']).agg(
                average_Nac_Temp_Avg=pd.NamedAgg(column="temp_difference", aggfunc="mean"),
                standart_deviaton_Nac_Temp_Avg=pd.NamedAgg(column="temp_difference", aggfunc="std"))
            df.set_index('PCTimeStamp', inplace=True)
            df = pd.merge(df, avg_df, left_index=True, right_index=True, how='left')
            df["zscore"] = (df["temp_difference"] - df["average_Nac_Temp_Avg"]) / df[
                "standart_deviaton_Nac_Temp_Avg"]
            df = df[(abs(df["zscore"]) > 3.4)]
            pickle.dump(df, open(f"pickles/{str(begin_date.strftime('%Y%b%d'))}_{str(end_date.strftime('%Y%b%d'))}_{sanity_naming}.pickle", "wb"))
            ax2.scatter(df.index.values, df["temp_difference"], c='red', s=0.5)
            ax2.plot(df.index.values, df["average_Nac_Temp_Avg"], c='blue')
    else:
        try:
            df = pickle.load(open(
                f"pickles/{str(begin_date.strftime('%Y%b%d'))}_{str(end_date.strftime('%Y%b%d'))}_{sanity_naming}.pickle",
                "rb"))
            f, (ax1) = plt.subplots(nrows=1, ncols=1)
            ax1.set_title('Errors')
            ax1.scatter(df.index.values, df["temp_difference"], c='red')
            ax1.plot(df.index.values, df["average_Nac_Temp_Avg"], c='blue')
        except (OSError, IOError, EOFError) as e:
            f, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
            ax1.set_title('16 turbines')
            ax2.set_title('Errors')
            avg_df = pd.read_csv(DATA_PATH_EFE + '_01.' + SOURCE_FORMAT,
                             usecols=['PCTimeStamp', 'Nac_Temp_Avg', 'HCnt_Avg_Run', 'Amb_Temp_Avg'])
            avg_df = avg_df[avg_df["HCnt_Avg_Run"] >= 300]
            avg_df["temp_difference"] = abs(avg_df["Nac_Temp_Avg"]-avg_df['Amb_Temp_Avg'])
            avg_df = avg_df[["PCTimeStamp", "temp_difference"]]
            avg_df["temp_difference"] = pd.to_numeric(avg_df["temp_difference"], downcast="float")
            avg_df['PCTimeStamp'] = pd.to_datetime(avg_df['PCTimeStamp'])
            avg_df = avg_df[(begin_date <= avg_df['PCTimeStamp']) & (avg_df['PCTimeStamp'] <= end_date)]
            ax1.scatter(avg_df["PCTimeStamp"], avg_df["temp_difference"], color=COLORS[(1) % 8], s=0.2)
            # df = df[begin_date <= pd.to_datetime(df['PCTimeStamp'])]
            # df = df[pd.to_datetime(df['PCTimeStamp']) <= end_date]

            # for other turbines
            for i in range(2, 17):
                if i < 10:
                    file = DATA_PATH_EFE + '_0' + str(i) + '.' + SOURCE_FORMAT
                else:
                    file = DATA_PATH_EFE + '_' + str(i) + '.' + SOURCE_FORMAT

                df_temp = pd.read_csv(file,
                                      usecols=['PCTimeStamp', 'Nac_Temp_Avg', 'HCnt_Avg_Run', 'Amb_Temp_Avg'])

                df_temp = df_temp[df_temp["HCnt_Avg_Run"] >= 300]
                df_temp["temp_difference"] = abs(df_temp["Nac_Temp_Avg"] - df_temp['Amb_Temp_Avg'])
                df_temp["temp_difference"] = pd.to_numeric(df_temp["temp_difference"],
                                                                    downcast="float")
                df_temp = df_temp[["PCTimeStamp", "temp_difference"]]
                df_temp['PCTimeStamp'] = pd.to_datetime(df_temp['PCTimeStamp'])
                df_temp = df_temp[(begin_date <= df_temp['PCTimeStamp']) & (df_temp['PCTimeStamp'] <= end_date)]
                ax1.scatter(df_temp["PCTimeStamp"], df_temp["temp_difference"], color=COLORS[(i - 1) % 8],
                            s=0.2)
                avg_df = pd.concat([avg_df, df_temp], axis=0)
                print(str(i) + "   finished")
            avg_df = avg_df[["PCTimeStamp", "temp_difference"]].groupby(avg_df['PCTimeStamp']).agg(
                average_Nac_Temp_Avg=pd.NamedAgg(column="temp_difference", aggfunc="mean"),
                std_Nac_Temp_Avg=pd.NamedAgg(column="temp_difference", aggfunc="std"))
            if 'PCTimeStamp' != df.index.name:
                df.set_index('PCTimeStamp', inplace=True)
            df = pd.merge(df, avg_df, left_index=True, right_index=True, how='left')
            df["temp_difference"] = abs(df["Nac_Temp_Avg"] - df['Amb_Temp_Avg'])
            df["zscore"] = (df["temp_difference"] - df["average_Nac_Temp_Avg"]) / df[
                "std_Nac_Temp_Avg"]
            df = df[(abs(df["zscore"]) > 1.5)]
            pickle.dump(df, open(
                f"pickles/{str(begin_date.strftime('%Y%b%d'))}_{str(end_date.strftime('%Y%b%d'))}_{sanity_naming}.pickle",
                "wb"))
            ax2.scatter(df.index.values, df["temp_difference"], c='red', s=0.5)
            ax2.scatter(df.index.values, df["average_Nac_Temp_Avg"], c='blue')
    plt.gcf().autofmt_xdate()
    plt.show()
    return df

def rpm_yaw_bins(begin_date, end_date, s_begin_date, s_end_date):
    dict = {}

    for i in range(1, 17):
        if i < 10:
            file = DATA_PATH_EFE + '_0' + str(i) + '.' + SOURCE_FORMAT
        else:
            file = DATA_PATH_EFE + '_' + str(i) + '.' + SOURCE_FORMAT

        df = pd.read_csv(file, usecols=['PCTimeStamp', 'Rtr_RPM_Avg','Amb_WindSpeed_Avg', 'Amb_WindDir_Relative_Avg', 'HCnt_Avg_Run'])
        df = df[df["HCnt_Avg_Run"] >= 300]
        df = df[df["Amb_WindSpeed_Avg"] < 11]
        df = df[df["Amb_WindSpeed_Avg"] > 1]
        df = df[['PCTimeStamp', 'Amb_WindDir_Relative_Avg', 'Rtr_RPM_Avg','Amb_WindSpeed_Avg']]
        df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'])
        df = df[(begin_date <= df['PCTimeStamp']) & (df['PCTimeStamp'] <= end_date)]
        for index, row in df.iterrows():
            if row['Amb_WindSpeed_Avg'] in dict.keys():
                if row['Amb_WindDir_Relative_Avg'] in dict[row['Amb_WindSpeed_Avg']].keys():
                    dict[row['Amb_WindSpeed_Avg']][row['Amb_WindDir_Relative_Avg']].append(row['Rtr_RPM_Avg'])
                else:
                    dict[row['Amb_WindSpeed_Avg']][row['Amb_WindDir_Relative_Avg']] = []
                    dict[row['Amb_WindSpeed_Avg']][row['Amb_WindDir_Relative_Avg']].append(row['Rtr_RPM_Avg'])
            else:
                dict[row['Amb_WindSpeed_Avg']] = {}
                dict[row['Amb_WindSpeed_Avg']][row['Amb_WindDir_Relative_Avg']] = []
                dict[row['Amb_WindSpeed_Avg']][row['Amb_WindDir_Relative_Avg']].append(row['Rtr_RPM_Avg'])

        print(str(i) + "   finished")

    for k,v in dict.items():
        for k1, v1 in v.items():
            dict[k][k1] = sum(v1) / len(v1)

    df2 = pd.read_csv(DATA_PATH_EFE + '_01.' + SOURCE_FORMAT,
                     usecols=['PCTimeStamp', 'Rtr_RPM_Avg', 'HCnt_Avg_Run','Amb_WindDir_Relative_Avg', 'Amb_WindSpeed_Avg'])
    df2 = df2[df2["HCnt_Avg_Run"] >= 300]
    df2 = df2[df2["Amb_WindSpeed_Avg"] < 11]
    df2 = df2[df2["Amb_WindSpeed_Avg"] > 1]
    df2 = df2[['PCTimeStamp', 'Amb_WindDir_Relative_Avg', 'Rtr_RPM_Avg', 'Amb_WindSpeed_Avg']]
    df2['PCTimeStamp'] = pd.to_datetime(df2['PCTimeStamp'])
    df2 = df2[(s_begin_date <= df2['PCTimeStamp']) & (df2['PCTimeStamp'] <= s_end_date)]

    for index, row in df2.iterrows():
        try:
            print(str(row['PCTimeStamp']) + "   expected rpm: " + "{:.2f}".format(dict[row['Amb_WindSpeed_Avg']][row['Amb_WindDir_Relative_Avg']]) + "    actual: " + str(row['Rtr_RPM_Avg']))
        except:
            continue

def run(begin_date, end_date,  *args, hcnt=300):
    sanity_naming = ""
    main_df = None
    for sanity_type in args:
        sanity_naming = sanity_naming + '_'  + sanity_type
        if sanity_type == "speed_to_relative_avg":
            speed_df = speed_to_relative_avg(begin_date, end_date, hcnt, ('_01'), sanity_naming,main_df)
            for i in range(2, 17):
                if i < 10:
                    speed_df = pd.concat((speed_df, speed_to_relative_avg(begin_date, end_date, hcnt, ('_0' + str(i)), sanity_naming, main_df)), axis=0)
                else:
                    speed_df = pd.concat((speed_df, speed_to_relative_avg(begin_date, end_date, hcnt, ('_' + str(i)), sanity_naming, main_df)), axis=0)
                print(str(i) + "   finished")
            fig, ax = plt.subplots()
            main_df = speed_df
            main_df.plot("Amb_WindSpeed_Avg", "std_speed", kind='scatter', ax=ax, c='green', marker='x')
            main_df.plot("Amb_WindSpeed_Avg", "mean_speed", kind='scatter', ax=ax, c='blue', marker='x')
            main_df.plot("Amb_WindSpeed_Avg", "Amb_WindDir_Relative_Avg", kind='scatter', ax=ax, c='red', marker='x')
            plt.show()
            print(len(main_df))
        elif sanity_type == "power_curve_sanity_check":
            power_df = power_curve_sanity_check(begin_date,end_date, hcnt, '_01', sanity_naming, main_df)
            for i in range(2, 17):
                if i < 10:
                    power_df = pd.concat((power_df, power_curve_sanity_check(begin_date,end_date, hcnt,  ('_0' + str(i)),sanity_naming, main_df)), axis=0)
                else:
                    power_df = pd.concat((power_df, power_curve_sanity_check(begin_date,end_date, hcnt, ('_' + str(i)),sanity_naming, main_df)), axis=0)
                print(str(i) + "   finished")
            fig, ax = plt.subplots()
            main_df = power_df
            main_df = main_df.reset_index()
            main_df.plot("Amb_WindSpeed_Avg", "Grd_Prod_Pwr_Avg", kind='scatter', ax=ax, c='red', marker='x')
            main_df.plot("Amb_WindSpeed_Avg", "average_power", ax=ax, c='blue', kind='scatter')
            plt.show()
            print(len(main_df))
        elif sanity_type == "rpm_yaw_misalignment":
            main_df = rpm_yaw_misalignment(begin_date, end_date, main_df, sanity_naming)
            print(len(main_df))
            #print(main_df)
        elif sanity_type == "nac_temp_avg":
            main_df = nac_temp_avg(begin_date, end_date, sanity_naming, main_df)
            print(len(main_df))
            #print(main_df)
        elif sanity_type == "all_turbines_yaw_misaligment":
            main_df = all_turbines_yaw_misaligment(begin_date, end_date, sanity_naming, main_df)
            print(len(main_df))
            main_df.to_excel
            main_df.to_excel("output.xlsx")
            print(main_df)
