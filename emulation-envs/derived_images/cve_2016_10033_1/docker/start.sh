#!/bin/bash

/usr/sbin/sshd -D &
service rsyslog restart
/main.sh
tail -f /dev/null
