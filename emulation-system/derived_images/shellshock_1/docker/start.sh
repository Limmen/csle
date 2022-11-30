#!/bin/bash

chmod 755 /run/sshd
chown root /run/sshd
/usr/sbin/sshd -D &
/main.sh &
tail -f /dev/null
