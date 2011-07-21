Cassandra Tests
===============

##Information about the Cluster

There are three nodes in the local cluster and they are listening on IP addresses 127.0.0.1, 127.0.0.5, 127.0.010. Every time we add a node to the cluster, we must reassign tokens to all of the existing nodes. Use the cassandra_token.py script to get the appopriate tokens. That script is taken from http://www.datastax.com/docs/0.8/install/adding_nodes#adding-nodes.

##Questions/Discoveries about Cassandra

*	Connection Pools
	*	    When we create the connection pool, we only need to add one server to the server_list parameter. Cassandra will use it's own internal communication to figure out the rest of the nodes in the cluster.
	*	    Can't direct a write to a specific node.

*	Eventual Consistency
	*	    Strongly consistent: R + W > ReplicationFactor
	*	    As stated [here](http://cassandra-user-incubator-apache-org.3065146.n2.nabble.com/meaning-of-eventual-consistency-in-Cassandra-td5885445.html), eventualy consistency depends on our choice of consistency level. If we read from multiple nodes, as in QUORUM or ALL, then the value with the most recent timestamp is returned.
	*	    Cassandra uses Read Repair--if whenever Cassandra reads from replicas of the same key and the most recent timestamped value is different from the other values, the newest version will be sent to all the out-of-date replicas.

