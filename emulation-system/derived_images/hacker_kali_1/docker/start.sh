#!/bin/bash

#./setup_firewall.sh
service csle-firewall start
/usr/sbin/sshd -D
service rsyslog restart
tail -f /dev/null
