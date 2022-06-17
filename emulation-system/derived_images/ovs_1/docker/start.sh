#!/bin/bash

/var/ossec/bin/ossec-control start
/usr/share/openvswitch/scripts/ovs-ctl start
/usr/sbin/sshd -D &
tail -f /dev/null
