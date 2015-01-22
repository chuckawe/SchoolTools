#!/usr/bin/python

from Student import *
from Course import *
from Exam import *
from Transcript import *
from Readers import *
import subprocess,os,os.path
import argparse

parser = argparse.ArgumentParser(description="""
Democracy Prep Attendance Summarizer\r
This program reads Democracy Prep student records and generates a spreadsheet
with a summary of each student's attendance.
""")
parser.add_argument('-i', dest='input_file', help='Attendance file from jupiter.')
args = parser.parse_args()

splash = """
#########################################
#                                       #
#  DEMOCRACY PREP ATTENDANCE SUMMARIZER #
#    If any problems please contact     #
#    bmartin@democracyprep.org          #
#                                       #
#########################################
"""

print splash

students = []

data_read = StudentDataReader('data/DPStudentData.xlsx')
data_read.get_data(students)
            

P  = {}
A  = {}
L  = {}
SO = {}
SO1= {}
SO2= {}
SOI= {}
SI = {}


import csv
with open(args.input_file,'rb') as csvfile:
    data = csv.reader(csvfile,delimiter=',')
    n=0
    for row in data:
        n+=1
        if n==1: continue
        i = 0
        ID = 0
        for cell in row:
            if i == 2:
                ID = int(cell)
                if ID not in P.keys():
                    P[ID] = 0  
                    A[ID] = 0 
                    L[ID] = 0  
                    SO[ID] = 0 
                    SO1[ID] = 0
                    SO2[ID] = 0
                    SOI[ID] = 0
                    SI[ID] = 0
            elif i == 3:
                if cell == 'P':
                    P[ID] += 1
                elif cell == 'A':
                    A[ID] += 1
                elif cell == 'L':
                    L[ID] += 1
                elif cell == 'SO':
                    SO[ID] += 1
                elif cell == 'SO1':
                    SO1[ID] += 1
                elif cell == 'SO2':
                    SO2[ID] += 1
                elif cell == 'SOI':
                    SOI[ID] += 1
                elif cell == 'SI':
                    SI[ID] += 1


            i+=1


listFile = open('AttendanceSummary.csv','w')
headerStr = 'StudentID,LastName,FirstName,School,Grade,IEP,504,ELL,P,A,L,SO,SO1,SO2,SOI,SI,AllSusp'

listFile.write(headerStr+'\n')


for stu in students:
    # 'StudentID,LastName,FirstName,School,Grade,IEP,504,ELL,P,A,L,SO,SO1,SO2,SOI,SI,AllSusp'    
    lineStr = '%i,%s,%s,DPCHS,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i' % (stu.stuID,stu.last,stu.first,stu.get_hs_grade(),int(stu.HasIEP),int(stu.Has504),int(stu.IsELL),P[stu.stuID],A[stu.stuID],L[stu.stuID],SO[stu.stuID],SO1[stu.stuID],SO2[stu.stuID],SOI[stu.stuID],SI[stu.stuID],SO[stu.stuID]+SO1[stu.stuID]+SO2[stu.stuID]+SOI[stu.stuID]+SI[stu.stuID])
    listFile.write(lineStr+'\n')
listFile.close()

