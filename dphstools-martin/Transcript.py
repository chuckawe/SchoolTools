# File: Transcript.py
# Author: Brian Martin
# Date: July 27, 2012
# Description: Module for preparing transcript

def build_course_table(student, year):
    """Return tex markup of a course table for a given year"""
    is_current = student.get_courses(year)[0].current

    # FIXME
    is_current = False

    if is_current:
        theTEX = r"""
\begin{table}
\caption[]{School Year %i-%i\footnotemark[1]}
\centering
\begin{tabularx}{\textwidth}{ m{5.0cm} c c }
\toprule
{\bf Subject} & \multicolumn{1}{c}{\bf Num} & {\bf Credits} \\
{\bf Area}& \multicolumn{1}{c}{\bf Avg} & {\bf Earned} \\
\midrule
""" % (year, year+1)
    else:
        theTEX = r"""
\begin{table}
\caption{School Year %i-%i}
\centering
\begin{tabularx}{\textwidth}{ m{5.0cm}  c c }
\toprule
{\bf Subject} & \multicolumn{1}{c}{\bf Num} & {\bf Credits} \\
{\bf Area}& \multicolumn{1}{c}{\bf Avg} & {\bf Earned} \\
\midrule
""" % (year, year+1)
        

    for course in student.get_courses(year):
        #if not is_current and course.credits_earned() == 0.0: continue
        if 'SAT Prep' in course.title: continue
        if 'College Readiness' in course.title: continue

        # Protect against ampersand character in latex
        title = course.title.replace('&','\&')

		# Add (Hon) to honors courses
        if course.level == 2:
			title += " (Hon)"


        # Shorten Longer titles
        if title == "AP English Language and Composition":
            title = "AP English Lang \& Comp"
        if title == "AP English Literature and Composition":
            title = "AP English Lit \& Comp"
        if title == "Korean Literature \& Culture":
            title = "Korean Lit \& Culture"
        if title == "Algebra II/Trigonometry":
            title = "Algebra II/Trig"
        if title == "Global Environment (SUNY-ESF)":
            title = "Glob Environment (SUNY-ESF)"

        theTEX += '%s & %.0f & %.1f \\\\\n' % (title, round(course.grade(),0), round(course.credits_earned(),1))
    
    if not is_current:
        theTEX += r"""\midrule
Year Average & %.1f &  Total %.1f \\
""" % (round(student.compute_gpa(False,year,use4Scale=False),1),round(student.get_credits(year),1))

    theTEX += r"""
\bottomrule
\end{tabularx}
\end{table}
"""
    if is_current:
        theTEX += r'* Grades for this academic year indicate current standing and are not final.'
    

    # Add footnote to elective
    if 'Elective' in theTEX:
        theTEX = theTEX.replace('Elective',r'Elective\footnotemark[2]')
    return theTEX

def build_course_singletable(student):
    """Return tex markup of a course table for all courses at DPCHS"""
    theTEX = r"""
\begin{table}
\centering
\begin{tabularx}{\textwidth}{ m{5.2cm} c c c }
\toprule
{\bf Subject} & {\bf Academic} & {\bf Numerical}  & {\bf Credits} \\
{\bf Area}    & {\bf Year}     & {\bf Average}            & {\bf Earned}   \\
\midrule
"""
        

    for course in student.get_courses():
        if 'SAT Prep' in course.title: continue
        if 'College Readiness' in course.title: continue

        # Protect against ampersand character in latex
        title = course.title.replace('&','\&')
		

		# Add (Hon) to honors courses
        if course.level == 2:
			title += " (Hon)"

        # Shorten Longer titles
        if title == "AP English Language and Composition":
            title = "AP English Lang \& Comp"
        if title == "AP English Literature and Composition":
            title = "AP English Lit \& Comp"
        if title == "Global Environment (SUNY-ESF)":
            title = "Glob Environment (SUNY-ESF)"
        
        theTEX += '%s & %i-%i & %.0f & %.1f \\\\[5pt]\n' % (title, course.year, course.year+1, round(course.grade(),0), round(course.credits_earned(),1))
    
