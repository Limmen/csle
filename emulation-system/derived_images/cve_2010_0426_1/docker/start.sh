#!/bin/bash

/usr/sbin/sshd -D &
service rsyslog restart
nohup /teamspeak3-server_linux_amd64/ts3server_startscript.sh start &
/usr/local/tomcat/bin/catalina.sh start
tail -f /dev/null
