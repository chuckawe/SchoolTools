#!/usr/bin/python

from Student import *
from Course import *
from Exam import *
from Readers import *
import subprocess,os,os.path
import argparse

def total(d):
    
    t = 0
    for k in d:
        t += d[k]

    return t

parser = argparse.ArgumentParser(description="""
Democracy Prep Dashboard Puller\r
This program reads Democracy Prep student records and pulls the information 
needed for the school's dashboard.
""")

splash = """
######################################
#                                    #
#  DEMOCRACY PREP DASHBOARD PULLER   #
#    If any problems please contact  #
#    bmartin@democracyprep.org       #
#                                    #
######################################
"""

print splash

students = []

data_read = StudentDataReader('data/DPStudentData.xlsx')
data_read.get_data(students)
            

print 'Reading Course grades'

cur_read = CourseCurrentReader('data/DPCourseCurrent.xlsx')
cur_read.get_courses(students,final_term='YR')  # SET THIS TO TAKE THE DESIRED TERM

label = '1-24-2014'
listFile = open('Dashboard'+label+'.csv','w')
headerStr = 'Category,School,9th,10th,11th,12th'

listFile.write(headerStr+'\n')

litTotal =    {9:0,10:0,11:0,12:0}
litPass =     {9:0,10:0,11:0,12:0}
lit83   =     {9:0,10:0,11:0,12:0}
writingTotal ={9:0,10:0,11:0,12:0}
writingPass = {9:0,10:0,11:0,12:0}
writing83  =  {9:0,10:0,11:0,12:0}
mathTotal =   {9:0,10:0,11:0,12:0}
mathPass =    {9:0,10:0,11:0,12:0}
math83   =    {9:0,10:0,11:0,12:0}
scienceTotal ={9:0,10:0,11:0,12:0}
sciencePass = {9:0,10:0,11:0,12:0}
science83   = {9:0,10:0,11:0,12:0}
historyTotal ={9:0,10:0,11:0,12:0}
historyPass = {9:0,10:0,11:0,12:0}
history83   = {9:0,10:0,11:0,12:0}
koreanTotal = {9:0,10:0,11:0,12:0}
koreanPass =  {9:0,10:0,11:0,12:0}
korean83   =  {9:0,10:0,11:0,12:0}

for stu in students:
    grade = stu.get_hs_grade()
    if grade > 12:
        grade = 12
    for course in stu.get_courses(2013):
        if 'Literature' in course.title or 'AP Lang' in course.title:
            litTotal[grade] += 1

            if course.numAvg > 82.4:
                litPass[grade] += 1
                lit83[grade]   += 1
            elif course.numAvg > 69.4:
                litPass[grade] +=1
        if 'Writing' in course.title:
            writingTotal[grade] += 1
            if course.numAvg > 82.4:
                writingPass[grade] += 1
                writing83[grade]   += 1
            elif course.numAvg > 69.4:
                writingPass[grade] +=1
        if 'Algebra' in course.title or 'Geometry' in course.title or 'Calculus' in course.title:
            mathTotal[grade] += 1
            if course.numAvg > 82.4:
                mathPass[grade] += 1
                math83[grade]   += 1
            elif course.numAvg > 69.4:
                mathPass[grade] +=1
        if 'Physics' in course.title or 'Biology' in course.title or 'Chemistry' in course.title or 'Science' in course.title:
            scienceTotal[grade] += 1
            if course.numAvg > 82.4:
                sciencePass[grade] += 1
                science83[grade]   += 1
            elif course.numAvg > 69.4:
                sciencePass[grade] +=1
        if 'History' in course.title or 'Sociology' in course.title:
            historyTotal[grade] += 1
            if course.numAvg > 82.4:
                historyPass[grade] += 1
                history83[grade]   += 1
            elif course.numAvg > 69.4:
                historyPass[grade] +=1
        if 'Korean' in course.title:
            koreanTotal[grade] += 1
            if course.numAvg > 82.4:
                koreanPass[grade] += 1
                korean83[grade]   += 1
            elif course.numAvg > 69.4:
                koreanPass[grade] +=1
        

lineStr = ''
lineStr += '# of Scholars Passing Math,'+str(total(mathPass))+','+str(mathPass[9])+','+str(mathPass[10])+','+str(mathPass[11])+','+str(mathPass[12])+'\n'
lineStr += '# of Scholars Earning 83+ in Math,'+str(total(math83))+','+str(math83[9])+','+str(math83[10])+','+str(math83[11])+','+str(math83[12])+'\n'

lineStr += '# of Scholars Passing Lit,'+str(total(litPass))+','+str(litPass[9])+','+str(litPass[10])+','+str(litPass[11])+','+str(litPass[12])+'\n'
lineStr += '# of Scholars Earning 83+ in Lit,'+str(total(lit83))+','+str(lit83[9])+','+str(lit83[10])+','+str(lit83[11])+','+str(lit83[12])+'\n'

lineStr += '# of Scholars Passing Writing,'+str(total(writingPass))+','+str(writingPass[9])+','+str(writingPass[10])+','+str(writingPass[11])+','+str(writingPass[12])+'\n'
lineStr += '# of Scholars Earning 83+ in Writing,'+str(total(writing83))+','+str(writing83[9])+','+str(writing83[10])+','+str(writing83[11])+','+str(writing83[12])+'\n'