#    if not is_current:
#        theTEX += r"""\midrule
# & Year GPA %.2f &  Total %.1f \\
#""" % (round(student.compute_gpa(True,year,useCurrent=True),2),round(student.get_credits(year),1))

    theTEX += r"""
\bottomrule
\end{tabularx}
\end{table}
"""
    return theTEX



def build_sum_table(student,college):
    """Return tex markup of summary table."""
    theTEX = ""

#    theTEX += r"""
#\large
#\begin{table}
#\begin{tabular}{ l c  }
#{\bf Weighted GPA}: & %.2f \\
#{\bf Unweighted GPA}: & %.2f \\
#{\bf Total Credits Earned}: & %.1f \\
#\end{tabular}
#\end{table}
#""" % (student.compute_gpa(weighted=True,coreOnly=False), student.compute_gpa(weighted=False,coreOnly=False),student.get_credits())
    
    if college:
        theTEX += r"""
\large
\begin{table}
\begin{tabular}{ l c  }
{\bf Cumulative GPA}: & %.2f \\
{\bf Total Credits Earned}: & %.1f \\
\end{tabular}
\end{table}
""" % (student.compute_gpa(weighted=True,coreOnly=False, use4Scale=True),student.get_credits())
    else:
        theTEX += r"""
\large
\begin{table}
\begin{tabular}{ l c  }
{\bf Cumulative Average}: & %.1f \\
{\bf Total Credits Earned}: & %.1f \\
\end{tabular}
\end{table}
""" % (student.compute_gpa(weighted=True,coreOnly=False, use4Scale=False),student.get_credits())


    if college and student.get_hs_grade() > 12:
        if student.get_hs_grade() >= 12:#FIXME
            diploma = ''
            if student.meets_advanced_diploma():
                diploma = 'Advanced Regents'
            elif student.meets_regents_diploma():
                diploma= 'Regents' 
    
            theTEX += r"""
\large
\begin{table}
\begin{tabular}{ l l  }
{\bf Diploma}: & %s \\
    """ % diploma
    
            avg = student.get_regents_average()
            if avg > 89.50000: 
                theTEX += r""" & with Honors Distinction \\"""
    
            if student.meets_science_honors():
                theTEX += r""" & with Science Honors \\"""
            
            if student.meets_math_honors():
                theTEX += r""" & with Mathematics Honors \\"""
    
            if student.get_hs_grade() == 13:
                theTEX += r""" & Earned 06/24/2014 \\"""
            elif student.get_hs_grade() == 14:
                theTEX += r""" & Earned 06/24/2013 \\"""
    
            theTEX += r"""\end{tabular}
\end{table}
"""

    return theTEX

def build_exam_table(exams,title,nTables,nExams,singletable=False):
    """Return tex markup of exams"""

    if singletable:
        x_coord = 10
        y_coord = 2.5
        width = 4.7
    else:
        x_coord = 0.5+nTables*4
        y_coord = 11.5
        width = 3.7
    if 'SAT' in title or 'ACT' in title:
        width = 3.3

    theTEX = r"""
\begin{textblock}{%.2f}(%.2f,%.2f)
\begin{table}
\caption{%s}
\centering
\begin{tabularx}{\textwidth}{ X  c }
\toprule
{\bf Subject} & {\bf Score} \\
\midrule
""" % (width,x_coord,y_coord,title)

    for exam in exams:
        if singletable: theTEX += '%s & %i \\\\[5pt] \n' % (exam.subject, exam.score)
        else: theTEX += '%s & %i \\\\ \n' % (exam.subject, exam.score)
        if not singletable: theTEX = theTEX.replace("Algebra II/Trigonometry","Algebra II/Trig")
        nExams += 1

    theTEX += r"""\bottomrule
\end{tabularx}
\end{table}
\end{textblock}

"""

    return theTEX

