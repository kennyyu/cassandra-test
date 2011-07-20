"""
Load this file with an interactive python interpretive session with python -i grades.py
This will execute all the definitions and assignments, and will give you the namespace
of the variables in this file.
"""

import pycassa
from create_grades_schema import GRADES_KEYSPACE as GRADES_KEYSPACE
from create_grades_schema import QUIZ_GRADES_COLUMN_FAMILY as QUIZ_GRADES_COLUMN_FAMILY
from create_grades_schema import STUDENT_GRADES_COLUMN_FAMILY as STUDENT_GRADES_COLUMN_FAMILY
from create_grades_schema import QUIZ_QUESTIONS_COLUMN_FAMILY as QUIZ_QUESTIONS_COLUMN_FAMILY

#GRADES_KEYSPACE = 'Test_Grades'
#QUIZ_GRADES_COLUMN_FAMILY = 'Quiz_Grades'
#STUDENT_GRADES_COLUMN_FAMILY = 'Student_Grades'
#QUIZ_QUESTIONS_COLUMN_FAMILY = 'Quiz_Questions'

# open a pool of connections to the cluster
pool = pycassa.ConnectionPool(keyspace=GRADES_KEYSPACE, 
                              server_list=['127.0.0.1:9160'])

# grab the column families
quiz_grades_cf = pycassa.ColumnFamily(pool, QUIZ_GRADES_COLUMN_FAMILY)
student_grades_cf = pycassa.ColumnFamily(pool, STUDENT_GRADES_COLUMN_FAMILY)
quiz_questions_cf = pycassa.ColumnFamily(pool, QUIZ_QUESTIONS_COLUMN_FAMILY)

PASSING_SCORE = 65
MAX_SCORE = 100

class Student:
    def __init__(self, name):
        self.name = name

    def add_quiz(self, quiz, quiz_score=0, questions_wrong=[]):
        """
        Args:
           - quiz: Quiz Object
           - quiz_score: int
           - questions_wrong: list of strings
        """
        quiz_grades_cf.insert(key=quiz.name,
                              columns={quiz_score : {self.name : str(questions_wrong)}})
        student_grades_cf.insert(key=self.name,
                                 columns={quiz.name : {'grade' : quiz_score,
                                                       'questions' : str(questions_wrong)}})
        # probably better to use a batch_insert
        for question in questions_wrong:
            quiz_questions_cf.add(key=quiz.name, column=question, value=1)

        if quiz_score < PASSING_SCORE:
            quiz_questions_cf.add(key=quiz.name, column='num_failed', value=1)
            
    def get_grade(self, quiz):
        data = student_grades_cf.get(self.name, super_column=quiz.name, columns=['grade'])
        return data['grade']

    def get_all_grades(self):
        """
        Returns a dict mapping quiz names -> grade
        """
        data = student_grades_cf.get(self.name)
        grades = {}
        for quiz in data:
            del data[quiz]['questions'] # superfluous information
            grades[quiz] = data[quiz]['grade']
        return grades

    def get_questions_wrong(self, quiz):
        # eval converts the string back to a list
        data = student_grades_cf.get(self.name, super_column=quiz.name, columns=['questions'])
        return eval(data['questions'])

class Quiz:
    def __init__(self, name):
        self.name = name

    def get_grades(self):
        """
        Returns a dict mapping grade -> students who received those grades
        """
        data = quiz_grades_cf.get(key=self.name)
        grades = {}
        for grade in data:
            for student in data[grade]:
                if grade in grades:
                    grades[grade].append(student)
                else:
                    grades[grade] = [student]
        return grades

    def get_students_with_grade_geq_than(self, score):
        """
        Returns a list of students with grade >= score on this quiz
        """
        data = quiz_grades_cf.get(key=self.name, 
                                  column_start=score, 
                                  column_finish=MAX_SCORE)
        students = []
        for grade in data:
            for student in data[grade]:
                students.append(student)
        return students

    def get_num_students_with_grade_geq_than(self, score):
        """
        Returns number of students with grade >= score on this quiz
        """
        return quiz_grades_cf.get_count(key=self.name,
                                        column_start=score,
                                        column_finish=MAX_SCORE)

    def get_num_failed(self):
        data = quiz_questions_cf.get(key=self.name, columns=['num_failed'])
        return data['num_failed']

    def get_question_frequency(self):
        """
        We can't efficiently given a quiz and a question, return WHO answered it incorrectly.
        Returns a dict mapping question -> frequency answered incorrectly.
        """
        data = quiz_questions_cf.get(key=self.name)
        if 'num_failed' in data:
            del data['num_failed']
        return dict(data)

    @staticmethod
    def get_quizzes_with_geq_students_failing(num):
        """
        Returns a dict mapping quizes -> number of students that failed that quiz

        WARNING: Cassandra currently does not support secondary indexes on counter columns nor
        secondary indexes on subcolumns of super columns. Thus, this method will not work.
        """
        fail_expr = pycassa.index.create_index_expression('num_failed', num, pycassa.index.GTE)
        clause = pycassa.index.create_index_clause([fail_expr])
        quizzes = {}
        for quiz, num_failed in quiz_questions_cf.get_indexed_slices(clause):
            quizzes[quiz] = num_failed
        return quizzes

s1 = Student('Kenny')
s2 = Student('Jack')
q1 = Quiz('q1')
q2 = Quiz('q2')

s1.add_quiz(q1, quiz_score=80, questions_wrong=['1','2a'])
s1.add_quiz(q2, quiz_score=40, questions_wrong=['3','7','10b'])
s2.add_quiz(q1, quiz_score=30, questions_wrong=['1','9'])
s2.add_quiz(q2, quiz_score=20, questions_wrong=['3','7','9'])
