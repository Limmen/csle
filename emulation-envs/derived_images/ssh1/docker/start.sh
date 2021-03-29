#!/bin/bash

service named start &
/usr/sbin/sshd -D &
#/apache-cassandra-2.1.22/bin/cassandra &
swipl -s /erl_pengine/prolog/server.pl -g "server(80)." > pl.txt
tail -f /dev/null
