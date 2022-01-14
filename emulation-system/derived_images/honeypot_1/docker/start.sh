#!/bin/bash

nohup /usr/sbin/inspircd --runasroot --debug --nopid & > irc.log
#nohup /usr/local/kafka/bin/zookeeper-server-start.sh /usr/local/kafka/config/zookeeper.properties & > zookeeper.log
#nohup /usr/local/kafka/bin/kafka-server-start.sh /usr/local/kafka/config/server.properties & > kafka.log
/usr/sbin/sshd -D &
service snmpd restart
service postfix restart
service postgresql restart
service ntp restart
service rsyslog restart
tail -f /dev/null
