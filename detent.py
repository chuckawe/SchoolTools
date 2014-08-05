#!/usr/bin/env python

import csv
reader=open('culture-analysis (1).csv', 'rb')
culture = csv.reader(reader, delimiter=',')
        	
# date dictionary
dates = {}

n = 0
for row in culture:
    if n>100: break
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
    elif row [4] == "Sent Out":
    	# This means we have a Send Out
    	dates[date][stu_id][2] +=1
# elif
    
    n += 1

print dates
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> master
=======
>>>>>>> 05c3acc949cd199d739307e4e510f59cbbca32b4
=======
>>>>>>> master

# Placeholder for reading in of lateness data
# 


<<<<<<< HEAD
# Discipline Policy enforced in this part of code
# Loop over dates
for date in dates.keys():
=======
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> master
# Discipline Policy enforced in this part of code
# Loop over dates
for date in dates.keys():
    # Total students
    print date, len(dates[date].keys())
<<<<<<< HEAD

print 'hello'
n=0
# Loop over dates and returns total for each student
for date in dates.keys():
    for stu_id in dates[date].keys():
            nDemerits= dates[date][stu_id][0]
            nAutoDTs= dates[date][stu_id][1]
            nSendOuts= dates[date][stu_id][2]
            print date, stu_id, nDemerits, nAutoDTs, nSendOuts

=======

print 'hello'
n=0
# Loop over dates and returns total for each student
for date in dates.keys():
    for stu_id in dates[date].keys():
            nDemerits= dates[date][stu_id][0]
            nAutoDTs= dates[date][stu_id][1]
            nSendOuts= dates[date][stu_id][2]
            print date, stu_id, nDemerits, nAutoDTs, nSendOuts

>>>>>>> master
# for stu_id in dates[date].keys():
    x = sum(dates[date][stu_id][0])
    print x

# [dates[date][stu_id][x] for x in dates[date].keys()]

    # Loop over student and group them into behaviors
<<<<<<< HEAD

<<<<<<< HEAD
=======
reader.close()

>>>>>>> 05c3acc949cd199d739307e4e510f59cbbca32b4
# Discipline Policy enforced in this part of code
# Loop over dates
for date in dates.keys():
<<<<<<< HEAD
    # Loop over students for that day
    if stu_id in dates.[date]:
    	
=======
>>>>>>> origin/from-school
    # Total students
    print date, len(dates[date].keys())

print 'hello'

# Loop over dates and returns total for each student
for date in dates.keys():
    for stu_id in dates[date].keys():
        nDemerits= dates[date][stu_id][0]
        nAutoDTs= dates[date][stu_id][1]
        nSendOuts= dates[date][stu_id][2]
<<<<<<< HEAD

        print date, stu_id, nDemerits, nAutoDTs, nSendOuts

# for stu_id in dates[date].keys():
    x = sum(dates[date][stu_id][0])
    print x

# [dates[date][stu_id][x] for x in dates[date].keys()]

    # Loop over student and group them into behaviors

=======
    print date, stu_id, nDemerits, nAutoDTs, nSendOuts

[dates[date][stu_id][x] for x in dates[date].keys()]

    # Loop over student and group them into behaviors
>>>>>>> 05c3acc949cd199d739307e4e510f59cbbca32b4
    pass
=======
>>>>>>> master
=======

>>>>>>> master
>>>>>>> origin/from-school

# Used to save header info for writing new file
#    if rownum == 0:
#        header = row
#    else:
#        colnum = 0
#        for col in row:
#            print '%-8s: %s' % (header[colnum], col)
#            colnum += 1
                
#    rownum +=1
    
	
