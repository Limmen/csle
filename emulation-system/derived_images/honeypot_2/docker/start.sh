#!/bin/bash

nohup /usr/sbin/inspircd --runasroot --debug --nopid & > irc.log
/usr/sbin/sshd -D &
service snmpd restart
/var/ossec/bin/ossec-control start
service postfix restart
service postgresql restart
service ntp restart
service rsyslog restart
tail -f /dev/null
