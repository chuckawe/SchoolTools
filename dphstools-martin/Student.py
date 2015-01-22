# File: Student.py
# Author: Brian Martin
# Date: July 27, 2012
# Description: Module to hold class
# holding all information needed for
# a student's records.

import datetime

from Exam import Exam
from Section import Section

def find_by_id(students,ID):
    """Return student with a particular ID,
    if no match return None"""
    for student in students:
        if ID == student.stuID:
            return student
    return None

class Student(object):
    """Stores student data"""

    def __init__(self, **kwargs):
        self.stuID   = kwargs.get('stuID',0)
        
        self.last    = kwargs.get('last',  '')
        self.first   = kwargs.get('first', '')

        self.street  = kwargs.get('street', '')
        self.city    = kwargs.get('city',   '')
        self.state   = kwargs.get('state',  '')
        self.zipcode = kwargs.get('zipcode','')
        
        self.dob     = kwargs.get('dob','')

        self.gradYear = kwargs.get('gradYear',1999)
        self._grade = -1

        self.homeroom = kwargs.get('homeroom', '')
        self.advisor  = kwargs.get('advisor', '')
        
        # Does the student have an IEP
        self.HasIEP = kwargs.get('HasIEP',False)
        # Does the student have an 504
        self.Has504 = kwargs.get('Has504',False)
        # Is the student classified as ELL
        self.IsELL = kwargs.get('IsELL',False)
        
        # Dictionary of courses by year (As in Course objects)
        self.coursework = {}
        
        # List of Exams (As in Exam objects)
        self.exams = []
        
        # List of Behaviors (As in Behavior objects)
        self.behaviors = []
        
        # Schedule Related objects
        self.schedule = [None,None,None,None,None,None,None,None,None,None]
        self.friday_schedule = [None,None,None,None,None,None]
        self.has = {}
        self.has['act']       = False
        self.has['math']       = False
        self.has['science']    = False
        self.has['history']    = False
        self.has['literature'] = False
        self.has['writing']    = False
        self.has['korean']     = False
        self.has['elective']   = False
        self.needed = {}
        self.needed['act']       = 'None'
        self.needed['math']       = 'None'
        self.needed['science']    = 'None'
        self.needed['history']    = 'None'
        self.needed['literature'] = 'None'
        self.needed['writing']    = 'None'
        self.needed['korean']     = 'None'
        self.needed['elective']   = 'None'

    def __str__(self):
        s =  '_________________________________________'
        s += '\nStudent ID:  '    +str(self.stuID)
        s += '\nFirst Name:  '    +self.first
        s += '\nLast Name: '      +self.last
        s += '\nStreet:  '        +self.street
        s += '\nCity: '           +self.city
        s += '\nState:  '         +self.state
        s += '\nZip Code: '       +self.zipcode
        s += '\nDOB: '            +self.dob
        s += '\nGraduation Year: '+str(self.gradYear)
        s += '\nYears Attended:  '+str(len(self.coursework))
        s += '\nCourses:         '+str(len(self.get_courses()))
        s += '\nExams:         '  +str(len(self.exams))
        s += '\n_________________________________________'

        return s
    
    def print_schedule(self):
        print 'Schedule for',self.first,self.last
        for section in self.schedule:
            if section is None:
                print 'MISSING'
            else:
                print 'Period',section.period,'-',section.title

        for subject in self.needed.keys():
            if self.needed[subject] != 'None':
                print 'Need to schedule:',self.needed[subject]

        for section in self.friday_schedule:
            if section is None:
                print 'MISSING'
            else:
                print 'Friday Period',section.period,'-',section.title
    
    def reset_schedule(self):
        self.schedule = [None,None,None,None,None,None,None,None,None,None]
        self.friday_schedule = [None,None,None,None,None,None]
        self.has = {}
        self.has['act']     = False
        self.has['math']     = False
        self.has['science']  = False
        self.has['history']  = False
        self.has['literature']      = False
        self.has['writing']  = False
        self.has['korean']   = False
        self.has['elective'] = False

    def set_hs_grade(self,grade):
        
        self._grade = int(grade)

    def get_hs_grade(self):
        """Returns High School Grade
        given expected graduation year"""
   
        if self._grade != -1:
            return self._grade

        now = datetime.datetime.now()

        ToGo = self.gradYear - now.year

        if now.month > 7:
            ToGo -= 1

        self._grade = 12 - ToGo
        return self._grade

    def add_course(self,course):
        if course.year not in self.get_years():
            self.coursework[course.year] = []

        self.coursework[course.year].append(course)

    def add_exam(self,exam):
        self.exams.append(exam)

    def add_behavior(self, behavior):
        self.behaviors.append(behavior)

    def get_years(self):
        """Return list of years student at DP"""
        return sorted(self.coursework.keys())

    def get_courses(self, year=None):
        """Returns courses from a particular year.
        or if year is None, entire career."""
        if year is None:
            courses = []
            for year in self.get_years():
                courses += self.get_courses(year)
            return courses
        elif year not in self.coursework.keys():
            return []
        else:
            return self.coursework[year]

    def resolve_repeats(self):
        """Remove duplicate courses retaining instance with highest grade"""
        print "Removing the lower score of any repeated courses."
        course_dict = {}
        tmp_coursework = {}
        for course in self.get_courses():
            if course.title in course_dict.keys():
                print "Repeat course found for",self.first,self.last,course.title,course.year
            else:
                course_dict[course.title] = []
            
            course_dict[course.title].append(course)
        for course_title in course_dict.keys():
            max_course = None
            for course in course_dict[course_title]:
                if max_course == None or max_course.grade() < course.grade():
                    max_course = course

            if max_course.year not in tmp_coursework.keys():
                tmp_coursework[max_course.year] = []

            tmp_coursework[max_course.year].append(max_course)

        self.coursework = tmp_coursework
        

    def get_exams(self, examType=None):
        """Return list of exams of examType.  If
        examType == None, allexams are returned."""

        if examType is None:
            return self.exams
        else:
            filtExams = []
            for exam in self.exams:
                if exam.examType == examType:
                    filtExams.append(exam)
            
            return filtExams

    def get_highest_exam(self,examType,subject="all"):
        """Return highest exam of examType in certain subject.
           If subject is 'total' (only useful for SAT and ACT), then
           highest composite score is returned, regardless of sitting.
           If subject is 'all' return all exams removing the duplicates
           (keeping the higher of the duplicated exam)"""

        if subject=='total' and examType not in ['SAT','ACT']:
            raise ValueError('Cannot compute total for %s examType.  Must be SAT or ACT.' % (examType))
            import sys
            sys.exit(1)

        # Loop over exams finding exams of correct type
        maxExam = {}
        for exam in self.exams:
            if exam.examType == examType:
                if subject in ["total","all"] or subject == exam.subject:
                    # Keep highest exam
                    if exam.subject not in maxExam.keys() or exam.score > maxExam[exam.subject].score:
                        maxExam[exam.subject] = exam

        # Remove Writing from ACT Composite score
        if examType == 'ACT': 
            maxExam.pop('Writing',0)

        if subject == 'total':
            total = 0.0
            for exam in maxExam.values:
                total += exam.score
            return total/float(len(maxExam))
        elif subject == 'all':
            return maxExam.values()
        else:
            if subject not in maxExam.keys():
                return None
            else:
                return maxExam[subject]

    def meets_regents_diploma(self):
        """Returns boolean depending on student meeting
        regular regents dipolma requirements"""

        meets = True
        exam = self.get_highest_exam(examType='Regents',subject='Global History')
        meets &= (exam != None and exam.score>=65) 
        exam = self.get_highest_exam(examType='Regents',subject='US History')
        meets &= (exam != None and exam.score>=65) 
        exam = self.get_highest_exam(examType='Regents',subject='English')
        meets &= (exam != None and exam.score>=65) 
        
        alg = self.get_highest_exam(examType='Regents',subject='Integrated Algebra')
        geo = self.get_highest_exam(examType='Regents',subject='Geometry')
        alg2= self.get_highest_exam(examType='Regents',subject='Algebra II/Trigonometry')
        meets &= (alg != None and alg.score>=65) or \
                 (geo != None and geo.score>=65) or \
                 (alg2!= None and alg2.score>=65) 
        bio  = self.get_highest_exam(examType='Regents',subject='Living Environment')
        chem = self.get_highest_exam(examType='Regents',subject='Chemistry')
        phys = self.get_highest_exam(examType='Regents',subject='Physics')
        eart = self.get_highest_exam(examType='Regents',subject='Earth Science')
        meets &= (bio != None and bio.score>=65)  or \
                 (chem!= None and chem.score>=65) or \
                 (phys!= None and phys.score>=65) or \
                 (eart!= None and eart.score>=65) 

        return meets

    def meets_advanced_diploma(self):
        """Returns boolean depending on student meeting
        regular regents dipolma requirements"""

        meets = True
        exam = self.get_highest_exam(examType='Regents',subject='Global History')
        meets &= (exam != None and exam.score>=65) 
        exam = self.get_highest_exam(examType='Regents',subject='US History')
        meets &= (exam != None and exam.score>=65) 
        exam = self.get_highest_exam(examType='Regents',subject='English')
        meets &= (exam != None and exam.score>=65) 
        
        alg = self.get_highest_exam(examType='Regents',subject='Integrated Algebra')
        geo = self.get_highest_exam(examType='Regents',subject='Geometry')
        alg2= self.get_highest_exam(examType='Regents',subject='Algebra II/Trigonometry')
        meets &= (alg != None and alg.score>=65) and \
                 (geo != None and geo.score>=65) and \
                 (alg2!= None and alg2.score>=65) 
        bio  = self.get_highest_exam(examType='Regents',subject='Living Environment')
        chem = self.get_highest_exam(examType='Regents',subject='Chemistry')
        phys = self.get_highest_exam(examType='Regents',subject='Physics')
        eart = self.get_highest_exam(examType='Regents',subject='Earth Science')
        meets &= (bio != None and bio.score>=65)  and \
                 ((chem!= None and chem.score>=65) or \
                 (phys!= None and phys.score>=65) or \
                 (eart!= None and eart.score>=65))
        kor = self.get_highest_exam(examType='Regents',subject='Korean')
        spa = self.get_highest_exam(examType='Regents',subject='Spanish')
        fre = self.get_highest_exam(examType='Regents',subject='French')
        meets &= (kor != None and kor.score>=65) or \
                 (spa != None and spa.score>=65) or \
                 (fre != None and fre.score>=65) 
        
        return meets

    def meets_math_honors(self):
        
        alg  = self.get_highest_exam(examType='Regents',subject='Integrated Algebra')
        geo  = self.get_highest_exam(examType='Regents',subject='Geometry')
        alg2 = self.get_highest_exam(examType='Regents',subject='Algebra II/Trigonometry')
        
        if alg is None or geo is None or alg2 is None: return False
        
        return (alg.score>=85 and geo.score>=85 and alg2.score>=85)

    def meets_science_honors(self):
        
        bio  = self.get_highest_exam(examType='Regents',subject='Living Environment')
        chem = self.get_highest_exam(examType='Regents',subject='Chemistry')
        phys = self.get_highest_exam(examType='Regents',subject='Physics')
        
        if bio is None or chem is None or phys is None: return False
        
        return (bio.score>=85 and chem.score>=85 and phys.score>=85)

    def get_regents_average(self):
        """Compute average of advanced regents diploma exams only"""

        exams = []
        for reg in ['Integrated Algebra','Living Environment','Geometry','Global History','English','US History','Algebra II/Trigonometry','Korean']:
            reg_exam = self.get_highest_exam(examType='Regents',subject=reg)
            if reg_exam != None:
                exams.append(reg_exam)

        # Select higher of Physics and Chemistry
        phys = self.get_highest_exam(examType='Regents',subject='Physics')
        chem = self.get_highest_exam(examType='Regents',subject='Chemistry')
        
        if chem != None and phys == None: exams.append(chem)
        elif phys != None and chem == None: exams.append(phys)
        elif phys != None and chem != None: 
            if chem.score > phys.score:
                exams.append(chem)
            else:
                exams.append(phys)

        scores =[ e.score for e in exams ]

        return (float(sum(scores))/len(scores) if len(scores) > 0 else float(0.0))

    def get_credits(self,year=None, coreOnly=False):
        """Return credits earned for a single year.
        or if year is None, entire career."""

        credits = 0.0
        if year is None:
            for year in self.get_years():
                credits += self.get_credits(year, coreOnly=coreOnly)
        else:
            # Important: the number of credits here should be the number
            # earned.  i.e if a student failed, it should be zero.
            for course in self.coursework[year]:
                if coreOnly and not course.is_core(): continue
                credits += course.credits_earned()

        return credits

    def compute_gpa(self,weighted,year=None, coreOnly=False, use4Scale=True):
        """Computes GPA of student for a given year
        or if year is None, entire career."""

        points  = 0.0
        credits = 0.0
        now = datetime.datetime.now()
        this_year = now.year
        if now.month < 7: this_year -= 1

        if year is None:
            for year in self.get_years():
                yearCredits = self.get_credits(year, coreOnly=coreOnly)
                points  += self.compute_gpa(weighted,year,coreOnly=coreOnly, use4Scale=use4Scale)*yearCredits
                credits += yearCredits
        else:
            # Important: For GPA calculation, the number of credits for
            # the course must be used (not the number earned by the student)
            for course in self.coursework[year]:
                if coreOnly and not course.is_core(): 
                    #print 'Excluding ',course.title,' ==> not CORE'
                    continue
                #print '\t\t\t\tIncluding ',course.title,' ==> as CORE'
                if use4Scale:
                    points += course.gpa(weighted)*course.nCredits
                    #print course.title,"Grade:",course.grade(),"GPA: ",course.gpa(weighted),"Credits:",course.nCredits
                else:
                    points += course.grade()*course.nCredits 
                credits += course.nCredits
        
            #print "Year:",year,"Points: ",points,"Credits:",credits
        if credits < 0.1:
            return 0.0
        else:
            return float(points/credits)

    def remove_exam(self,examType,subject):
        """Remove single exam from record"""
        self.exams[:] = [exam for exam in self.exams if (exam.examType != examType or exam.subject != subject) ]

    def clean_exams(self):
        """Removes failing exams from record.  Works for regents only."""
        print "Removing any failed Regents Exams."
        self.exams[:] = [exam for exam in self.exams if (exam.examType != "Regents" or exam.score > 64) ]

    def clean_courses(self):
        """Removes failing courses from record."""
        print "Removing any failed courses."
        temp_coursework = {}
        for year in self.coursework.keys():
            self.coursework[year][:] = [course for course in self.coursework[year] if course.grade() >= 70 ]

