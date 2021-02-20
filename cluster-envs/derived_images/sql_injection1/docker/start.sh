#!/bin/bash

/usr/sbin/sshd -D &
#nohup /usr/sbin/inspircd --runasroot --debug --nopid & > irc.log
/main.sh
tail -f /dev/null
