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

labels = ('3 Demerits','Auto Dt','Uniform','Send Out')
values = [0,0,0,0]

dates = {}

i = 0
for b in behaviors:
    if b.date not in dates.keys():
        dates[b.date] = {}
    
    if b.student not in dates[b.date].keys():
        dates[b.date][b.student] = [0,0,0,0]# [ nDemerits, nAutoDetentions, nUniforms, nSendouts]


    i += 1
    #if i>100: break
    if b.behaviorType == 'Demerit':
        dates[b.date][b.student][0] += 1
    elif b.behaviorType == 'AutoDetention':
        dates[b.date][b.student][1] += 1
        #values[1] += 1
    elif b.behaviorType == 'Uniform':
        dates[b.date][b.student][2] += 1
        #values[2] += 1
    elif b.behaviorType == 'SendOut':
        dates[b.date][b.student][3] += 1
        #values[3] += 1


n6demerits = 0
for d in dates.keys():
    
    for s in dates[d].keys():
        if dates[d][s][0] > 5:
            n6demerits += 1
        elif dates[d][s][0] > 2:
            values[0] += 1
        elif dates[d][s][1] > 0:
            values[1] += 1
        elif dates[d][s][2] > 0:
            values[2] += 1
        elif dates[d][s][3] > 0:
            values[3] += 1

width = 0.35
ind = np.arange(len(values))

fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111)

temp = values[2:4]
values[2:4] = [0,0]
bars = ax.bar(ind+width, tuple(values), width, color='r')
barstop = ax.bar(ind+width, tuple([n6demerits,0]+temp), width, bottom=tuple(values),color='#1943BF')


ax.set_ylabel('Detentions')
ax.set_title('Detentions by Type')
ax.set_xticks(ind+width)
ax.set_xticklabels( labels )

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

#autolabel(bars)

plt.show()


blah = raw_input("waiting...")

