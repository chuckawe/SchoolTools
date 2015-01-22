#!/usr/bin/python

from Student import *
from Course import *
from Exam import *
from Transcript import *
from Readers import *
import subprocess,os,os.path
import argparse

parser = argparse.ArgumentParser(description="""
Democracy Prep GPA Calculator\r
This program reads Democracy Prep student records and generates a spreadsheet with the selected
student's GPAs produced according to the users needs.
""")
parser.add_argument('studentIDs',nargs='*',type=int,
                   help='List of Student IDs for whom GPAs should be generated.  LEAVE BLANK FOR ALL STUDENTS.')
parser.add_argument('--grade',type=int, dest='grade_filt',
                   default=-1, help='Select students by grade level.')
parser.add_argument('--dir',type=str, dest='dir',
                   default='tmp', help='Output directory for transcript files.')
parser.add_argument('--year', type=int,dest='year', help='Enrollment year (specified as leading year)')
parser.add_argument('--school',type=str, dest='school',
                   default='DPCHS', help='DP High School for which to create transcripts.')
args = parser.parse_args()

splash = """
######################################
#                                    #
#  DEMOCRACY PREP REGENTS SUMMARIZER #
#    If any problems please contact  #
#    bmartin@democracyprep.org       #
#                                    #
######################################
"""

print splash

if args.school == 'DPCHS':
    print "Loading data from Democracy Prep Charter High School (DPCHS)"
elif args.school == 'DPHHS':
    print "Loading data from Democracy Prep Harlem High School (DPHHS)"
elif args.school == 'BXPHS':
    print "Bronx Prep High School (BXPHS) transcripts not available yet."
else:
    print "Unknown school: " + args.school + " please specify either DPCHS or DPHHS"

students = []
for ID in args.studentIDs:
    students.append(Student(stuID=ID))

data_read = StudentDataReader('data/'+args.school+'_StudentData.xlsx')
while data_read.next_sheet():
    data_read.get_data(students,year=args.year)
    print "Found",len(students),"thus far."

regentsList = [ 
            'Integrated Algebra',
            'Algebra I (Common Core)',
            'Living Environment',
            'Global History',
            'Geometry',
            'Geometry (Common Core)',
            'Chemistry',
            'English',
            'English (Common Core)',
            'US History',
            'Algebra II/Trigonometry',
            'Physics',
            'Korean'
            ]
            #'Spanish',
            #'French',
            #'Mathematics A',
            #'Earth Science'
            #'Italian',
            

reg_read = RegentsReader('data/'+args.school+'_RegentsData.xlsx')
while reg_read.next_sheet():
    reg_read.get_exams(students)


outDir = os.path.expanduser("~")+'/Desktop/'+args.dir
if not os.path.isdir(outDir):
    os.makedirs(outDir)

listFileStr = outDir+'/RegentsSummary.csv'
print "Saving Regents Summary to:",listFileStr
listFile = open(listFileStr,'w')
headerStr = 'StudentID,LastName,FirstName,GradYear,Honors,ScienceHonors,MathHonors,Advanced,Regular,MetELA,MetMath,RegAvg'
for regents in regentsList:
    headerStr += ','
    headerStr += regents

listFile.write(headerStr+'\n')


for stu in students:
    lineStr = '%s,%s,%s,%i' % (stu.stuID,stu.last,stu.first,stu.gradYear)
    
    avg = stu.get_regents_average()

    if avg > 89.50000: lineStr += ',Yes'
    else:                           lineStr += ',No'

    if stu.meets_science_honors(): lineStr += ',Yes' 
    else:                           lineStr += ',No'
    
    if stu.meets_math_honors(): lineStr += ',Yes' 
    else:                           lineStr += ',No'

    if stu.meets_advanced_diploma():  lineStr += ',Yes'
    else:                           lineStr += ',No'

    if stu.meets_regents_diploma():   lineStr += ',Yes'
    else:                           lineStr += ',No'
    
    ELA = stu.get_highest_exam(examType='Regents',subject='English')
    if ELA != None and ELA.score  >= 75:  lineStr += ',Yes'
    else:                           lineStr += ',No'

    alg = stu.get_highest_exam(examType='Regents',subject='Integrated Algebra')
    geo = stu.get_highest_exam(examType='Regents',subject='Geometry')
    alg2= stu.get_highest_exam(examType='Regents',subject='Algebra II/Trigonometry')
    if (alg != None and alg.score >= 80) or \
       (geo != None and geo.score >= 80) or \
       (alg2!= None and alg2.score >= 80): 
        lineStr += ',Yes'
    else:                           lineStr += ',No'
    

    lineStr += ',%02f' % avg 

    for regents in regentsList:
        exam = stu.get_highest_exam(examType='Regents',subject=regents)
        lineStr += ','
        if exam != None:
            lineStr += str(exam.score)
        
    listFile.write(lineStr+'\n')

listFile.close()

