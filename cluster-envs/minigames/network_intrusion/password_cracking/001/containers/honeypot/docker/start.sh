#!/bin/bash

nohup /usr/sbin/inspircd --runasroot --debug --nopid & > irc.log
service snmpd restart
service postfix restart
service postgresql restart
tail -f /dev/null
