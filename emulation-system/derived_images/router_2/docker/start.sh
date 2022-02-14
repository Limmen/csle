#!/bin/bash

/usr/sbin/sshd -D &
service rsyslog restart
sudo snort -D -q -u snort -g snort -c /etc/snort/snort.conf -i eth0 -l /var/snort/ -h 55.0.0.0/8
tail -f /dev/null

