#!/usr/bin/python

import subprocess,os,os.path
from os.path import expanduser
import argparse
from Student import *
from Section import *
from Readers import ReadMaster


def build_sched_table(student,friday):
    """Return tex markup of a course table for a given year"""

    theTEX = r""""""

    sched = []
    if friday:
        sched = student.friday_schedule
    else:
        sched = student.schedule
    
    pd = 0
    for section in sched:
        pd +=1
        if pd == 10 and student.get_hs_grade() > 10:
            break
        if pd == 9 and student.get_hs_grade() > 11:
            break
        if pd == 1:
            theTEX += '%s & %s & %s & %s \\\\\n' % ('AM', 'AM Homeroom', '-', student.homeroom)
        #if section is None: 
            # Hack for 12th grade schedule
            #theTEX += '%i & %s & %s & %s \\\\\n' % (pd, 'See Homeroom Teacher', '', '')
            #theTEX += '%i & %s & %s & %s \\\\\n' % (pd, 'See Period 9 Daily Schedule', '', '')
        #else:
        theTEX += '%i & %s & %s & %s \\\\\n' % (section.period, section.title, section.teacher, section.room)
    if student.get_hs_grade() < 12:
        theTEX += '%s & %s & %s & %s \\\\\n' % ('PM', 'PM Homeroom', '-', student.homeroom)


    return theTEX

def build_elective_table(student,ed):

    theTEX = r"""
\begin{textblock}{5}(3.5,8.0)
\Large {\bf Electives Table}\\
\begin{tabular}{l l l l}
\bf{Day} & \bf{Course} & \bf{Teacher} & \bf{Room} \\
\hline
"""
    pd = 0
    for d in sorted(ed.keys()):
        theTEX += '%s & %s & %s & %s \\\\\n' % (d, ed[d][0], ed[d][1], ed[d][2])

    theTEX += """
\end{tabular}
\end{textblock}
"""
    return theTEX

