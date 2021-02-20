#!/bin/bash

/usr/sbin/sshd -D &
nohup /usr/sbin/inspircd --runasroot --debug --nopid & > irc.log
nohup /main.sh &
sleep 5
/setup_db.sh
tail -f /dev/null
