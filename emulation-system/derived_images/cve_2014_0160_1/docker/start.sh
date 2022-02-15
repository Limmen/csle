#!/bin/bash

/usr/sbin/sshd -D &
/usr/sbin/apache2ctl -DFOREGROUND
tail -f /dev/null
