#!/bin/bash

/var/ossec/bin/ossec-control start
/etc/init.d/xinetd restart
service rsyslog restart
/usr/sbin/sshd -D &
python /web/web_server.py
tail -f /dev/null
