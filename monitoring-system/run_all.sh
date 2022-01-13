#!/bin/bash

./run_c_advisor.sh

nohup ./run_node_exporter.sh &
nohup ./run_prometheus.sh &

./run_grafana.sh

nohup ./csle_monitor.sh &

# Then connect, e.g. ssh -L 2381:localhost:8080 -L 2382:localhost:3000 -L 2383:localhost:9090 -L 2384:localhost:9100 kim@172.31.212.92
# ssh -L 2381:localhost:8080 -L 2382:localhost:3000 -L 2383:localhost:9090 -L 2384:localhost:9100 -L 2385:localhost:7777 kim@172.31.212.92
