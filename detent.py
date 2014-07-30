#!/usr/bin/env python

import csv
reader=open('culture-analysis (1).csv', 'rb')
culture = csv.reader(reader, delimiter=',')

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
        
        
        	
	
print dates
	
reader.close()

rownum = 0
for row in culture:
    # Used to save header info
    if rownum == 0:
        header = row
    else:
        colnum = 0
        for col in row:
            print '%-8s: %s' % (header[colnum], col)
            colnum += 1
                
    rownum +=1
    
	