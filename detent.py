#!/usr/bin/env python

import csv
reader=open('culture-analysis (1).csv', 'rb')
culture = csv.reader(reader, delimiter=',')

<<<<<<< HEAD
# date listing of culture
dates ={}
# listing of behaviors committed
# behaviors =[]	
# listing of IDs
# whodunit =[]
n=0
for row in culture:
    if n>100: break
    date = row[8]
    stud_id = row[1]
    if date not in dates.keys():
        dates[date] = {}
        
    if stud_id not in date[dates].keys():
        dates[dates][stud_id] = []
        
        
        	
=======
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
        dates[date][stu_id] = [0, 0, 0, 0, False] # [ nDemerits, nUniViolations, nAutoDTs, nSendOuts, If Late   ]
>>>>>>> dc477eff368bfaf9c402ea64a8810be5414a485c
	
    if row[5] == 'Demeritable Behaviors':
        # This means we have a demerit
        dates[date][stu_id][0] += 1
    elif row[4] == "Uniform":
        # This means we have a uniform violation
        dates[date][stu_id][1] += 1
        
    
    n += 1
    #behaviors.append(row[4])
	#whodunit.append(row[1])

print dates
<<<<<<< HEAD
	
=======
#print behaviors
#print whodunit


# Placeholder for reading in of lateness data
# 



>>>>>>> dc477eff368bfaf9c402ea64a8810be5414a485c
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
    
	
