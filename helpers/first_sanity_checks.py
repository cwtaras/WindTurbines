import pickle
import time
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from constants import DATA_PATH, SOURCE_FORMAT, COLORS, DATA_PATH_EFE


# Wind speed-dependent table. Calculate the observed yaw
# misalignment for each wind speed and adjust each value in the table
# accordingly.
def speed_to_relative_avg(begin_date, end_date, hcnt):
    before = time.time()
    try:
        df = pickle.load(open("var.pickle", "rb"))
    except (OSError, IOError) as e:
        df = pd.read_csv(DATA_PATH_EFE + '_01.' + SOURCE_FORMAT,
                         usecols=['PCTimeStamp', 'Amb_WindDir_Relative_Avg', 'HCnt_Avg_Run', 'Amb_WindSpeed_Avg'])
        df = df[df["HCnt_Avg_Run"] >= hcnt]
        means = df[["Amb_WindSpeed_Avg", "Amb_WindDir_Relative_Avg"]].groupby(["Amb_WindSpeed_Avg"]).mean()
        means.columns = ['mean']
        std = df[["Amb_WindSpeed_Avg", "Amb_WindDir_Relative_Avg"]].groupby(["Amb_WindSpeed_Avg"]).std()
        std.columns = ['std']
        df = df.join(means, on='Amb_WindSpeed_Avg', how="left")
        df = df.join(std, on='Amb_WindSpeed_Avg', how="left")
        df["zscore"] = (df["Amb_WindDir_Relative_Avg"] - df["mean"]) / df["std"]
        df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'])
        df = df[(df["PCTimeStamp"] >= begin_date) & (df["PCTimeStamp"] <= end_date) &
                (abs(df["zscore"]) > 5) & (df["Amb_WindSpeed_Avg"] > 5)]
        pickle.dump(df, open("var.pickle", "wb"))
    fig, ax = plt.subplots()
    df.plot("Amb_WindSpeed_Avg", "Amb_WindDir_Relative_Avg", kind='scatter', ax=ax, c='red', marker='x')
    plt.show()
    end = time.time()
    print("finished in:" + str(end-before))


def all_turbines_yaw_misaligment(begin_date, end_date):
    # master df
    f = plt.figure()
    f, (ax1,ax2) = plt.subplots(nrows=2, ncols=1)
    ax1.set_title('16 tribune')
    ax2.set_title('Errors')
    df = pd.read_csv(DATA_PATH_EFE + '_01.' + SOURCE_FORMAT,
                     usecols=['PCTimeStamp', 'Amb_WindDir_Relative_Avg', 'HCnt_Avg_Run'])
    df = df[df["HCnt_Avg_Run"] >= 300]
    df = df[["PCTimeStamp","Amb_WindDir_Relative_Avg"]]
    df["Amb_WindDir_Relative_Avg"] = pd.to_numeric(df["Amb_WindDir_Relative_Avg"], downcast="float")
    df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'])
    df = df[(begin_date <= df['PCTimeStamp']) & (df['PCTimeStamp'] <= end_date)]
    ax1.plot(df["PCTimeStamp"], df["Amb_WindDir_Relative_Avg"], color=COLORS[(1) % 8])
    # df = df[begin_date <= pd.to_datetime(df['PCTimeStamp'])]
    # df = df[pd.to_datetime(df['PCTimeStamp']) <= end_date]

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
        ax1.plot(df_temp["PCTimeStamp"], df_temp["Amb_WindDir_Relative_Avg"], color=COLORS[(i - 1) % 8])
        df = pd.concat([df, df_temp], axis=0)
        print(str(i) + "   finished")

    df["zscore"] = (df["Amb_WindDir_Relative_Avg"] - df["Amb_WindDir_Relative_Avg"].mean()) / df[
        "Amb_WindDir_Relative_Avg"].std(ddof=0)
    df = df[(abs(df["zscore"]) > 2)]
    df = df.groupby(df['PCTimeStamp']).mean()
    ax2.scatter(df.index.values, df["Amb_WindDir_Relative_Avg"])
    plt.gcf().autofmt_xdate()
    plt.show()

def turbine_yaw_avg_comprasion(begin_date, end_date):
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

