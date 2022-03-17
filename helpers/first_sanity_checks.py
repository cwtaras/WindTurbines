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

def all_turbines_yaw_misaligment(begin_date, end_date):
    # master df
    df = pd.read_csv(DATA_PATH + '_01.' + SOURCE_FORMAT,
                     usecols=['PCTimeStamp', 'Amb_WindDir_Relative_Avg', 'HCnt_Avg_Run'])
    df = df[df["HCnt_Avg_Run"] >= 300]
    df = df[["PCTimeStamp","Amb_WindDir_Relative_Avg"]]
    df["Amb_WindDir_Relative_Avg"] = pd.to_numeric(df["Amb_WindDir_Relative_Avg"], downcast="float")

    # df = df[begin_date <= pd.to_datetime(df['PCTimeStamp'])]
    # df = df[pd.to_datetime(df['PCTimeStamp']) <= end_date]

    #for other turbines
    for i in range(2, 17):
        if i < 10:
            file = DATA_PATH + '_0' + str(i) + '.' + SOURCE_FORMAT
        else:
            file = DATA_PATH + '_' + str(i) + '.' + SOURCE_FORMAT

        df_temp = pd.read_csv(file,
                              usecols=['PCTimeStamp', 'Amb_WindDir_Relative_Avg', 'HCnt_Avg_Run'])

        df_temp = df_temp[df_temp["HCnt_Avg_Run"] >= 300]
        df_temp["Amb_WindDir_Relative_Avg"] = pd.to_numeric(df_temp["Amb_WindDir_Relative_Avg"], downcast="float")
        df_temp = df_temp[["PCTimeStamp", "Amb_WindDir_Relative_Avg"]]
        df = pd.concat([df, df_temp], axis=0)

        print(str(i) + "   finished")

    df["zscore"] = (df["Amb_WindDir_Relative_Avg"] - df["Amb_WindDir_Relative_Avg"].mean()) / df[
        "Amb_WindDir_Relative_Avg"].std(ddof=0)
    df['PCTimeStamp'] = pd.to_datetime(df['PCTimeStamp'])
    df = df[(begin_date <= df['PCTimeStamp']) & (df['PCTimeStamp'] <= end_date)]
    df = df[(abs(df["zscore"]) > 2)]
    df = df.groupby(df['PCTimeStamp']).mean()
    plt.scatter(df.index.values, df["Amb_WindDir_Relative_Avg"])
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
