import csv
from datetime import datetime
import matplotlib.pyplot as plt
from constants import DATA_PATH, SOURCE_FORMAT


def winddir_relative_arg_hours(begin_date, end_date):
    with open(
            DATA_PATH + '_01.' + SOURCE_FORMAT,
            newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        timeList = {}
        winddir = []
        hours = []
        i = 0
        for row in spamreader:
            if i != 0:
                time = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                if begin_date < time < end_date:
                    date = row[0].split(' ')
                    hour = date[1].split(':')[0]
                    if hour in timeList.keys():
                        timeList[hour].append(float(row[33]))
                    else:
                        timeList[hour] = [float(row[33])]
            i = i + 1

    for k, v in timeList.items():
        hours.append(k)
        winddir.append(sum(v) / len(v))
    plt.plot(hours, winddir)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()