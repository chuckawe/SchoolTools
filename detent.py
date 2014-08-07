#!/usr/bin/env python

import csv
reader=open('culture-analysis (1).csv', 'rb')
culture = csv.reader(reader, delimiter=',')
        	
# date dictionary
dates = {}

n = 0
for row in culture:
    if n>5000: break
    date = row[8]
    stu_id = row[1]
    
    # Check if date is already stored
    if date not in dates.keys():
	    dates[date] = {}

    # Check if Student is already stored
    if stu_id not in dates[date].keys():
        dates[date][stu_id] = [0, 0, 0, False, True] # [ nDemerits, nAutoDTs, nSendOuts, If Late, If Late Egreg   ]

    if row[5] == "Demeritable Behaviors":
        # This means we have a demerit
        dates[date][stu_id][0] += 1
    elif row[5] == "Auto-Detention" or row[4] == "Missed DT":
        # This means we have a Auto DT assigned 
        dates[date][stu_id][1] += 1
    elif row [4] == "Sent out" or "Sent out - Teacher follow up":
    	# This means we have a Send Out
    	dates[date][stu_id][2] +=1
    
n += 1

#print dates


# Placeholder for reading in of lateness data
#

# Discipline Policy enforced in this part of code
# Loop over dates
#for date in dates.keys():

#print 'hello'



# Loop over dates and returns total for each student
for date in dates.keys():
    #Total students/day
    stnum=[0,0,0,0,0] # [nthdemPerDay, nthsentPerDay, nthdetPerDay,Demcap,SentCap]
#    DEM = raw_input('What should demerit limit be\n')
    for stu_id in dates[date].keys():
#           studentDate ={}
            nDemerits= dates[date][stu_id][0]
            nSendOuts= dates[date][stu_id][2]
            nAutoDTs= dates[date][stu_id][1]
            print date, stu_id, nDemerits, nSendOuts, nAutoDTs
            if nDemerits >=3:
                stnum[0] += 1
            elif nDemerits >0:
                stnum[3] += 1
                    #checks for 3+
            if nSendOuts >1:
                stnum[1] +=1
            elif nSendOuts >0:
                stnum[4] +=1
                    #checks sendout 2 or more
            if nAutoDTs >0:
                stnum[2] +=1
                    #checks given Auto
                    
#            if stu_id not in studentDate.keys():
#                studentDate[stu_id]=[]
#                studentDate[stu_id].append(date)
#           elif stu_id in studentDate.keys:
#               for stu_id in studentDate[stu_id]:
#                   stnum =+1
#            print len(studentDate.keys()), stnum,
    print date, len(dates[date].keys())
    print 'For day,', date ,'there were' ,stnum[3] ,'student(s) given a Dem,', stnum[0], 'given 3+ for the day'
    print 'For day,', date ,'there were' ,stnum[4] ,'student(s) sent out,', stnum[1], 'sent out more than once'
    print 'For day,', date ,'there were' ,stnum[2] ,'student(s) given Auto DT'



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