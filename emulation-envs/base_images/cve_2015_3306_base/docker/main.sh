#!/bin/bash

# Start apache
source /etc/apache2/envvars
apachectl -f /etc/apache2/apache2.conf

# start proftpd
proftpd --nodaemon
