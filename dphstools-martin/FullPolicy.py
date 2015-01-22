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


day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#labels = ('3 Demerits','Auto Dt','Uniform','Send Out')
labels = ('Monday','Tuesday','Wednesday','Thursday','Friday')
newDetentions = [0,0,0,0,0]
oldDetentions = [0,0,0,0,0]
nDays = [0,0,0,0,0]
week_points = {}

dates = {}

i = 0
for b in behaviors:
    if b.date not in dates.keys():
        dates[b.date] = {}
    
    if b.student not in dates[b.date].keys():
        dates[b.date][b.student] = [0,0,0,0]# [ nDemerits, nAutoDetentions, nUniforms, nSendouts]


    i += 1
    #print b.date.weekday(),day_names[b.date.weekday()]
    #print b.date.date()
    #print (b.date+datetime.timedelta(days=1)).date()
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
    # Get Day
    day = d.weekday()
    #print "Checking detention for:",d.date(),"which is a",day_names[d.weekday()],"day=",day 
    if day<4:
        dt_day = day + 1
    else:
        dt_day = 0

    nDays[dt_day] +=1
    #print "Dt_day=",dt_day

    # Get date of Friday of that week
    if day==0:# Monday
        fridate = (d + datetime.timedelta(days=4)).date()
    elif day==1:# Tuesday
        fridate = (d + datetime.timedelta(days=3)).date()
    elif day==2:# Wednesday
        fridate = (d + datetime.timedelta(days=2)).date()
    elif day==3:# Thursday
        fridate = (d + datetime.timedelta(days=8)).date()
    elif day==4:# Friday
        fridate = (d + datetime.timedelta(days=7)).date()
    else: # Skip Sat and Sun
        continue

    # If not done already, add to key to points dictionary
    if fridate not in week_points.keys():
        week_points[fridate] = {}



    for s in dates[d].keys():
        # Compute points for that student
        nPointsDay = dates[d][s][0] + dates[d][s][1]*4
        # Add student to friday points dictionary
        if s not in  week_points[fridate].keys():
            week_points[fridate][s] = 0
        # Add points
        week_points[fridate][s] += nPointsDay

        
        if dates[d][s][0] > 5: # 6+ demerits
            oldDetentions[dt_day] += 1
            newDetentions[dt_day] += 1
            week_points[fridate][s] -= 6
        elif dates[d][s][0] > 2: # 3-5 Demerits
            oldDetentions[dt_day] += 1
        elif dates[d][s][1] > 0: # Auto DT
            oldDetentions[dt_day] += 1
        elif dates[d][s][2] > 0: # Uniform
            oldDetentions[dt_day] += 1
            #newDetentions[dt_day] += 1
        elif dates[d][s][3] > 0: # Sendout
            oldDetentions[dt_day] += 1
            newDetentions[dt_day] += 1

friDetentions = 0
nSaturdayDt = 0
weekDist = []
friLengthDist = []
for d in week_points.keys():
    for s in week_points[d].keys():
        nPoints = week_points[d][s]
        friTime = 0

        # For historgram
        weekDist.append(nPoints)

        # Check if over threshold
        if nPoints >= 10:
            friDetentions += 1
            friTime = 60
            for pt in xrange(11,nPoints+1):
                friTime += 5
                if pt == 22:
                    nSaturdayDt += 1
                    break
        
        if friTime >0:
            friLengthDist.append(friTime)

        

print "Number of Saturday Detentions due to points:",nSaturdayDt
print "Number of weeks:",nDays[4]
print "Average number of Saturdays:",nSaturdayDt/nDays[4]
#import sys
#sys.exit(0)

for i in xrange(0,len(oldDetentions)):
    oldDetentions[i] = oldDetentions[i]/nDays[i]
    newDetentions[i] = newDetentions[i]/nDays[i]

width = 0.35
ind = np.arange(len(labels))

fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111)

oldsystem = ax.bar(ind, tuple(oldDetentions), width, color='b')
newsystem = ax.bar(ind+width, tuple(newDetentions), width, color='#FFD966')
newfriday = ax.bar(ind+width, tuple([0,0,0,0,friDetentions/nDays[4]]), width, bottom=newDetentions,color='r')


ax.set_ylabel('Average Daily Detentions')
ax.set_title('Detentions by Day')
ax.set_xticks(ind+width)
ax.set_xticklabels( labels )
ax.legend((oldsystem[0],newsystem[0],newfriday[0]),('Old System','New System','Week Points'),'upper right')


fig2 = plt.figure(facecolor='w')
ax2 = fig2.add_subplot(111)

# histogram of detention time
n, bins, patches = ax2.hist(friLengthDist,facecolor='green',bins=7)
ax2.set_xlabel('Minutes of Friday Detention')
ax2.set_ylabel('Number of Students')

fig3 = plt.figure(facecolor='w')
ax3 = fig3.add_subplot(111)

# histogram of points
n, bins, patches = ax3.hist(weekDist,facecolor='orange',bins=7,log=False)#normed=True)
ax3.set_xlabel('Point earned in a week')
ax3.set_ylabel('Number of Students')

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

#autolabel(bars)

plt.show()


blah = raw_input("waiting...")

