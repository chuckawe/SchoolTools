#!/usr/bin/python

from Student import *
from Course import *
from Exam import *
from Transcript import *
from Readers import *
import subprocess,os,os.path
import argparse

parser = argparse.ArgumentParser(description="""
Democracy Prep ATS Credit Counter\r
This program reads Democracy Prep student records and generates a spreadsheet
with the number of ATS credits earned for each student..
""")
parser.add_argument('studentIDs',nargs='*',type=int,
                   help='List of Student IDs for whom credits should be generated.  LEAVE BLANK FOR ALL STUDENTS.')
parser.add_argument('--school',type=str, dest='school',
                   default='DPCHS', help='DP High School for which to generate credits.')
parser.add_argument('--year',type=str, dest='year',
                   help='Should be year at start of academic year (Ex for 2013-2014 use 2013).')

args = parser.parse_args()

splash = """
######################################
#                                    #
#  DEMOCRACY PREP ATS CREDIT COUNTER #
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
    print "Bronx Prep High School (BXPHS) credits not available yet."
else:
    print "Unknown school: " + args.school + " please specify either DPCHS or DPHHS"

students = []
for ID in args.studentIDs:
    students.append(Student(stuID=ID))

data_read = StudentDataReader('data/'+args.school+'_StudentData.xlsx')
if(data_read.set_sheet(args.year+'-'+str(int(args.year)+1))):
    print 'Sheet:',args.year+'-'+str(int(args.year)+1),'not found'
data_read.get_data(students)
print "Found",len(students),"students"
            

print 'Reading Course grades'
cur_read = CourseCurrentReader('data/'+args.school+'_CourseCurrent.xlsx')
cur_read.get_courses(students,final_term='F3')  # SET THIS TO TAKE THE DESIRED TERM
course_read = CourseReader('data/'+args.school+'_CourseData.xlsx')
course_read.get_courses(students)

listFile = open('ATSCredits.csv','w')
headerStr = 'StudentID,LastName,FirstName,Math,Science,English,SocialScience,Other'

listFile.write(headerStr+'\n')

# To get list of unique courses:
#       =INDEX(Grades!$G$2:$G$10538,MATCH(0,INDEX(COUNTIF($A$1:A1,Grades!$G$2:$G$10538),0,0),0))
# Lookups for subjects
math_courses = {}
#math_courses = {
#'Integrated Algebra':2,
#'Geometry (Hon) 9th':2,
#'Geometry':2,
#'Geometry Accelerated':2,
#'Geometry (Hon)':2,
#'Algebra II':2,
#'Algebra II Accelerated':2,
#'Algebra II/Trigonometry (Hon)':2,
#'Pre-Calculus':2,
#'Intro to Calculus':2,
#'SAT Prep: Math':0.5
#}
scie_courses = {}
#scie_courses = {
#'Biology':2,
#'Chemistry':2,
#'Chemistry (Hon)':2,
#'Physics':2,
#'Physics (Hon)':2,
#'Topics in Physics':1,
#'Scientific Literacy':1,
#'AP Biology':2,
#'AP Physics':2,
#'Global Environment (SUNY-ESF)':2
#}
engl_courses = {}
#engl_courses = {
#'Writing I':2,
#'Writing II':2,
#'Literature I':2,
#'Literature II':2,
#'Literature III':2,
#'Literature Studies I':2,
#'Literature Studies II':2,
#'American Literature':2,
#'Writing III':2,
#'Senior Literature':2,
#'AP English Language and Composition':2,
#'SAT Prep: Critical Reading':0.5
#}
socs_courses = {}
#'Global History I: Mesopotamia to Renaissance':2,
#'Global History II: Enlightenment to Present Day':2,
#'Global History I':2,
#'Global History II':2,
#'U.S. History':2,
#'U.S. History (Hon)':2,
#'Applied Civics II: Seminar in American Democracy':2,
#'Seminar in American Democracy':2,
#'Economics':1,
#'SAT Prep/CTW':1
#}
othr_courses = {}
#'Korean I':2,
#'Korean II':2,
#'Korean III':2,
#'Korean IV - Regents Prep':2,
#'Korean Literature & Culture':2,
#'College Readiness':0.5,
#'Physical Education':1,
#'Theatre: Scene Study and Process':1,
#'Theatre for Social Change with The Laramie Project':1
#}


catalog = ReadGoogleSheet('DPHSCourseCatalog','Courses',['Department','Course Title','Credits'])

for course in catalog:
    # Check department and assign to credit category
    if course[0] == 'Mathematics':
        math_courses[course[1]] = float(course[2])
    elif course[0] == 'Science':
        scie_courses[course[1]] = float(course[2])
    elif course[0] == 'English':
        engl_courses[course[1]] = float(course[2])
    elif course[0] == 'History & Civics':
        socs_courses[course[1]] = float(course[2])
    else:
        #print 'Adding',course[1],'as an OTHER course'
        othr_courses[course[1]] = float(course[2])

for stu in students:
    math_credits = 0.0
    scie_credits = 0.0
    engl_credits = 0.0
    socs_credits = 0.0
    othr_credits = 0.0
    for course in stu.get_courses(int(args.year)):
        
        # Determine fraction of full course credits that student earned
        multiplier = 0.0
        #if 'F3' in course.term_grades.keys() and course.numAvg > 69.4: 
        #    multiplier = 1.0
        #else:
        if course.credits_earned() > 0:
            multiplier = 1.0
        else:
            for det_course in stu.get_courses(int(args.year)+1):
                if det_course.title == course.title:
                    #print 'Found matched trimester grade for',det_course.title,det_course.term_grades.keys()
                    for term in ['F1','F2']:
                        if term in det_course.term_grades.keys() and det_course.term_grades[term] > 69.4:
                            multiplier += 0.33
                            #print 'Added 1/3 credit trimester grade for',det_course.title,det_course.term_grades.keys()
            
        if course.title in math_courses.keys():
            math_credits += (multiplier*math_courses[course.title])
        elif course.title in scie_courses.keys():
            scie_credits += (multiplier*scie_courses[course.title])
        elif course.title in engl_courses.keys():
            engl_credits += (multiplier*engl_courses[course.title])
        elif course.title in socs_courses.keys():
            socs_credits += (multiplier*socs_courses[course.title])
        elif course.title in othr_courses.keys():
            othr_credits += (multiplier*othr_courses[course.title])
        else:
            print 'Cannot find course:',course.title

    # Get Summer school credits
    #for course in stu.get_courses(2012):
    #    if not course.PassSummer:
    #        continue
    #        
    #    if course.title in math_courses.keys():
    #        math_credits += 1.0
    #    elif course.title in scie_courses.keys():
    #        scie_credits += 1.0
    #    elif course.title in engl_courses.keys():
    #        engl_credits += 1.0
    #    elif course.title in socs_courses.keys():
    #        socs_credits += 1.0
    #    elif course.title in othr_courses.keys():
    #        othr_credits += 1.0
    #    else:
    #        print 'Cannot find Summer School course:',course.title

    
    if (math_credits+scie_credits+engl_credits+socs_credits+othr_credits)>0.0:
        #print stu.stuID,stu.last,stu.first,math_credits,scie_credits,engl_credits,socs_credits,othr_credits
        lineStr = '%i,%s,%s,%.2f,%.2f,%.2f,%.2f,%.2f' % (stu.stuID,stu.last,stu.first,math_credits,scie_credits,engl_credits,socs_credits,othr_credits)
        listFile.write(lineStr+'\n')
listFile.close()

