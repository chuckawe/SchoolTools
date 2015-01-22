#!/usr/bin/python

from Student import *
from Course import *
from Exam import *
from Transcript import *
from Readers import *

students = []
#students.append(
#        Student(
#        first='Jonathan', 
#        last='Mejia', 
#        stuID=202599809,
#        gradYear=2013)
#        )
#
#students.append(
#        Student(
#        first='Jamie', 
#        last='McCoy', 
#        stuID=271008179,
#        gradYear=2013)
#        )
students.append(
        Student(
        first='Cyinthia', 
        last='Castillo', 
        stuID=269314928,
        gradYear=2013)
        )
data_read = StudentDataReader('data/DPStudentData.xlsx')
data_read.get_data(students)

course_read = CourseReader('data/DPCourseData.xlsx')
course_read.get_courses(students)


#for stu in students:
#    stu.add_course(Course(title='Physics',year=2011,level=1,numAvg=87.42,nCredits=3))
#    stu.add_course(Course(title='Algebra',year=2009,level=1,numAvg=82.24,nCredits=3))
#    stu.add_course(Course(title='Literature I',year=2009,level=1,numAvg=73.85,nCredits=2))
#    stu.add_course(Course(title='Elective',year=2009,level=1,numAvg=95.41,nCredits=1.5))
#    stu.add_course(Course(title='Global History I',year=2009,level=1,numAvg=92.22,nCredits=3))
#    stu.add_course(Course(title='Global History II',year=2010,level=1,numAvg=92.22,nCredits=3))
#    stu.add_course(Course(title='Chemistry',year=2010,level=1,numAvg=75.22,nCredits=3))
#    stu.add_course(Course(title='Algebra II',year=2011,level=2,numAvg=95.22,nCredits=3))
#    stu.add_course(Course(title='Geometry',year=2010,level=2,numAvg=93.22,nCredits=3))
#    stu.add_course(Course(title='Biology',year=2009,level=2,numAvg=73.22,nCredits=3))

#stu.add_exam(Exam(examType='Regents',subject='Physics',year=2012,month=6,score=95))
#stu.add_exam(Exam(examType='Regents',subject='Chemistry',year=2011,month=6,score=84))
#stu.add_exam(Exam(examType='Regents',subject='Geometry',year=2011,month=6,score=87))
#stu.add_exam(Exam(examType='Regents',subject='Geometry',year=2011,month=6,score=87))
#stu.add_exam(Exam(examType='Regents',subject='Geometry',year=2011,month=6,score=87))
#stu.add_exam(Exam(examType='Regents',subject='Geometry',year=2011,month=6,score=87))
#stu.add_exam(Exam(examType='Regents',subject='Geometry',year=2011,month=6,score=87))
#stu.add_exam(Exam(examType='Regents',subject='Geometry',year=2011,month=6,score=87))
#stu.add_exam(Exam(examType='Regents',subject='Geometry',year=2011,month=6,score=87))
#stu.add_exam(Exam(examType='Regents',subject='Geometry',year=2011,month=6,score=87))
#stu.add_exam(Exam(examType='Regents',subject='Geometry',year=2011,month=6,score=87))

reg_read = RegentsReader('data/DPRegentsData.xlsx')
reg_read.get_exams(students)

sat_read = SATReader('data/DPSATData.xlsx')
sat_read.get_exams(students)

act_read = ACTReader('data/DPACTData.xlsx')
act_read.get_exams(students)

ap_read = APReader('data/DPAPData.xlsx')
ap_read.get_exams(students)

#stu.add_exam(Exam(examType='AP',subject='Physics C: Mechanics',year=2011,month=6,score=5))
#stu.add_exam(Exam(examType='AP',subject='Physics C: Mechanics',year=2011,month=6,score=5))
#stu.add_exam(Exam(examType='AP',subject='Physics C: Mechanics',year=2011,month=6,score=5))

#stu.add_exam(Exam(examType='SAT',subject='Reading',year=2011,month=6,score=700))
#stu.add_exam(Exam(examType='SAT',subject='Mathematics',year=2011,month=6,score=740))


import subprocess
for stu in students:
    text = make_transcript(stu)
    texFile = 'tmp/'+stu.first+stu.last+'_Transcript.tex'
    newTranscript = open(texFile,'w')
    newTranscript.write(text)
    newTranscript.close()

    logFile = open('tmp/tmp.log','w')
    return_value = subprocess.call(['/usr/texbin/pdflatex','-output-directory=tmp/', texFile], shell=False, stdout=logFile, stderr=subprocess.STDOUT)
    if return_value == 0:
        print 'PDF file:',texFile.replace('tex','pdf'),'has been successfully created'
    else:
        print 'File generation failed.  Please check log file:',logFile.name

