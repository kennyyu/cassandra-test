#!/usr/bin/env python

import pycassa
from pycassa.system_manager import *

# name of the keyspace we will use for this grades simulation
GRADES_KEYSPACE = 'Test_Grades'

# total number of copies of all the data in this keyspace on different nodes. We only have one node.
REPLICATION_FACTOR = 1

# connect to the local cluster (1 node only) on localhost:9160
# this operation will block until all the nodes in the cluster have accepted the modification
sys = SystemManager('127.0.0.1:9160')

# create the keyspace if it does not already exist
if not GRADES_KEYSPACE in sys.list_keyspaces():
    # for cassandra 0.8, need to put replication_factor inside strategy_options dict
    # SIMPLE_STRATEGY: the replicated nodes are next to each other on the ring
    sys.create_keyspace(GRADES_KEYSPACE, replication_factor=None, replication_strategy=SIMPLE_STRATEGY,
                        strategy_options={'replication_factor' : str(REPLICATION_FACTOR)})

# print information about cluster and keyspace
print 'Cluster Name: ' + sys.describe_cluster_name()
print 'Keyspaces in cluster: ' + str(sys.list_keyspaces())
print 'Ring description of keyspace: ' + str(sys.describe_ring(GRADES_KEYSPACE))
print 'GRADES_KEYSPACE properties: ' + str(sys.get_keyspace_properties(GRADES_KEYSPACE))

# create super column family schema

# We create a super column family where keys will be quiz names that map to super columns
# that are the grades received on those quizes. Each of these quizes map to columns which
# are student names, and the values are the questions the student answered incorrectly on
# the quiz. This will allow us to support easily these queries:
#
#  * for quiz Q, get students with grades >= #           (using column comparison on the super columns)
#  * get all scores and their frequencies for a quiz     (using count() on the number of sub columns for a grade)
#
# Column Family: Quiz_Grades
# Keys: quiz names (string) (key_validation_class: ASCII type)
# Supercolumns: Grades (int) (comparator: int type)
# Columns: Students (string) (comparator: ASCII type)
# Values: Questions wrong (string) (comparator: ASCII type)
QUIZ_GRADES_COLUMN_FAMILY = 'Quiz_Grades'

if not QUIZ_GRADES_COLUMN_FAMILY in sys.get_keyspace_column_families(GRADES_KEYSPACE):
    sys.create_column_family(GRADES_KEYSPACE, QUIZ_GRADES_COLUMN_FAMILY, 
                             super=True, 
                             key_validation_class='AsciiType',
                             comparator_type='IntegerType',
                             subcomparator_type='AsciiType',
                             default_validation_class='AsciiType')

# We create a super column family where keys will be student names that map to super columns
# that are quiz names. Each of these quiz names map to two columns, grade and questions which
# represent the student's grade and questions for that quiz. This allows us to support easily
# these queries:
#
#  * for student S, and for a quiz Q, get the student's grade and questions answered incorrectly
#  * what are student S's scores on all quizes?
#
# Column Family: Student_Grades
# Keys: student names (string) (key_validation_class: ASCII type)
# Supercolumns: quiz names (string) (comparator_type: ASCII type)
# Columns: grade and questions (string)
# Values: (grade, score (int)) (questions, comma separated list of question numbers (string))
STUDENT_GRADES_COLUMN_FAMILY = 'Student_Grades'

if not STUDENT_GRADES_COLUMN_FAMILY in sys.get_keyspace_column_families(GRADES_KEYSPACE):
    sys.create_column_family(GRADES_KEYSPACE, STUDENT_GRADES_COLUMN_FAMILY, 
                             super=True, 
                             key_validation_class='AsciiType')
    sys.alter_column(GRADES_KEYSPACE, STUDENT_GRADES_COLUMN_FAMILY, 'grade', INT_TYPE)

# We create a standard column family where keys will be quiz names that map to columns that will
# be question numbers. Each of these question numbers will have a counter for their frequency
# answered incorrectly. This allows us to support easily these queries:
#
#  * for quiz Q, which questions answered incorrectly most frequently?      (using a counter)
#  * for which quizes Q, did more than n people fail?                       (secondary index)
#
# Column Family: Quiz_Questions
# Keys: quiz names (string)
# Columns: questions (string), num_failed (secondary index, string)
# Values: frequency (int, counter)
QUIZ_QUESTIONS_COLUMN_FAMILY = 'Quiz_Questions'

if not QUIZ_QUESTIONS_COLUMN_FAMILY in sys.get_keyspace_column_families(GRADES_KEYSPACE):
    sys.create_column_family(GRADES_KEYSPACE, QUIZ_QUESTIONS_COLUMN_FAMILY, 
                             key_validation_class='AsciiType',
                             comparator_type='AsciiType',
                             default_validation_class='CounterColumnType')
    sys.create_index(GRADES_KEYSPACE, QUIZ_QUESTIONS_COLUMN_FAMILY, 
                     column='num_failed', value_type='CounterColumnType')


print 'Column Families: ' + str(sys.get_keyspace_column_families(GRADES_KEYSPACE))

# close the connection to cassandra
sys.close()

