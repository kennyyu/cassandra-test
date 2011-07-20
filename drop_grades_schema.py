#!/usr/bin/env python

import pycassa
from pycassa.system_manager import *

# name of the keyspace we will use for this grades simulation
from create_grades_schema import GRADES_KEYSPACE as GRADES_KEYSPACE

# connect to the local cluster (1 node only) on localhost:9160
# this operation will block until all the nodes in the cluster have accepted the modification
sys = SystemManager('127.0.0.1:9160')

# drop this keyspace
if GRADES_KEYSPACE in sys.list_keyspaces():
    sys.drop_keyspace(GRADES_KEYSPACE)

# close the connection to cassandra
sys.close()

