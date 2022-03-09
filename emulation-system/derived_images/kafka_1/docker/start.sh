#!/bin/bash

/usr/sbin/sshd -D &
sudo service kafka start
tail -f /dev/null

