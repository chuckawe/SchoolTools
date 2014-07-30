#!/usr/bin/env python

import csv
reader=open('culture-analysis (1).csv', 'rb')
culture = csv.reader(reader, delimiter=',')
        	
# date dictionary
dates = {}
# listing of behaviors committed
#behaviors =[]	
# listing of IDs
#whodunit =[]
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
    
    
        
    
    n += 1
    #behaviors.append(row[4])
	#whodunit.append(row[1])

print dates
	
#print behaviors
#print whodunit


# Placeholder for reading in of lateness data
# 



reader.close()



# Discipline Policy enforced in this part of code
rownum = 0
# Loop over dates
for date in dates.keys():
    # Loop over students for that day
    pass

# Used to save header info
#    if rownum == 0:
#        header = row
#    else:
#        colnum = 0
#        for col in row:
#            print '%-8s: %s' % (header[colnum], col)
#            colnum += 1
                
#    rownum +=1
    
	
