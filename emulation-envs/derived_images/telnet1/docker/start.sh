#!/bin/bash

/etc/init.d/xinetd restart
/usr/sbin/sshd -D &
python /web/web_server.py
tail -f /dev/null
