#!/usr/bin/python

from openpyxl.reader.excel import load_workbook

from Readers import *
from Behavior import *
from Student import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab


behav_read = BehaviorReader('data/DPCHS_BehaviorData.xlsx')
behaviors = []
while behav_read.next_sheet():
    behaviors += behav_read.get_data()

labels = ('Demerit','AutoDt','Uniform','SendOut')
values = [0,0,0,0]

# Fill Bar Chart
for b in behaviors:
    if b.behaviorType == 'Demerit':
        values[0] += 1
    elif b.behaviorType == 'AutoDetention':
        values[1] += 1
    elif b.behaviorType == 'Uniform':
        values[2] += 1
    elif b.behaviorType == 'SendOut':
        values[3] += 1




width = 0.35
ind = np.arange(len(values))

fig = plt.figure()
ax = fig.add_subplot(111)

bars = ax.bar(ind+width, tuple(values), width, color='y')

plt.show()


blah = raw_input("waiting...")

