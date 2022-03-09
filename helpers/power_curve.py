import csv
from datetime import datetime
import matplotlib.pyplot as plt


def power_curve(begin_date, end_date):
    with open('/Users/efesabanoglu/Downloads/borusan_scada_harmanlik/borusan_scada_harmanlik_01.csv',
              newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        wind_speed = []
        power = []
        i = 0
        for row in spamreader:
            if i != 0:
                time = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                if begin_date < time < end_date:
                    wind_speed.append(float(row[12]))
                    power.append(float(row[47]))
            i = i + 1
    plt.plot(wind_speed, power)
    plt.show()