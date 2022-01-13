#!/bin/bash

while [ 1 ]
do
    sleep 2
    timeout 5 sshpass -p 'test' ssh -oStrictHostKeyChecking=no 172.18.8.37 > /dev/null 2>&1
    sleep 2
    timeout 5 snmpwalk -v2c 172.18.8.37 -c csle_ctf1234 > /dev/null 2>&1
    sleep 2
    timeout 5 curl 172.18.8.37 > /dev/null 2>&1
    sleep 2
done