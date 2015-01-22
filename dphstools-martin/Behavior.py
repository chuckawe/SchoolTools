# File: Behavior.py
# Author: Brian Martin
# Date: July 14, 2014
# Description: Module to hold behaviors

class Behavior(object):
    """Simple class to hold student behaviors"""
    def __init__(self, behaviorType, date, student, teacher=''):
        self.allowedTypes = ['Demerit','AutoDetention','SendOut','Uniform','LateSchool','LateClass','Unprepared']
        if behaviorType not in self.allowedTypes:
            raise ValueError('%s not a valid behaviorType.  Must be one of ['% behaviorType+', '.join(self.allowedTypes)+']')
            import sys
            sys.exit(1)

        self.behaviorType = behaviorType
        self.date         = date
        self.student      = student
        self.teacher      = teacher

