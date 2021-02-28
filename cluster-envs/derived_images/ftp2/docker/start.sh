#!/bin/bash

#./setup_firewall.sh
service pycr-firewall start
nohup /usr/sbin/vsftpd &
/usr/sbin/sshd -D &
/etc/init.d/inetutils-inetd restart
#/cockroach-v20.1.8.linux-amd64/cockroach start-single-node --insecure --listen-addr=0.0.0.0:26257 --http-addr=0.0.0.0:8080 --background &
#nohup /usr/local/kafka/bin/zookeeper-server-start.sh /usr/local/kafka/config/zookeeper.properties & > zookeeper.log
#nohup /usr/local/kafka/bin/kafka-server-start.sh /usr/local/kafka/config/server.properties & > kafka.log
tail -f /dev/null
