#!/usr/bin/env python

import csv
reader=open('culture-analysis (1).csv', 'rb')
culture = csv.reader(reader, delimiter=',')
        	
# date dictionary
dates = {}

n = 0
for row in culture:
    if n>500: break
    date = row[8]
    stu_id = row[1]
    
    # Check if date is already stored
    if date not in dates.keys():
	    dates[date] = {}

    # Check if Student is already stored
    if stu_id not in dates[date].keys():
        dates[date][stu_id] = [0, 0, 0, False, True] # [ nDemerits, nAutoDTs, nSendOuts, If Late, If Late Egreg   ]

    if row[5] == 'Demeritable Behaviors':
        # This means we have a demerit
        dates[date][stu_id][0] += 1
    elif row[5] == "Auto-Detention":
        # This means we have a Auto DT assigned 
        dates[date][stu_id][1] += 1
    elif row [4] == "Sent out":
    	# This means we have a Send Out
    	dates[date][stu_id][2] +=1
    
    n += 1

print dates


# Placeholder for reading in of lateness data
#

# Discipline Policy enforced in this part of code
# Loop over dates
for date in dates.keys():
    #Total stud/day
    print date, len(dates[date].keys())

print 'hello'


# Loop over dates and returns total for each student
for date in dates.keys():
    nthdemPerDay = 0
    nthsentPerDay =0
    for stu_id in dates[date].keys():
            nDemerits= dates[date][stu_id][0]
            nAutoDTs= dates[date][stu_id][1]
            nSendOuts= dates[date][stu_id][2]
            print date, stu_id, nDemerits, nAutoDTs, nSendOuts
            if nDemerits >=3:
                nthdemPerDay +=1
            if nSendOuts >=2:
                nthsentPerDay +=1
    print 'For day,', date ,'there were' ,nthdemPerDay ,'students with 3+ Dem'
    print 'For day,', date ,'there were' ,nthsentPerDay ,'students sent out more than once'



#for date in dates.keys():
#   for stu_id in dates[date].keys():
#       for behave in dates[date][stu_id]:



# for stu_id in dates[date].keys():
#x = sum(dates[date][stu_id][0])
#print x

# [dates[date][stu_id][x] for x in dates[date].keys()]

    # Loop over student and group them into behaviors

# Used to save header info for writing new file
#    if rownum == 0:
#        header = row
#    else:
#        colnum = 0
#        for col in row:
#            print '%-8s: %s' % (header[colnum], col)
#            colnum += 1
#    rownum +=1