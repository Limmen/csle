#!/bin/bash

service named start
/usr/sbin/sshd -D &
swipl -s /erl_pengine/prolog/server.pl -g "server(8888)." > pl.txt
#tail -f /dev/null
