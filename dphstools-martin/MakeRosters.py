#!/usr/bin/python

import subprocess,os,os.path
from os.path import expanduser
import argparse
from Student import *
from Section import *
from Readers import ReadMaster


def build_roster_table(section):
    """Return tex markup of a course table for a given year"""

    theTEX = r""""""
    

    #theTEX += 'Student ID & Last Name & First Name &   \\\\\n'
    for student in section.students:
        theTEX += '%s & %s & %s & %s \\\\\n \\hline' % (student.stuID, student.last, student.first, '')


    return theTEX


def make_roster(section):

    texFile = open('TemplateSchedule/TemplateRoster.tex', 'r')
    theTEX = texFile.read()
    texFile.close()

    if len(section.students) == 0:
        return ""
    print 'Generating roster for', section.title,section.period
    

    # Student Info
    theTEX = theTEX.replace('COURSENAME',section.title)
    theTEX = theTEX.replace('PERIOD',str(section.period))
    theTEX = theTEX.replace('ROOM',section.room)
    theTEX = theTEX.replace('TEACHER',section.teacher)
    if section.is_friday:
        theTEX.replace('DAY','Friday')
    else:
        theTEX.replace('DAY','Mon-Thur')

    text = build_roster_table(section)
    theTEX = theTEX.replace('%THEROSTER',text)
     

    return theTEX

parser = argparse.ArgumentParser(description="""
Democracy Prep Roster Maker\r
This program reads Democracy Prep master schedule and prepares individual 
rosters for each section.
""")
parser.add_argument('--dir',type=str, dest='dir',
                   default='tmp', help='Output directory for schedule files.')
args = parser.parse_args()


splash = """
######################################
#                                    #
#  DEMOCRACY PREP ROSTER MAKER       #
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


for sec in sections:
    text = make_roster(sec)
    if text == '': continue
    title = sec.title
    title = title.replace('/','-')
    if sec.is_friday:
        texFile = outDir+'/'+title+'_Pd'+str(sec.period)+'_FridayRoster.tex'
    else:
        texFile = outDir+'/'+title+'_Pd'+str(sec.period)+'_Mon-ThurRoster.tex'
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

