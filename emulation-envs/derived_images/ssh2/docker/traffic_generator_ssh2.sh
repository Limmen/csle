#!/bin/bash

while [ 1 ]
do
    sleep 2
    timeout 5 sshpass -p 'test' ssh -oStrictHostKeyChecking=no 172.18.8.21 > /dev/null 2>&1
    sleep 2
    timeout 5 nslookup limmen.dev 172.18.8.21 > /dev/null 2>&1
    sleep 2
done