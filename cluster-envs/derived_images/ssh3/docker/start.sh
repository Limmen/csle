#!/bin/bash

#./setup_firewall.sh
service pycr-firewall start
service named start
service ntp restart
/usr/sbin/sshd -D &
tail -f /dev/null
