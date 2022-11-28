#!/bin/bash

nohup /usr/sbin/vsftpd &
service rsyslog restart
/usr/sbin/sshd -D &
/etc/init.d/inetutils-inetd restart
tail -f /dev/null
