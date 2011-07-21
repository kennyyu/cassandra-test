#!/usr/bin/env python

import pycassa
from pycassa.system_manager import *

# name of the keyspace we will use for this grades simulation
from constants import GRADES_KEYSPACE as GRADES_KEYSPACE

# connect to the local cluster, there are three nodes in the cluster:
#          127.0.0.1
#          127.0.0.5
#          127.0.0.10
# this operation will block until all the nodes in the cluster have accepted the modification
sys = SystemManager('127.0.0.1:9160')

print 'Cluster Name: ' + sys.describe_cluster_name()
print 'Keyspaces in cluster before drop: ' + str(sys.list_keyspaces())

# drop this keyspace
if GRADES_KEYSPACE in sys.list_keyspaces():
    sys.drop_keyspace(GRADES_KEYSPACE)

# print information about cluster and keyspace
print 'Keyspaces in cluster after drop: ' + str(sys.list_keyspaces())

# close the connection to cassandra
sys.close()

