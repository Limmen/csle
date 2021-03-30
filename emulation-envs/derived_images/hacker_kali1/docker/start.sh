#!/bin/bash

#./setup_firewall.sh
service pycr-firewall start
/usr/sbin/sshd -D
service rsyslog restart
tail -f /dev/null
