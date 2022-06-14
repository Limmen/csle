#!/bin/bash

/var/ossec/bin/ossec-control start
service rsyslog restart
service postgresql restart
sleep 2
/usr/sbin/sshd -D &
/etc/init.d/xinetd restart
/*glassfish*/bin/asadmin start-domain domain1
tail -f /dev/null