def make_transcript(student,school,college,official,singletable):

    if singletable:
        texFile = open('TemplateTranscript/TemplateTranscript_singletable.tex', 'r')
        #texFile = open('TemplateTranscript/TemplateTranscript_singletableFilled.tex', 'r')
    else:
        texFile = open('TemplateTranscript/TemplateTranscript.tex', 'r')
    theTEX = texFile.read()
    texFile.close()

    print 'Generating transcript for', student.first,student.last
    
    theTEX = theTEX.replace('LOGO','\includegraphics[scale=1.3]{'+school+'}')

    if school == 'DPCHS':
        school_address = r"""222 W. 134th St. New York, NY 10030 \\
Phone: (212) 281-3061 \hspace{0.5cm} Fax: (212) 281-3064\\"""
    elif school == 'DPHHS':
        school_address = r"""212 W. 120th St. New York, NY 10027 \\
Phone: (212) 932-7791 \hspace{0.5cm} Fax: (212) 666-3706\\"""


    theTEX = theTEX.replace('SCHOOLADDRESS',school_address)

    # Student Info
    theTEX = theTEX.replace('FIRSTNAME',student.first)
    theTEX = theTEX.replace('LASTNAME',student.last)
    theTEX = theTEX.replace('STUID',str(student.stuID))
    if student.get_hs_grade() > 12:
        theTEX = theTEX.replace('GRADE','Graduate')
    else:
        theTEX = theTEX.replace('GRADE',str(student.get_hs_grade()))
    #theTEX = theTEX.replace('STREET',student.street)
    #theTEX = theTEX.replace('CITY',student.city)
    #theTEX = theTEX.replace('STATE',student.state)
    #theTEX = theTEX.replace('ZIP',student.zipcode)
    theTEX = theTEX.replace('DATEOFBIRTH',student.dob)

    # Fix special character problem
    theTEX = theTEX.replace('#','\#')

    # Coursework
    if singletable:
        text = build_course_singletable(student)
        theTEX = theTEX.replace('%COURSEWORKALL',text)
    else:
        i=0
        hasElective = False
        for year in reversed(student.get_years()):
            text = build_course_table(student, year)
            if 'Elective' in text: hasElective = True
            theTEX = theTEX.replace('%COURSEWORKYEAR'+str(i),text)
            i += 1
  
        # Add elective footnote
        if hasElective:
            theTEX = theTEX.replace('%ELECTIVEFOOTNOTE',r'\footnotetext[2]{Elective classes include: Art, Theatre, and Physical Education.}')

    text = build_sum_table(student,college=college)
    theTEX = theTEX.replace('%COURSEWORKSUMMARY',text)

    # Exams
    nTables = 0
    nExams  = 0
    text = ''
    
    exams = student.get_highest_exam('Regents',subject='all')
    if len(exams) > 0 :
        text += build_exam_table(exams,'NYS Regents',nTables,nExams,singletable)
        nExams  += len(exams)
        nTables += 1

    exams = student.get_highest_exam('AP')
    # Only report AP exams greater than 2
    exams_to_print = [exam for exam in exams if exam.score > 2]
    if len(exams_to_print) > 0 :
        text += build_exam_table(exams_to_print,'Advanced Placement',nTables,nExams)
        nExams  += len(exams_to_print)
        nTables += 1
    
    exams = student.get_highest_exam('SAT')
    if len(exams) > 0 :
        text += build_exam_table(exams,'SAT',nTables,nExams)
        nExams  += len(exams)
        nTables += 1
    
    exams = student.get_highest_exam('ACT')
    if len(exams) > 0 :
        text += build_exam_table(exams,'ACT',nTables,nExams)
        nExams  += len(exams)
        nTables += 1
    
    if text == '':
        text += """\\begin{textblock}{3.5}(12.0,3.5)
\large
No Examinations on record.
\end{textblock}"""
    theTEX = theTEX.replace('%EXAMSBYTYPE',text)
    
    
    # Set Background image
    if college:
        theTEX = theTEX.replace('%WATERMARK',"""
% Official Transcript "Watermark"
\\begin{textblock}{10}(0.15,3.0)
\includegraphics[scale=0.80]{DPPS_Shield}
\end{textblock}
""")      
    elif official:
        theTEX = theTEX.replace('%WATERMARK',"""
% Official Transcript "Watermark"
\\begin{textblock}{40}(0.5,5.0)
\includegraphics[scale=0.8]{OffTrans}
\end{textblock}
""")      
    else:
        theTEX = theTEX.replace('%WATERMARK',"""
% Unofficial Transcript "Watermark"
\\begin{textblock}{40}(0.5,5.0)
\includegraphics[scale=0.8]{UnOffTrans}
\end{textblock}
""")     

    return theTEX



