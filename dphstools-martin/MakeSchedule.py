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
        if section == None: continue
        pd +=1
        if pd == 10: break
        #if pd == 10 and student.get_hs_grade() > 10:
        #    break
        #if pd == 9 and student.get_hs_grade() > 11:
        #    break
        if pd == 1:
            theTEX += '%s & %s & %s & %s \\\\\n' % ('AM', 'AM Homeroom', '-', student.homeroom)
        #if section is None: 
            # Hack for 12th grade schedule
            #theTEX += '%i & %s & %s & %s \\\\\n' % (pd, 'See Homeroom Teacher', '', '')
            #theTEX += '%i & %s & %s & %s \\\\\n' % (pd, 'See Period 9 Daily Schedule', '', '')
        #else:
        theTEX += '%i & %s & %s & %s \\\\\n' % (section.period, section.title, section.teacher, section.room)

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
    
    # Handle Electives Block in 9/10
    if 'Elective Block 10' in theTEX:
        theTEX = theTEX.replace('Elective Block 10 & - & 0','\\textit{refer to elective table} & - & -')
        elec_dict = {}
        elec_dict['Mon-Tues'] = ['Health','AGetting','302']
        elec_dict['Wed-Thur'] = ['Physical Education','JDaCorta','St. Phillips Gym']
        text = build_elective_table(student,elec_dict)
        theTEX = theTEX.replace('%ELECTIVES',text)

    if 'SETTS-10' in theTEX:
        theTEX = theTEX.replace('SETTS-10 & MKelley & 325B','\\textit{refer to elective table} & - & -')
        elec_dict = {}
        elec_dict['Mon-Tues'] = ['SETTS-10','MKelley','325B']
        elec_dict['Wed-Thur'] = ['Physical Education','JDaCorta','St. Phillips Gym']
        text = build_elective_table(student,elec_dict)
        theTEX = theTEX.replace('%ELECTIVES',text)
    
    if 'Elective Block 9' in theTEX:
        theTEX = theTEX.replace('Elective Block 9 & - & 0','\\textit{refer to elective table} & - & -')
        elec_dict = {}
        elec_dict['Mon-Tues'] = ['Physical Education','JDaCorta','St. Phillips Gym']
        elec_dict['Wed-Thur'] = ['Communications','AGetting','302']
        text = build_elective_table(student,elec_dict)
        theTEX = theTEX.replace('%ELECTIVES',text)
    
    if 'SETTS-9' in theTEX:
        theTEX = theTEX.replace('SETTS-10 & EDiMauro & 325A','\\textit{refer to elective table} & - & -')
        elec_dict = {}
        elec_dict['Mon-Tues'] = ['Physical Education','JDaCorta','St. Phillips Gym']
        elec_dict['Wed-Thur'] = ['SETTS-9','EDiMauro','325A']
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

docsFile = 'DPCHS_Schedule_2014-2015'
outDir = os.path.expanduser("~")+'/Desktop/'+args.dir
print 'Schedules will be saved to',outDir
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
    texFile = outDir+'/'+stu.homeroom+'_'+stu.last+stu.first+'_'+str(stu.stuID)+'_'+str(stu.get_hs_grade())+'_Schedule.tex'
    #texFile = outDir+'/'+stu.last+stu.first+'_'+str(stu.get_hs_grade())+'_'+stu.homeroom+'_Schedule.tex'
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

