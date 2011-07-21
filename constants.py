#!/usr/bin/env python

GRADES_KEYSPACE = 'Test_Grades'
QUIZ_GRADES_COLUMN_FAMILY = 'Quiz_Grades'
STUDENT_GRADES_COLUMN_FAMILY = 'Student_Grades'
QUIZ_QUESTIONS_COLUMN_FAMILY = 'Quiz_Questions'

if __name__ == '__main__':
    print GRADES_KEYSPACE
    print QUIZ_GRADES_COLUMN_FAMILY
    print STUDENT_GRADES_COLUMN_FAMILY
    print QUIZ_QUESTIONS_COLUMN_FAMILY
