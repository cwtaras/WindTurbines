import csv
from datetime import datetime
import matplotlib.pyplot as plt

from constants import DATA_PATH, SOURCE_FORMAT


def winddir_relative_arg(begin_date, end_date):
    with open(
            DATA_PATH + '_01.' + SOURCE_FORMAT,
            newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        timeList = []
        winddir = []
        i = 0
        for row in spamreader:
            if i != 0:
                time = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                if begin_date < time < end_date:
                    timeList.append(time)
                    winddir.append(float(row[33]))
            i = i+1
    plt.plot(timeList, winddir)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()