#!/bin/bash

/var/ossec/bin/ossec-control start
/usr/sbin/sshd -D &
service rsyslog restart
tail -f /dev/null

