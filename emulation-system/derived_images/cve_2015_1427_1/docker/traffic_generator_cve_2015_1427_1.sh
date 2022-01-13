#!/bin/bash

while [ 1 ]
do
    sleep 2
    timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no 172.18.8.82 > /dev/null 2>&1
    sleep 2
    timeout 5 snmpwalk -v2c 172.18.8.82 -c csle_ctf1234 > /dev/null 2>&1
    sleep 2
done