#!/bin/bash

/usr/sbin/sshd -D &
service rsyslog restart
service snmpd restart
/main.sh
tail -f /dev/null
