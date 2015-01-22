

class Section(object):
    def __init__(self, **kwargs):
        self.students = []
        self.title    = kwargs.get('title',   '')
        self.cap      = kwargs.get('cap',     32)
        self.subject  = kwargs.get('subject', '')
        self.teacher  = kwargs.get('teacher', '')
        self.coteacher  = kwargs.get('coteacher', '')
        self.period   = kwargs.get('period',   0)
        self.room     = kwargs.get('room',    '')
        self.is_friday = kwargs.get('friday',    False)
        self.is_cotaught = kwargs.get('cotaught',    False)
        self.course  = kwargs.get('course',    None)
        #self.full_teacher  = kwargs.get('full_teacher', '')
        #self.credits   = kwargs.get('credits',   0)
        #self.friday_period   = kwargs.get('friday_period',   0)
        #self.friday_room     = kwargs.get('friday_room',    '')
        #self.friday_students = []

    def reset(self):
        self.students = []
        
    def __str__(self):
        s =  '_________________________________________'
        if self.is_friday:
            s+=  '\n****Friday Course****'
        s += '\nCourse Title:  '  +self.title
        s += '\nTeacher:  '       +self.teacher
        s += '\nCoTeacher:  '       +self.coteacher
        s += '\nPeriod: '         +str(self.period)
        s += '\nRoom:  '          +self.room
        s += '\nCapacity: '       +str(self.cap)
        s += '\nEnrolled:  '      +str(len(self.students))
        if self.is_cotaught:
            s+=  '\n****ICT Course****'
        s += '\n_________________________________________'

        return s
