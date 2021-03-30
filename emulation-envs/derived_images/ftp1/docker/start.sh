#!/bin/bash

nohup /usr/sbin/vsftpd &
nohup /usr/bin/mongod &
service rsyslog restart
/usr/sbin/sshd -D &
/etc/init.d/inetutils-inetd restart
/usr/local/tomcat/bin/catalina.sh start
nohup /teamspeak3-server_linux_amd64/ts3server_startscript.sh start &
tail -f /dev/null
