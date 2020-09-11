#!/bin/bash

echo "starting inspircd"
nohup /usr/sbin/inspircd --runasroot --debug --nopid & > irc.log
echo "inspircd started"
service snmpd restart
service postfix restart
tail -f /dev/null
