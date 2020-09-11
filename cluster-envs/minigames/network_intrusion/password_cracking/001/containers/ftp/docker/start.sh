#!/bin/bash

nohup /usr/sbin/vsftpd &
/etc/init.d/inetutils-inetd restart
tail -f /dev/null
