#!/bin/bash

#./setup_firewall.sh
service pycr-firewall start
/usr/sbin/sshd -D
tail -f /dev/null
