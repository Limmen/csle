#!/bin/bash

/etc/init.d/xinetd restart
python /web/web_server.py
tail -f /dev/null
