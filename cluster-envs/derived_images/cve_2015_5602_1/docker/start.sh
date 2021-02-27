#!/bin/bash

/usr/sbin/sshd -D &
/apache-cassandra-2.1.22/bin/cassandra &
tail -f /dev/null
