#!/bin/bash

./setup_firewall.sh
/etc/init.d/xinetd restart
python /web/web_server.py
tail -f /dev/null
