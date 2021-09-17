#!/bin/bash

while :
do
	wget 172.18.4.2
	sleep 1
	psql -h 172.18.4.21 -p 5432
	sleep 1
	curl 172.18.4.3
	sleep 1
	curl 172.18.4.79:8080
	sleep 10
done