#!/bin/bash

/etc/init.d/xinetd restart
#/usr/sbin/in.telnetd -debug
python /web/web_server.py
tail -f /dev/null
