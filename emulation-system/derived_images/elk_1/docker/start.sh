#!/bin/bash

/usr/sbin/sshd -D &
/usr/local/bin/start.sh
tail -f /dev/null
