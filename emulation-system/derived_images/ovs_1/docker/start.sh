#!/bin/bash

/usr/share/openvswitch/scripts/ovs-ctl start
/usr/sbin/sshd -D &
tail -f /dev/null
