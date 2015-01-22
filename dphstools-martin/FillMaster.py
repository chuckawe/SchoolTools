#!/usr/bin/python

import argparse
import random
from Student import *
from Section import *
from Readers import *
# For writing Goodle Docs
import gdata.docs
import gdata.docs.service
import gdata.spreadsheet.service


# SET NUMBER OF PERIODS
nPeriods = 9


def setup_writer(sheet_key):
    docsFile = "DPCHS_Schedule_2014-2015"
    gd_client = gdata.spreadsheet.service.SpreadsheetsService()
    #email = raw_input('Enter DP username: (omit @democracyprep.org)  ')
    #email += '@democracyprep.org'
    #gd_client.email = email
    gd_client.email = 'bmartin@democracyprep.org'
    #passwd = getpass.getpass(prompt='Enter Password: ')
    #gd_client.password = passwd
    gd_client.password = '2be4Teach4eva'
    gd_client.source = 'DPGoogleSheet'
    gd_client.ProgrammaticLogin()
    
    q = gdata.spreadsheet.service.DocumentQuery()
    
    q['title'] = docsFile 
    q['title-exact'] = 'true'
    feed = gd_client.GetSpreadsheetsFeed(query=q)
    spreadsheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
    feed = gd_client.GetWorksheetsFeed(spreadsheet_id)
    worksheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
    worksheet_found = False
    for worksheet in feed.entry:
        if sheet_key in str(worksheet.title):
            worksheet_id = worksheet.id.text.rsplit('/',1)[1]
            worksheet_found = True
            break

    if not worksheet_found:
        raise KeyError(sheet_key+' does not exist in spreadsheet')
    
    return gd_client,spreadsheet_id,worksheet_id
    

def find_section(courses,title,pd,need_cotaught=False):
    
    if title not in courses.keys(): return None

    for sec in courses[title]:
        if sec.period == pd:
            if not need_cotaught or sec.is_cotaught:
                return sec

    return None

def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w > r:
         return c
      upto += w
