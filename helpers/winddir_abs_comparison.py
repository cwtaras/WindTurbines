import csv
from datetime import datetime
import matplotlib.pyplot as plt
import random
from constants import DATA_PATH, SOURCE_FORMAT

def winddir_abs_comparison(begin_date, end_date):
    not_last_one = True
    index = 1
    timeList = []
    while not_last_one:
        try:
            if index == 1:
                temp = []
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
                                temp.append(float(row[34]))
                        i = i+1
                    print("Tribune " + str(index) + " has finished")
                color = random.uniform(0, 1)
                plt.plot(timeList, temp, color=(color, color, color))
            elif index < 10:
                temp = []
                with open(
                        DATA_PATH + '_0' + str(index) + '.' + SOURCE_FORMAT,
                        newline='') as csvfile:
                    spamreader = csv.reader(csvfile)
                    i = 0
                    for row in spamreader:
                        if i != 0:
                            time = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                            if begin_date < time < end_date:
                                temp.append(float(row[34]))
                        i = i+1
                    print("Tribune " + str(index) + " has finished")
                color = random.uniform(0, 1)
                plt.plot(timeList, temp, color=(color, color, color))
            else:
                temp = []
                with open(
                        DATA_PATH + '_' + str(index) + '.' + SOURCE_FORMAT,
                        newline='') as csvfile:
                    spamreader = csv.reader(csvfile)
                    i = 0
                    for row in spamreader:
                        if i != 0:
                            time = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                            if begin_date < time < end_date:
                                temp.append(float(row[34]))
                        i = i+1
                    print("Tribune " + str(index) + " has finished")
                color = random.uniform(0, 1)
                plt.plot(timeList, temp, color=(color, color, color))
            index = index + 1
        except:
            not_last_one = False
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