def make_schedule(student):

    texFile = open('TemplateSchedule/TemplateSchedule.tex', 'r')
    theTEX = texFile.read()
    texFile.close()

    print 'Generating schedule for', student.first,student.last
    

    # Student Info
    theTEX = theTEX.replace('FIRSTNAME',student.first)
    theTEX = theTEX.replace('LASTNAME',student.last)
    theTEX = theTEX.replace('STUID',str(student.stuID))
    theTEX = theTEX.replace('GRADE',str(student.get_hs_grade()))
    theTEX = theTEX.replace('HOMEROOM',student.homeroom)
    theTEX = theTEX.replace('ADVISOR',student.advisor)
    
    text = build_sched_table(student,False)
    theTEX = theTEX.replace('%THECOURSES',text)
    
    # Handle CollegeReadiness Block in 9/10
    if 'College Readiness 201' in theTEX:
        theTEX = theTEX.replace('College Readiness 201 & Getting & 321','\\textit{refer to elective table} & - & -')
        elec_dict = {}
        elec_dict['Mon-Tues'] = ['College Readiness 201','Getting','321']
        elec_dict['Wed-Thur'] = ['Physical Education','Jackson','Gym']
        text = build_elective_table(student,elec_dict)
        theTEX = theTEX.replace('%ELECTIVES',text)
    
    if 'College Readiness 101' in theTEX:
        theTEX = theTEX.replace('College Readiness 101 & Getting & None','\\textit{refer to elective table} & - & -')
        elec_dict = {}
        elec_dict['Mon-Tues'] = ['Theatre','Kowalski','Auditorium']
        elec_dict['Wed-Thur'] = ['College Readiness 101','Getting','321']
        text = build_elective_table(student,elec_dict)
        theTEX = theTEX.replace('%ELECTIVES',text)
    
    if 'Flex Period A' in theTEX:
        theTEX = theTEX.replace('Flex Period A &  & ','\\textit{refer to Electives table} & - & -')
        elec_dict = {}
        elec_dict['5th-Mon/Wed']   = ['College Readiness 301','Ramos','331']
        elec_dict['5th-Tues/Thur'] = ['Study Hall','Ross','321']
        elec_dict['6th-Mon/Wed']   = ['SAT Prep: Critical Reading/Writing','-','329']
        elec_dict['6th-Tues/Thur'] = ['SAT Math','Dedhia','329']
        text = build_elective_table(student,elec_dict)
        theTEX = theTEX.replace('%ELECTIVES',text)
    
    if 'Flex Period B' in theTEX:
        theTEX = theTEX.replace('Flex Period B &  & ','\\textit{refer to Electives table} & - & -')
        elec_dict = {}
        elec_dict['5th-Mon/Wed']   = ['College Readiness 301','Ramos','331']
        elec_dict['5th-Tues/Thur'] = ['Study Hall','Ross','321']
        elec_dict['6th-Mon/Wed']   = ['SAT Math','Dedhia','329']
        elec_dict['6th-Tues/Thur'] = ['SAT Prep: Critical Reading/Writing','-','329']
        text = build_elective_table(student,elec_dict)
        theTEX = theTEX.replace('%ELECTIVES',text)
    
    if 'Flex Period C' in theTEX:
        theTEX = theTEX.replace('Flex Period C &  & ','\\textit{refer to Electives table} & - & -')
        elec_dict = {}
        elec_dict['5th-Mon/Wed']   = ['Study Hall','DeLoache','321']
        elec_dict['5th-Tues/Thur'] = ['College Readiness 301','Ramos','331']
        elec_dict['6th-Mon/Wed']   = ['SAT Prep: Critical Reading/Writing','-','325A']
        elec_dict['6th-Tues/Thur'] = ['SAT Math','Lance','325B']
        text = build_elective_table(student,elec_dict)
        theTEX = theTEX.replace('%ELECTIVES',text)
    
    if 'Flex Period D' in theTEX:
        theTEX = theTEX.replace('Flex Period D &  & ','\\textit{refer to Electives table} & - & -')
        elec_dict = {}
        elec_dict['5th-Mon/Wed']   = ['Study Hall','DeLoache','321']
        elec_dict['5th-Tues/Thur'] = ['College Readiness 301','Ramos','331']
        elec_dict['6th-Mon/Wed']   = ['SAT Math','Lance','325B']
        elec_dict['6th-Tues/Thur'] = ['SAT Prep: Critical Reading/Writing','-','325A']
        text = build_elective_table(student,elec_dict)
        theTEX = theTEX.replace('%ELECTIVES',text)
    
    if 'Flex Period E' in theTEX:
        theTEX = theTEX.replace('Flex Period E &  & ','\\textit{refer to Electives table} & - & -')
        elec_dict = {}
        elec_dict['5th-Mon/Wed']   = ['SAT Prep: Critical Reading/Writing','-','329']
        elec_dict['5th-Tues/Thur'] = ['SAT Math','Jospitre','329']
        elec_dict['6th-Mon/Wed']   = ['College Readiness 301','Ramos','331']
        elec_dict['6th-Tues/Thur'] = ['Study Hall','Park','321']
        text = build_elective_table(student,elec_dict)
        theTEX = theTEX.replace('%ELECTIVES',text)
    
    if 'Flex Period F' in theTEX:
        theTEX = theTEX.replace('Flex Period F &  & ','\\textit{refer to Electives table} & - & -')
        elec_dict = {}
        elec_dict['5th-Mon/Wed']   = ['SAT Math','Jospitre','329']
        elec_dict['5th-Tues/Thur'] = ['SAT Prep: Critical Reading/Writing','-','329']
        elec_dict['6th-Mon/Wed']   = ['College Readiness 301','Ramos','331']
        elec_dict['6th-Tues/Thur'] = ['Study Hall','Park','321']
        text = build_elective_table(student,elec_dict)
        theTEX = theTEX.replace('%ELECTIVES',text)
    
    if 'Flex Period G' in theTEX:
        theTEX = theTEX.replace('Flex Period G &  & ','\\textit{refer to Electives table} & - & -')
        elec_dict = {}
        elec_dict['5th-Mon/Wed']   = ['SAT Prep: Critical Reading/Writing','-','325A']
        elec_dict['5th-Tues/Thur'] = ['SAT Math','Romano','325B']
        elec_dict['6th-Mon/Wed']   = ['Study Hall','Park','321']
        elec_dict['6th-Tues/Thur'] = ['College Readiness 301','Ramos','331']
        text = build_elective_table(student,elec_dict)
        theTEX = theTEX.replace('%ELECTIVES',text)
    
    if 'Flex Period H' in theTEX:
        theTEX = theTEX.replace('Flex Period H &  & ','\\textit{refer to Electives table} & - & -')
        elec_dict = {}
        elec_dict['5th-Mon/Wed']   = ['SAT Math','Romano','325B']
        elec_dict['5th-Tues/Thur'] = ['SAT Prep: Critical Reading/Writing','-','325A']
        elec_dict['6th-Mon/Wed']   = ['Study Hall','Park','321']
        elec_dict['6th-Tues/Thur'] = ['College Readiness 301','Ramos','331']
        text = build_elective_table(student,elec_dict)
        theTEX = theTEX.replace('%ELECTIVES',text)
    
    text = build_sched_table(student,True)
    theTEX = theTEX.replace('%FRICOURSES',text)

    return theTEX

