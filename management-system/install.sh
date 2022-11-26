#!/bin/bash

wget https://github.com/prometheus/prometheus/releases/download/v2.23.0/prometheus-2.23.0.linux-amd64.tar.gz
wget https://github.com/prometheus/node_exporter/releases/download/v1.0.1/node_exporter-1.0.1.linux-amd64.tar.gz

tar xvfz prometheus-2.23.0.linux-amd64.tar.gz
tar xvfz node_exporter-1.0.1.linux-amd64.tar.gz

mv prometheus-2.23.0.linux-amd64 prometheus
mv node_exporter-1.0.1.linux-amd64 node_exporter

mv prometheus.yml prometheus/prometheus.yml

#sudo sysctl fs.inotify.max_user_watches=1048576

#sudo npm cache clean -f

#cd csle-mgmt-webapp; npm install --force
#sudo npm install react-file-download --save
#sudo npm install react-bootstrap bootstrap

