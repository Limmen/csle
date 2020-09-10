#!/bin/bash

service snmpd restart
service postfix restart
tail -f /dev/null
