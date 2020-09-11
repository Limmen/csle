#!/bin/bash

nohup /usr/sbin/vsftpd &
nohup /usr/bin/mongod &
/etc/init.d/inetutils-inetd restart
tail -f /dev/null
