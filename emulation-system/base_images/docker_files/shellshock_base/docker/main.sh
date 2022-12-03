#!/bin/bash

cd /etc/apache2/mods-enabled
sudo ln -s ../mods-available/cgi.load
/usr/sbin/apache2ctl -DFOREGROUND


