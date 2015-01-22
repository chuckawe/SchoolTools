#!/usr/bin/python

from Student import *
from Course import *
from Exam import *
from Transcript import *
from Readers import *
import sys,subprocess,os,os.path
import argparse

parser = argparse.ArgumentParser(description="""
Democracy Prep Transcript Maker\r
This program reads Democracy Prep student records and generates a pdf file
for each student for whom a transcript is requested.
""")
parser.add_argument('studentIDs',nargs='*',type=int,
                   help='List of Student IDs for which a transcript should be generated.  LEAVE BLANK FOR ALL STUDENTS.')
parser.add_argument('--grade',type=int, dest='grade_filt',
                   default=-1, help='Select students by grade level.')
parser.add_argument('--school',type=str, dest='school',
                   default='DPCHS', help='DP High School for which to create transcripts.')
parser.add_argument('--dir',type=str, dest='dir',
                   default='tmp', help='Output directory for transcript files.')
parser.add_argument('--official', dest='official', action='store_true',
                   default=False, help='Mark document as an official transcript.')
parser.add_argument('--college', dest='college', action='store_true',
                   default=False, help='Create transcripts for colleges.')
parser.add_argument('--transfer', dest='transfer', action='store_true',
                   default=False, help='Create transcript for transfer or program')
parser.add_argument('--clean', dest='clean', action='store_true',
                   default=False, help='Remove failing grades in failing exams.')
parser.add_argument('--singletable', dest='singletable', action='store_true',
                   default=False, help='Place all courses in a single table.')
parser.add_argument('--UseCurrent', dest='UseCurrent', action='store_true',
                   default=False, help='Switch off reporting of current course grades.')
parser.add_argument('--UseSAT', dest='UseSAT', action='store_true',
                   default=False, help='Switch off reporting of SAT exam results.')
parser.add_argument('--UseACT', dest='UseACT', action='store_true',
                   default=False, help='Switch off reporting of ACT exam results.')
parser.add_argument('--NoRegents', dest='UseRegents', action='store_false',
                   default=True, help='Switch off reporting of Regents exam results.')
parser.add_argument('--UseAP', dest='UseAP', action='store_true',
                   default=False, help='Switch off reporting of AP exam results.')
parser.add_argument('--TexOnly', dest='TexOnly', action='store_true',
                   default=False, help='Switch off generating PDF.')
parser.add_argument('--year', type=int,dest='year', help='Enrollment year (specified as leading year)')

args = parser.parse_args()

splash = """
######################################
#                                    #
#  DEMOCRACY PREP TRANSCRIPT MAKER   #
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
load_all_students = True
for ID in args.studentIDs:
    students.append(Student(stuID=ID))
    load_all_students = False

data_read = StudentDataReader('data/'+args.school+'_StudentData.xlsx')
while data_read.next_sheet():
    data_read.get_data(students,year=args.year, get_all=load_all_students)
    print "Found",len(students),"thus far."
    

if args.grade_filt != -1:
        students = [student for student in students if student.get_hs_grade() == args.grade_filt]

course_read = CourseReader('data/'+args.school+'_CourseData.xlsx')
course_read.get_courses(students)

if args.college and args.transfer:
    print 'Choose --college or --transfer, not both.'
    sys.exit(1)
elif not args.college and not args.transfer:
    print 'Choose --college or --transfer.'
    sys.exit(1)
elif args.college and not args.transfer:
    print 'Producing transcripts for college admission'
    args.clean = True
    args.singletable = True
elif not args.college and args.transfer:
    print 'Producing transcripts for college admission'

if args.UseCurrent:
    print 'Including Current Course grades'
    cur_read = CourseCurrentReader('data/'+args.school+'CourseCurrent.xlsx')
    cur_read.get_courses(students,final_term='F3')  # SET THIS TO TAKE THE DESIRED TERM
else:
    print 'Excluding Current Course grades'

if args.UseRegents:
    print 'Including Regents exam results'
    reg_read = RegentsReader('data/'+args.school+'_RegentsData.xlsx')
    while reg_read.next_sheet():
        reg_read.get_exams(students)
else:
    print 'Excluding Regents exam results'

if args.UseSAT:
    print 'Including SAT exam results'
    sat_read = SATReader('data/'+args.school+'_SATData.xlsx')
    sat_read.get_exams(students)
else:
    print 'Excluding SAT exam results'

if args.UseACT:
    print 'Including ACT exam results'
    act_read = ACTReader('data/'+args.school+'_ACTData.xlsx')
    act_read.get_exams(students)
else:
    print 'Excluding ACT exam results'

if args.UseAP:
    print 'Including AP exam results'
    ap_read = APReader('data/'+args.school+'_APData.xlsx')
    ap_read.get_exams(students)
else:
    print 'Excluding AP exam results'


outDir = os.path.expanduser("~")+'/Desktop/'+args.dir
if not os.path.isdir(outDir):
    os.makedirs(outDir)

for stu in students:
    # Remove repeated courses
    if args.college or args.clean:
        stu.resolve_repeats()

    # Remove Failed Grades and Exams
    if args.college or args.clean:
        stu.clean_exams()
        stu.clean_courses()

    if args.college:
        stu.remove_exam("Regents","Mathematics A")
        stu.remove_exam("Regents","Earth Science")
        

    # Build the Transcript
    text = make_transcript(stu, school=args.school,college=args.college, official=args.official, singletable=args.singletable)

    if args.college:
        texFile = outDir+'/'+stu.last+stu.first+'_'+str(stu.stuID)+'_CollegeTranscript.tex'
    elif args.official:
        texFile = outDir+'/'+stu.last+stu.first+'_'+str(stu.stuID)+'_OfficialTranscript.tex'
    else:
        texFile = outDir+'/'+stu.last+stu.first+'_'+str(stu.stuID)+'_UnofficialTranscript.tex'
    
    # Write LATEX markup into file
    print "Saving Tex output as:",texFile
    newTranscript = open(texFile,'w')
    newTranscript.write(text)
    newTranscript.close()
    
    logFile = open(outDir+'/tmp.log','w')
    if not args.TexOnly:
        return_value = subprocess.call(['/usr/texbin/pdflatex','-output-directory='+outDir+'/', texFile], shell=False,cwd=os.getcwd(), stdout=logFile, stderr=subprocess.STDOUT)
        if return_value == 0:
            print 'PDF file:',texFile.replace('tex','pdf'),'has been successfully created'
        else:
            print 'File generation failed.  Please check log file:',logFile.name

