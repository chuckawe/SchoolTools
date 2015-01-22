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
parser.add_argument('--school',type=str, dest='school',
                   default='DPCHS', help='DP High School for which to create transcripts.')
parser.add_argument('--grade',type=int, dest='grade_filt',
                   default=-1, help='Select students by grade level.')
parser.add_argument('--dir',type=str, dest='dir',
                   default='tmp', help='Output directory for transcript files.')
parser.add_argument('--NoCurrent', dest='UseCurrent', action='store_false',
                   default=True, help='Switch off reporting of current course grades.')
parser.add_argument('--year', type=int,dest='year', help='Enrollment year (specified as leading year)')
args = parser.parse_args()

splash = """
######################################
#                                    #
#  DEMOCRACY PREP GPA CALCULATOR     #
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
    

if args.grade_filt != -1:
    students = [student for student in students if student.get_hs_grade() == args.grade_filt]
            
course_read = CourseReader('data/'+args.school+'_CourseData.xlsx')
course_read.get_courses(students)

if args.UseCurrent:
    currentFile = 'data/DPCourseCurrent.xlsx'
    print 'Reading current year grades from',currentFile
    cur_read = CourseCurrentReader(currentFile)
    cur_read.get_courses(students,final_term='T1') # Set this to desired term


outDir = os.path.expanduser("~")+'/Desktop/'+args.dir
if not os.path.isdir(outDir):
    os.makedirs(outDir)
gpa_file = outDir+'/GPA.csv'
print "Saving GPAs to",gpa_file
listFile = open(gpa_file,'w')
listFile.write('StudentID,LastName,FirstName,Grade,NumAvg,WeightedGPA,UnweightedGPA,WeightedCoreGPA,CoreGPA\n')


for stu in students:
    num_avg = stu.compute_gpa(weighted=False,year=None,coreOnly=False,use4Scale=False)
    #print stu.last,stu.first,' has a num avg of ', num_avg
    w_gpa = stu.compute_gpa(weighted=True,year=None,coreOnly=False)
    #print stu.last,stu.first,' has a weighted gpa of ', w_gpa
    gpa = stu.compute_gpa(weighted=False,year=None,coreOnly=False)
    #print stu.last,stu.first,' has a gpa of ', gpa
    w_core_gpa = stu.compute_gpa(weighted=True,year=None,coreOnly=True) 
    #print stu.last,stu.first,' has a weighted core gpa of ', w_core_gpa
    core_gpa = stu.compute_gpa(weighted=False,year=None,coreOnly=True) 
    #print stu.last,stu.first,' has a core gpa of ', core_gpa
    line = '%s,%s,%s,%i,%f,%f,%f,%f,%f\n' % (stu.stuID,stu.last,stu.first,stu.get_hs_grade(),num_avg,w_gpa,gpa,w_core_gpa,core_gpa)
    listFile.write(line)

listFile.close()

