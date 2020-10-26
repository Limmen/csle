#!/bin/bash

#./setup_firewall.sh
service pycr-firewall start
nohup /usr/sbin/vsftpd &
nohup /usr/bin/mongod &
/etc/init.d/inetutils-inetd restart
/usr/local/tomcat/bin/catalina.sh start
nohup /teamspeak3-server_linux_amd64/ts3server_startscript.sh start &
tail -f /dev/null
