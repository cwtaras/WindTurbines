import csv
from datetime import datetime
import matplotlib.pyplot as plt

from constants import DATA_PATH, SOURCE_FORMAT


def winddir_relative_arg_for_all_tribune(begin_date, end_date):
    not_last_one = True
    index = 1
    timeList = []
    winddir = {}
    while not_last_one:
        try:
            if index == 1:
                with open(
                        DATA_PATH + '_0' + str(index) + '.' + SOURCE_FORMAT,
                        newline='') as csvfile:
                    spamreader = csv.reader(csvfile)
                    i = 0
                    for row in spamreader:
                        if i != 0:
                            time = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                            if begin_date < time < end_date:
                                timeList.append(time)
                                winddir[time] = float(row[33])
                        i = i+1
                    print("Tribune " + str(index) + " has finished")
            elif index < 10:
                with open(
                        DATA_PATH + '_0' + str(index) + '.' + SOURCE_FORMAT,
                        newline='') as csvfile:
                    spamreader = csv.reader(csvfile)
                    i = 0
                    for row in spamreader:
                        if i != 0:
                            time = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                            try:
                                if begin_date < time < end_date:
                                    winddir[time] = winddir[time] + float(row[33])
                            except:
                                print(time, end='')
                                print("is first for" + str(index))
                        i = i+1
                    print("Tribune " + str(index) + " has finished")
            else:
                with open(
                        DATA_PATH + '_' + str(index) + '.' + SOURCE_FORMAT,
                        newline='') as csvfile:
                    spamreader = csv.reader(csvfile)
                    i = 0
                    for row in spamreader:
                        if i != 0:
                            time = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                            try:
                                if begin_date < time < end_date:
                                    winddir[time] = winddir[time] + float(row[33])
                            except:
                                print(time, end='')
                                print("is first for" + str(index))
                        i = i+1
                    print("Tribune " + str(index) + " has finished")
            index = index + 1
        except:
            not_last_one = False
    for k in winddir:
        winddir[k] = winddir[k] / (index-1)

    plt.plot(*zip(*sorted(winddir.items())))
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
