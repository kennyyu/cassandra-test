#!/usr/bin/env python

from grades import Student, Quiz

s1 = Student('Kenny')
s2 = Student('Jack')
q1 = Quiz('q1')
q2 = Quiz('q2')

s1.add_quiz(q1, quiz_score=80, questions_wrong=['1','2a'])
s1.add_quiz(q2, quiz_score=40, questions_wrong=['3','7','10b'])
s2.add_quiz(q1, quiz_score=30, questions_wrong=['1','9'])
s2.add_quiz(q2, quiz_score=20, questions_wrong=['3','7','9'])

students = [s1, s2]
quizzes = [q1, q2]

print 'STUDENTS'
for s in students:
    print s.name
    print "\tGrades: " + str(s.get_all_grades())
    for q in quizzes:
        print "\t\t" + str(q.name) + ": " + str(s.get_grade(q))
        print "\t\t Questions wrong on " + str(q.name) + ": " + str(s.get_questions_wrong(q))

print '\n'
print 'QUIZZES'
for q in quizzes:
    print q.name
    print "\tGrades: " + str(q.get_grades())
    print "\tNum failed: " + str(q.get_num_failed())
    print "\tQuestion frequency: " + str(q.get_question_frequency())
    print "\tNum students with grade > 65: " + str(q.get_num_students_with_grade_geq_than(65))
    print "\t\tstudents: " + str(q.get_students_with_grade_geq_than(65))
