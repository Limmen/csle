#!/bin/bash

nohup /usr/sbin/vsftpd &
tail -f /dev/null
