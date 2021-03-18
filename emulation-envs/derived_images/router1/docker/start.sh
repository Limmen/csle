#!/bin/bash

/usr/sbin/sshd -D &
tail -f /dev/null

