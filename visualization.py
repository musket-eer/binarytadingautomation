import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import calendar
from datetime import date

# this file is used to visually analyse the profit/ loss progression of the trading account balance
# it reads form the log files, converts the data to csv 
week_day = calendar.day_name[date.today().weekday()]
filename = "demo_logs" + week_day + ".csv"
file_object = open(filename, 'r')
x_axis = []
y_axis = []
for line in file_object:
    print(line.split(','))
    x_axis.append(line.split(',')[0])
    y_axis.append(line.split(',')[2])

plt.plot(x_axis,y_axis)
plt.title(week_day)
plt.ylabel('balance')
plt.xlabel('trades')
plt.show()

