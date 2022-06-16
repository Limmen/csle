#!/bin/bash

/var/ossec/bin/ossec-control start
/usr/sbin/sshd -D &
tail -f /dev/null
