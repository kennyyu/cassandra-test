#!/usr/bin/env python

# taken from http://www.datastax.com/docs/0.8/install/adding_nodes#adding-nodes
# every time we add a new node to the cluster, we must reassign tokens to all
# the existing nodes in the cluster.

import sys
if (len(sys.argv) > 1):
        num=int(sys.argv[1])
else:
        num=int(raw_input("How many nodes are in your cluster? "))
for i in range(0, num):
        print 'node %d: %d' % (i, (i*(2**127)/num))
