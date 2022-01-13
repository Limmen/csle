#!/bin/bash

/usr/sbin/sshd -D &
service rsyslog restart
tail -f /dev/null