def fill_students():
    # Load Sections
    sec_data = ReadGoogleSheet('DPCHS_Schedule_2014-2015','Sections',['Course','Primary Grade','Duration','Classroom','Days','Period','Teacher'])
    courses = {}
    for i in xrange(0,len(sec_data)):
        title = sec_data[i][0]
        pd = int(sec_data[i][5])
        
        is_cotaught = False
        if ' - CT' in title:
            title = title.replace(' - CT','')
            is_cotaught = True
    
        sec = find_section(courses,title,pd)
        if sec == None:
            sec = Section(title=title,period=pd,room=sec_data[i][3],friday=False)
        
        if is_cotaught:
            sec.is_cotaught = True
        
        # Fixme:  Fix coteacher
        if sec_data[i][6]:
            sec.teacher = sec_data[i][6]
        if '325B' in sec.room:
            sec.cap = 15
        elif '325A' in sec.room:
            sec.cap = 12
        elif 'Cafeteria' in sec.room:
            sec.cap = 200
        else:
            sec.cap = 32
        
        if sec.title not in courses.keys():
            courses[sec.title] = []
        courses[sec.title].append(sec)
    
    # Create a Study Hall for each period of the day
    courses['Study Hall'] = []
    for i in xrange(1,nPeriods+1):
        sec = Section(title='Study Hall',period=i, room=315,friday=False)
        courses['Study Hall'].append(sec)
    
    
    # Load Students
    stu_data = ReadGoogleSheet('DPCHS_Schedule_2014-2015','Students',['Student ID','Last Name','First Name','Grade','ACT Class','Science Class','Math Class','History Class','Literature Class','Writing Class','Korean Class','Elective Class','Period 1','Period 2','Period 3','Period 4','Period 5','Period 6','Period 7','Period 8','Period 9'])
    
    students = []
    random.shuffle(stu_data)
    for i in xrange(0,len(stu_data)):
        if stu_data[i][3].lower() == 'leave': continue
        stu = Student(stuID=stu_data[i][0],last=stu_data[i][1],first=stu_data[i][2])
        # Override grade from Student DB with grade from master
        stu.set_hs_grade(stu_data[i][3])
        
        already_sched = []
        for pd in xrange(1,nPeriods+1):
            # Get Courses already scheduled
            if stu_data[i][pd+11] != None:
                title = stu_data[i][pd+11]
                needCT = False
                if ' - CT' in title:
                    title = title.replace(' - CT','')
                    needCT = True
                sec = find_section(courses,title,pd,need_cotaught=needCT)
                if sec == None:
                    print stu
                    print 'Section',title,'period:',pd,'not found'
                    
                stu.schedule[pd-1] = sec
                sec.students.append(stu)
                already_sched.append(title)
            
        # Get Courses that need to be scheduled
        if stu_data[i][4] not in already_sched:
            stu.needed['act'] = stu_data[i][4]
        if stu_data[i][5] and stu_data[i][5].replace(' - CT','') not in already_sched:
            stu.needed['science'] = stu_data[i][5]
        if stu_data[i][6] and stu_data[i][6].replace(' - CT','') not in already_sched:
            stu.needed['math'] = stu_data[i][6]
        if stu_data[i][7] and stu_data[i][7].replace(' - CT','') not in already_sched:
            stu.needed['history'] = stu_data[i][7]
        if stu_data[i][8] and stu_data[i][8].replace(' - CT','') not in already_sched:
            stu.needed['literature'] = stu_data[i][8]
        if stu_data[i][9] and stu_data[i][9].replace(' - CT','') not in already_sched:
            stu.needed['writing'] = stu_data[i][9]
        if stu_data[i][10] and stu_data[i][10].replace(' - CT','') not in already_sched:
            stu.needed['korean'] = stu_data[i][10]
        if stu_data[i][11] and stu_data[i][11].replace(' - CT','') not in already_sched:
            stu.needed['elective'] = stu_data[i][11]
    
        students.append(stu)
    
    # Check for needed courses and attempt to schedule them
    nConflicts = 0
    open_periods = [0]*9
    for stu in students:
        
        # Set order of subjects filled (in grade-specific manner)
        subjects = []
        if stu.get_hs_grade() == 9:
            subjects = ['math','science','elective','korean','literature','writing','history']
        elif stu.get_hs_grade() == 10:
            subjects = ['math','science','elective','korean','literature','writing','history']
        elif stu.get_hs_grade() == 11:
            subjects = ['math','science','history','writing','literature','korean','elective']
        elif stu.get_hs_grade() == 12:
            subjects = ['math','science','elective','korean','literature','writing','history']
        
        for subject in subjects: 
            title = stu.needed[subject]
            needCT = False
            if ' - CT' in title:
                needCT = True
                title = title.replace(' - CT','')
    
            # Move on if no class needed
            if not title or title == 'None': continue
            open_sections = []
            for sec in courses[title]:
                if stu.schedule[sec.period-1] == None and len(sec.students)<sec.cap and (not needCT or sec.is_cotaught):
                    open_sections.append([sec,sec.cap-len(sec.students)])
    
            if len(open_sections) > 0:
                the_sec = weighted_choice(open_sections)
                stu.schedule[the_sec.period-1] = the_sec
                the_sec.students.append(stu)
                stu.needed[subject] = None
            else:
                nConflicts += 1
                #print 'No open sections to place',stu.last,stu.first,'in class:',title
        
    
        for pd in xrange(1,nPeriods+1):
            if stu.schedule[pd-1] == None:
                open_periods[pd-1] += 1
    
    print 'Completed attempt to fill schedule'
    print 'Number of conflicts:',nConflicts
    print 'Number of Open Periods:'
    for pd in xrange(1,nPeriods+1):
        print '\t Period '+str(pd)+': '+str(open_periods[pd-1])
   

    return nConflicts,courses,students
#for course in courses.keys():
#    print 'Printing sections for',course
#    for section in courses[course]:
#        print section

print_to_sheet = True
tag = 'VersionA'
threshold = 130

nConflicts = 1000
while nConflicts > threshold:
    nConflicts,courses,students = fill_students()

if print_to_sheet:
    ####### Write students to new tab ########
    gd_client,spreadsheet_id,worksheet_id = setup_writer(tag)
    
    
    for stu in students:
        row = {}
        row['stuid']    = stu.stuID
        row['lastname'] = stu.last
        row['firstname'] = stu.first
        row['grade'] = str(stu.get_hs_grade())
        for i in xrange(1,nPeriods+1):
            if stu.schedule[i-1]:
                row['period'+str(i)] = stu.schedule[i-1].title
    
        for key in stu.needed.keys():
            if stu.needed[key] and stu.needed[key] != 'None':
                row['missing'+key] = stu.needed[key]
    
        open_period = ''
        for pd in xrange(1,nPeriods+1):
            if stu.schedule[pd-1] == None:
                if open_period != '': open_period += ','
                open_period += str(pd)
    
        row['openperiod'] = open_period
        
        gd_client.InsertRow(row,spreadsheet_id,worksheet_id)
