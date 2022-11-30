#!/bin/bash

/usr/sbin/sshd -D &
/main.sh &
tail -f /dev/null
