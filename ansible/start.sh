#!/bin/bash
source ~/.bashrc
~/anaconda3/bin/activate $1
csle stop clustermanager
sleep 2
csle start clustermanager
sleep 2
csle start cadvisor
csle start grafana
csle start prometheus
csle start node_exporter
csle start flask
csle start nginx