#Power Curve : Rüzgar Hızı / Üretilen power grafiğinden sapan datalar hata bildirir.( Buzlanma vs. olabilir)
def power_curve_sanity_check(begin_date, end_date, hcnt):
    df = pd.read_csv(DATA_PATH_EFE + '_01.' + SOURCE_FORMAT,
                     usecols=['PCTimeStamp', 'Grd_Prod_Pwr_Avg', 'Amb_WindSpeed_Avg', 'HCnt_Avg_Run'])
    df = df[df["HCnt_Avg_Run"] >= hcnt]
    avg_df = df[["Grd_Prod_Pwr_Avg", "Amb_WindSpeed_Avg"]].groupby(df['Amb_WindSpeed_Avg']).agg(average_power=pd.NamedAgg(column="Grd_Prod_Pwr_Avg", aggfunc="mean"),
                                                                                                standart_deviaton=pd.NamedAgg(column="Grd_Prod_Pwr_Avg", aggfunc="std"))
    df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'])
    df = df[(df["PCTimeStamp"] >= begin_date) & (df["PCTimeStamp"] <= end_date)]
    df.set_index('Amb_WindSpeed_Avg', inplace=True)
    df = pd.merge(df, avg_df, left_index=True, right_index=True, how='left')
    df["zscore"] = (df["Grd_Prod_Pwr_Avg"] - df["average_power"]) / df["standart_deviaton"]
    df = df[abs(df["zscore"]) >= 3]
    fig, ax = plt.subplots()
    df.reset_index().plot("Amb_WindSpeed_Avg","Grd_Prod_Pwr_Avg", kind='scatter', ax=ax, c='red', marker='x')
    plt.show()
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print(df)

def rpm_yaw_misalignment(begin_date, end_date):
    df = pd.read_csv(DATA_PATH_EFE + '_01.' + SOURCE_FORMAT,
                     usecols=['PCTimeStamp', 'Rtr_RPM_Avg', 'HCnt_Avg_Run', 'Amb_WindSpeed_Avg'])
    df = df[(df["HCnt_Avg_Run"] >= 300) & (df["Amb_WindSpeed_Avg"] < 11) & (df["Amb_WindSpeed_Avg"] > 1)]
    df = df[["PCTimeStamp", "Rtr_RPM_Avg"]]
    df["Rtr_RPM_Avg"] = pd.to_numeric(df["Rtr_RPM_Avg"], downcast="float")

    #for other turbines
    for i in range(2, 17):
        if i < 10:
            file = DATA_PATH_EFE + '_0' + str(i) + '.' + SOURCE_FORMAT
        else:
            file = DATA_PATH_EFE + '_' + str(i) + '.' + SOURCE_FORMAT

        df_temp = pd.read_csv(file,
                              usecols=['PCTimeStamp', 'Rtr_RPM_Avg', 'HCnt_Avg_Run', 'Amb_WindSpeed_Avg'])

        df_temp = df_temp[df_temp["HCnt_Avg_Run"] >= 300 & (df_temp["Amb_WindSpeed_Avg"] < 11) & (df_temp["Amb_WindSpeed_Avg"] > 1)]
        df_temp["Rtr_RPM_Avg"] = pd.to_numeric(df_temp["Rtr_RPM_Avg"], downcast="float")
        df_temp = df_temp[["PCTimeStamp", "Rtr_RPM_Avg"]]
        df = pd.concat([df, df_temp], axis=0)
        print(str(i) + "   finished")

    df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'])
    df = df[(begin_date <= df['PCTimeStamp']) & (df['PCTimeStamp'] <= end_date)]
    avg_df = df[["PCTimeStamp", "Rtr_RPM_Avg"]].groupby(df['PCTimeStamp']).agg(
        average_power=pd.NamedAgg(column="Rtr_RPM_Avg", aggfunc="mean"),
        standart_deviaton=pd.NamedAgg(column="Rtr_RPM_Avg", aggfunc="std"))
    df.set_index('PCTimeStamp', inplace=True)
    df = pd.merge(df, avg_df, left_index=True, right_index=True, how='left')
    df["zscore"] = (df["Rtr_RPM_Avg"] - df["average_power"]) / df["standart_deviaton"]
    df = df[(abs(df["zscore"]) > 3.7)]
    print(df)
    plt.scatter(df.index.values, df["Rtr_RPM_Avg"])
    plt.show()

def rpm_yaw_bins(begin_date, end_date, s_begin_date, s_end_date):
    dict = {}

    for i in range(1, 17):
        if i < 10:
            file = DATA_PATH + '_0' + str(i) + '.' + SOURCE_FORMAT
        else:
            file = DATA_PATH + '_' + str(i) + '.' + SOURCE_FORMAT

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

    df2 = pd.read_csv(DATA_PATH + '_01.' + SOURCE_FORMAT,
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