parser = argparse.ArgumentParser(description="""
Democracy Prep Schedule Maker\r
This program reads Democracy Prep master schedule and prepares an individual 
schedule for each student.
""")
parser.add_argument('studentIDs',nargs='*',type=int,
                   help='List of Student IDs for which a schedule should be generated.  LEAVE BLANK FOR ALL STUDENTS.')
parser.add_argument('--grade',type=int, dest='grade_filt',
                   default=-1, help='Select students by grade level.')
parser.add_argument('--dir',type=str, dest='dir',
                   default='tmp', help='Output directory for schedule files.')
args = parser.parse_args()

print args.studentIDs

splash = """
######################################
#                                    #
#  DEMOCRACY PREP SCHEDULE MAKER     #
#    If any problems, please contact #
#    bmartin@democracyprep.org       #
#                                    #
######################################
"""

print splash

docsFile = 'DPCHS_Schedule_2013-2014'
outDir = os.path.expanduser("~")+'/Desktop/'+args.dir
print 'Transcripts will be saved to',outDir
if not os.path.isdir(outDir):
    os.makedirs(outDir)




students = []
sections = []
ReadMaster(docsFile,students,sections)

#print len(students)
#print args.studentIDs

if len(args.studentIDs)>0:
    students = [student for student in students if int(student.stuID) in args.studentIDs]

#print students
#new_students = []
#for student in students:
#    for id in 
#    if int(student.stuID) == 11 or int(student.stuID == 12):
#        new_students.append(student)


for stu in students:
    if args.grade_filt != -1 and float(stu.get_hs_grade()) != float(args.grade_filt):
        continue
    text = make_schedule(stu)
    texFile = outDir+'/'+stu.last+stu.first+'_'+str(stu.get_hs_grade())+'_'+stu.homeroom+'_Schedule.tex'
    texFile = texFile.replace(" ", "")
    newSchedule = open(texFile,'w')
    newSchedule.write(text)
    newSchedule.close()
    
    logFile = open(outDir+'/tmp.log','w')
    return_value = subprocess.call(['/usr/texbin/pdflatex','-output-directory='+outDir+'/', texFile], shell=False, stdout=logFile, stderr=subprocess.STDOUT)
    if return_value == 0:
        print 'PDF file:',texFile.replace('tex','pdf'),'has been successfully created'
    else:
        print 'File generation failed.  Please check log file:',logFile.name

