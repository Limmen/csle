#!/bin/bash

/usr/sbin/sshd -D &
/usr/local/samba/sbin/smbd -F -S -s /smb.conf --debuglevel=10
tail -f /dev/null
