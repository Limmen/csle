#!/bin/bash

/usr/sbin/sshd -D &
service snmpd restart
service rsyslog restart
/main.sh
tail -f /dev/null
