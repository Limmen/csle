#!/bin/bash

while [ 1 ]
do
    timeout 5 ftp 172.18.8.79 > /dev/null 2>&1
    sleep 2
    timeout 5 sshpass -p 'test' ssh -oStrictHostKeyChecking=no 172.18.8.79 > /dev/null 2>&1
    sleep 2
    timeout 5 curl 172.18.8.79:8080 > /dev/null 2>&1
    sleep 2
    timeout 5 mongo --host 172.18.8.79 --port 27017 > /dev/null 2>&1
    sleep 2
done