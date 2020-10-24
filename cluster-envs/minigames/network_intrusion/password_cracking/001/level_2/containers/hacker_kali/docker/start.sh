#!/bin/bash

./setup_firewall.sh
/usr/sbin/sshd -D
tail -f /dev/null
