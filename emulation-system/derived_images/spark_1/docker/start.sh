#!/bin/bash

RUN ./spark-3.3.2-bin-hadoop3/sbin/start-master.sh
sleep 5
RUN ./spark-3.3.2-bin-hadoop3/sbin/start-worker.sh spark://localhost:7077 -m 2G -c 1
/usr/sbin/sshd -D &
tail -f /dev/null
