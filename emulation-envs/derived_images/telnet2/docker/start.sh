#!/bin/bash

#./setup_firewall.sh
service pycr-firewall start
/etc/init.d/xinetd restart
service rsyslog restart
/usr/sbin/sshd -D &
/cockroach-v20.1.8.linux-amd64/cockroach start-single-node --insecure --listen-addr=0.0.0.0:26257 --http-addr=0.0.0.0:8080 --background &
tail -f /dev/null
