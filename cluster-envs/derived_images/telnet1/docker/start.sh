#!/bin/bash

/etc/init.d/xinetd restart
/usr/sbin/sshd -D &
#/usr/sbin/in.telnetd -debug
python /web/web_server.py
tail -f /dev/null
