#!/bin/bash

#./setup_firewall.sh
service pycr-firewall start
nohup /usr/sbin/inspircd --runasroot --debug --nopid & > irc.log
nohup /usr/local/kafka/bin/zookeeper-server-start.sh /usr/local/kafka/config/zookeeper.properties & > zookeeper.log
nohup /usr/local/kafka/bin/kafka-server-start.sh /usr/local/kafka/config/server.properties & > kafka.log
service snmpd restart
service postfix restart
service postgresql restart
service ntp restart
tail -f /dev/null
