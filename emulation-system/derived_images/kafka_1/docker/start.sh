#!/bin/bash

/usr/sbin/sshd -D &
sudo service kafka stop
sleep 20
sudo service kafka start
tail -f /dev/null

