#!/bin/bash

/usr/sbin/sshd -D &
nohup /usr/sbin/inspircd --runasroot --debug --nopid & > irc.log
sleep 5
/setup_db.sh
tail -f /dev/null
