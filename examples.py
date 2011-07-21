#!/usr/bin/env python

from grades import Student, Quiz

s1 = Student('Kenny')
s2 = Student('Jack')
s3 = Student('Kate')
s4 = Student('Locke')
s5 = Student('John')
s6 = Student('David')
s7 = Student('James')
s8 = Student('Juliet')

q1 = Quiz('q1')
q2 = Quiz('q2')

s1.add_quiz(q1, quiz_score=80, questions_wrong=['1','2a'])
s1.add_quiz(q2, quiz_score=40, questions_wrong=['3','7','10b'])
s2.add_quiz(q1, quiz_score=30, questions_wrong=['1','9'])
s2.add_quiz(q2, quiz_score=20, questions_wrong=['3','7','9'])
s3.add_quiz(q1, quiz_score=35, questions_wrong=['2','8b'])
s3.add_quiz(q2, quiz_score=100, questions_wrong=['3','7','9'])
s4.add_quiz(q1, quiz_score=65, questions_wrong=['2','7'])
s4.add_quiz(q2, quiz_score=70, questions_wrong=['2','8a','9'])
s5.add_quiz(q1, quiz_score=82, questions_wrong=['1','9', '2', '3', '4', '5', '6'])
s5.add_quiz(q2, quiz_score=14, questions_wrong=['3','7','9','8','1'])
s6.add_quiz(q1, quiz_score=100, questions_wrong=[])
s6.add_quiz(q2, quiz_score=100, questions_wrong=[])
s7.add_quiz(q1, quiz_score=65, questions_wrong=['1','9','7','2'])
s7.add_quiz(q2, quiz_score=65, questions_wrong=['4','5','6'])
s8.add_quiz(q1, quiz_score=0, questions_wrong=['1','2','3','4','5','6','7','8','9'])
s8.add_quiz(q2, quiz_score=0, questions_wrong=['1','2','3','4','5','6','7','8a','8b','9','10a','10b'])

students = [s1, s2, s3, s4, s5, s6, s7, s8]
quizzes = [q1, q2]

print 'STUDENTS'
for s in students:
    print s.name
    print "\tGrades: " + str(s.get_all_grades())
    for q in quizzes:
        print "\t\t" + str(q.name) + ": " + str(s.get_grade(q))
        print "\t\t\tQuestions wrong on " + str(q.name) + ": " + str(s.get_questions_wrong(q))

print 'QUIZZES'
for q in quizzes:
    print q.name
    print "\tGrades: " + str(q.get_grades())
    print "\tNum failed: " + str(q.get_num_failed())
    print "\tQuestion frequency: " + str(q.get_question_frequency())
    print "\tNum students with grade >= 65: " + str(q.get_num_students_with_grade_geq_than(65))
    print "\t\tstudents: " + str(q.get_students_with_grade_geq_than(65))
