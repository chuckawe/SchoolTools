# File: Course.py
# Author: Brian Martin
# Date: July 27, 2012
# Description: Module for class
# that stores all information
# relavant to a course

class Course(object):
    """Stores complete set of information defining a course that a student took"""

    levelStr = ['Regular','College Prep','Honors','AP']

    def __init__(self, **kwargs):
        # full title of course including AP, Honors, etc
        self.title = kwargs.get('title','')
        # first year of academic year (Ex 2011 refers to 2011-2012)
        self.year = kwargs.get('year',1999)
        # 0=Regular, 1=CollegePrep, 2=Honors, 3=AP
        self.level = kwargs.get('level',-1)
        # course grade as percent
        self.numAvg = kwargs.get('numAvg',0.0)
        # did the student pass the course over the summer
        self.PassSummer = kwargs.get('PassSummer',False)
        # Credits that the course is worth
        self.nCredits = kwargs.get('nCredits',0)
        # If True, course is from current academic year
        self.current = kwargs.get('CurrentCourse',False)
        # If is current, this holds trimester grades
        self.term_grades = {} # Expected keys: F1, F2, F3

    def __str__(self):
        s =  '_________________________________________'
        s += '\nCourse Title:  '+self.title
        s += '\nAcademic Year: '+str(self.year)+'-'+str(self.year+1)
        s += '\nCourse Level:  '+self.levelStr[self.level]
        s += '\nNumerical Avg: '+str(self.numAvg)
        s += '\nCourse Grade:  '+str(self.grade())
        s += '\nUnweighted GPA points:    '+str(self.gpa())
        s += '\nWeighted GPA points:    '+str(self.gpa(weighted=True))
        s += '\nCredits:       '+str(self.nCredits)
        s += '\n_________________________________________'

        return s

    def grade(self):
        """return course grade corrected for summer school participation and minimum grade policy"""
        if round(self.numAvg,0) >= 70:
            return round(self.numAvg,0)
        elif self.PassSummer:
            return 70
        elif round(self.numAvg,0) >= 55 and not self.PassSummer:
            return round(self.numAvg,0)
        else:
            return 55

    def gpa(self,weighted=False):
        """return student GPA"""
        if self.level < 0: 
            print 'Invalid Student Level:',self.level
            import sys
            sys.exit
        
        avg_bins = [
        99.5,  92.5,  89.5,  86.5,  82.5,  79.5,  76.5,  72.5,  69.5]
        weighted_pts   = [
        4.3,    4.0,    3.75,    3.5,    3.25,    3.0,    2.75,    2.5,    2.25]
        unweighted_pts   = [
        4.3,    4.0,    3.75,    3.5,    3.25,    3.0,    2.75,    2.5,    2.25]

        gpa = 0.0
        for i in range(len(avg_bins)):
            if self.grade() >= avg_bins[i]:
                if weighted:
                    gpa = weighted_pts[i]
                else:
                    gpa = unweighted_pts[i]
                break

        if not weighted: return gpa

        # Non-Core class
        if self.level == 0:
            return gpa
        # College-Prep Core Class
        elif self.level == 1:
            return gpa
        # Honors Class
        elif self.level == 2:
            return gpa*1.125
        # AP / College Class
        elif self.level == 3:
            return gpa*1.250

    def credits_earned(self):
        """Return the number of credits for a course only if a students passed"""

        if self.grade() >= 69.5:
            return self.nCredits
        else:
            return 0.0

    def is_core(self):
        """True if course is considered a Core Academic Course"""
        #core_stems = (
        #              'Algebra','Geometry','Precalculus','Calculus',
        #              'Biology','Chemistry','Physics','Living Environment','Global Environment','Scientific Literacy',
        #              'History','Economics',
        #              'Literature','Language','Writing','AP','Sem',
        #              'Korean',
        #              )
        #core = False
        #for stem in core_stems:
        #    if stem in self.title:
        #        core = True
        
        return self.level>0

