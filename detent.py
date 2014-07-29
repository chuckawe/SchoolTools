#!/usr/bin/env python

import csv
reader=open('culture-analysis (1).csv', 'rb')
culture = csv.reader(reader, delimiter=',')

dates =[]
# date listing of culture
behaviors =[]	
# listing of behaviors committed
whodunit =[]
# listing of IDs
for row in culture:
	dates.append(row[8])
	behaviors.append(row[4])
	whodunit.append(row[1])
	
print dates
print behaviors
print whodunit
	
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
    
	