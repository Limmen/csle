#!/bin/bash

service named start
service ntp restart
/usr/sbin/sshd -D &
tail -f /dev/null
