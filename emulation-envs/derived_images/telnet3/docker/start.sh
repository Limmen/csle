#!/bin/bash

#./setup_firewall.sh
service pycr-firewall start
/usr/sbin/sshd -D &
/etc/init.d/xinetd restart
/*glassfish*/bin/asadmin start-domain domain1
tail -f /dev/null
