#!/bin/bash

/usr/sbin/sshd -D &
service snmpd restart
/main.sh
tail -f /dev/null