lineStr += '# of Scholars Passing Science,'+str(total(sciencePass))+','+str(sciencePass[9])+','+str(sciencePass[10])+','+str(sciencePass[11])+','+str(sciencePass[12])+'\n'
lineStr += '# of Scholars Earning 83+ in Science,'+str(total(science83))+','+str(science83[9])+','+str(science83[10])+','+str(science83[11])+','+str(science83[12])+'\n'

lineStr += '# of Scholars Passing History,'+str(total(historyPass))+','+str(historyPass[9])+','+str(historyPass[10])+','+str(historyPass[11])+','+str(historyPass[12])+'\n'
lineStr += '# of Scholars Earning 83+ in History,'+str(total(history83))+','+str(history83[9])+','+str(history83[10])+','+str(history83[11])+','+str(history83[12])+'\n'

lineStr += '# of Scholars Passing Korean,'+str(total(koreanPass))+','+str(koreanPass[9])+','+str(koreanPass[10])+','+str(koreanPass[11])+','+str(koreanPass[12])+'\n'
lineStr += '# of Scholars Earning 83+ in Korean,'+str(total(korean83))+','+str(korean83[9])+','+str(korean83[10])+','+str(korean83[11])+','+str(korean83[12])+'\n'

lineStr += '%% of Scholars Passing Math,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f' % ( float(total(mathPass))/total(mathTotal),float(mathPass[9])/mathTotal[9],float(mathPass[10])/mathTotal[10],float(mathPass[11])/mathTotal[11],float(mathPass[12])/mathTotal[12] ) + '\n'
lineStr += '%% of Scholars Earning 83+ in Math,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f' % ( float(total(math83))/total(mathTotal),float(math83[9])/mathTotal[9],float(math83[10])/mathTotal[10],float(math83[11])/mathTotal[11],float(math83[12])/mathTotal[12] ) + '\n'

lineStr += '%% of Scholars Passing Literature,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f' % ( float(total(litPass))/total(litTotal),float(litPass[9])/litTotal[9],float(litPass[10])/litTotal[10],float(litPass[11])/litTotal[11],float(litPass[12])/litTotal[12] ) + '\n'
lineStr += '%% of Scholars Earning 83+ in Literature,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f' % ( float(total(lit83))/total(litTotal),float(lit83[9])/litTotal[9],float(lit83[10])/litTotal[10],float(lit83[11])/litTotal[11],float(lit83[12])/litTotal[12] ) + '\n'

lineStr += '%% of Scholars Passing Writing,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f' % ( float(total(writingPass))/total(writingTotal),float(writingPass[9])/writingTotal[9],float(writingPass[10])/writingTotal[10],float(writingPass[11])/writingTotal[11],0.0 ) + '\n'
lineStr += '%% of Scholars Earning 83+ in Writing,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f' % ( float(total(writing83))/total(writingTotal),float(writing83[9])/writingTotal[9],float(writing83[10])/writingTotal[10],float(writing83[11])/writingTotal[11],0.0) + '\n'

lineStr += '%% of Scholars Passing Science,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f' % ( float(total(sciencePass))/total(scienceTotal),float(sciencePass[9])/scienceTotal[9],float(sciencePass[10])/scienceTotal[10],float(sciencePass[11])/scienceTotal[11],float(sciencePass[12])/scienceTotal[12] ) + '\n'
lineStr += '%% of Scholars Earning 83+ in Science,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f' % ( float(total(science83))/total(scienceTotal),float(science83[9])/scienceTotal[9],float(science83[10])/scienceTotal[10],float(science83[11])/scienceTotal[11],float(science83[12])/scienceTotal[12] ) + '\n'

lineStr += '%% of Scholars Passing History,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f' % ( float(total(historyPass))/total(historyTotal),float(historyPass[9])/historyTotal[9],float(historyPass[10])/historyTotal[10],float(historyPass[11])/historyTotal[11],float(historyPass[12])/historyTotal[12] ) + '\n'
lineStr += '%% of Scholars Earning 83+ in History,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f' % ( float(total(history83))/total(historyTotal),float(history83[9])/historyTotal[9],float(history83[10])/historyTotal[10],float(history83[11])/historyTotal[11],float(history83[12])/historyTotal[12] ) + '\n'

lineStr += '%% of Scholars Passing Korean,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f' % ( float(total(koreanPass))/total(koreanTotal),float(koreanPass[9])/koreanTotal[9],float(koreanPass[10])/koreanTotal[10],float(koreanPass[11])/koreanTotal[11],float(koreanPass[12])/koreanTotal[12] ) + '\n'
lineStr += '%% of Scholars Earning 83+ in Korean,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f' % ( float(total(korean83))/total(koreanTotal),float(korean83[9])/koreanTotal[9],float(korean83[10])/koreanTotal[10],float(korean83[11])/koreanTotal[11],float(korean83[12])/koreanTotal[12] ) + '\n'


listFile.write(lineStr)
listFile.close()
        
        
