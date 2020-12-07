#!/bin/bash

while :
do
	wget 172.18.3.2
	sleep 1
	psql -h 172.18.3.21 -p 5432
	sleep 1
	curl 172.18.3.3
	sleep 1
	curl 172.18.3.79:8080
	sleep 10
done