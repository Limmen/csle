#!/bin/bash

./setup_firewall.sh
/etc/init.d/xinetd restart
/*glassfish*/bin/asadmin start-domain domain1
tail -f /dev/null
