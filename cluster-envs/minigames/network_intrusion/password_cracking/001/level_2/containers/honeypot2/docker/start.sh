#!/bin/bash

#./setup_firewall.sh
service pycr-firewall start
nohup /usr/sbin/inspircd --runasroot --debug --nopid & > irc.log
service snmpd restart
service postfix restart
service postgresql restart
service ntp restart
tail -f /dev/null
