# File: Exam.py
# Author: Brian Martin
# Date: July 29, 2012
# Description: Module to hold class
# holding all information relevant 
# to a student having taken an exam


class Exam(object):
    """Simple class to hold exam results"""
    def __init__(self, examType, subject, month, year, score):
        self.allowedTypes = ['Regents','AP','SAT','SAT2','ACT']
        if examType not in self.allowedTypes:
            raise ValueError('%s not a valid examType.  Must be one of ['+', '.join(self.allowedTypes)+']' % (examType))
            import sys
            sys.exit(1)

        self.examType = examType
        self.subject = subject # reading, math, Physics, etc
        self.month = month # 1-12
        self.year = year # ex 2012
        self.score = score
