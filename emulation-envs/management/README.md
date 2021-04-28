# PyCR Management Scripts

This directory includes scripts for starting Grafana+Prometheus+Cadvisor+NodeExporter for monitoring running
emulations as well as the host system. 

The directory also includes a scripts for starting a custom web-app (`pycr_monitor`) 
for keeping track of the emulation configurations.

## Grafana
A webapp for monitoring emulation environments created with PyCr

<p align="center">
<img src="docs/grafana_1.png" width="1200">
</p>

<p align="center">
<img src="docs/grafana_2.png" width="1200">
</p>

## PyCr Monitor
A webapp for monitoring emulation environments created with PyCr

<p align="center">
<img src="pycr_monitor/docs/screen.png" width="1200">
</p>

## Useful scripts
```bash
./install.sh   # Installs prometheus, grafana, PyCRMonitor, NodeExporter, Dashboards, C_Advisor etc.
./pycr_monitor.sh  # Installs PyCRMonitor
./run_c_advisor.sh # Installs C_Advisor
./run_grafana.sh  # Installs Grafana
./run_node_exporter.sh # Installs node exporter
./run_prometheus.sh # Installs Prometheus

make list_stopped # list stopped PyCR containers
make list_running # list running PyCR containers
make list_images # list images used by PyCR containers
make stop_running # stop running PyCR containers
make rm_stopped # remove stopped PyCR containers
make rm_images # remove images used by PyCR containers
make start_stopped # start stopped PyCR containers
make clean_docker # clean docker (delete unused networks, containers, images, cache, etc.)
```

When importing Prometheus as a data source in Grafana, use
```bash
http://<ip>:9090
```
e.g.
```bash
http://172.31.212.92:9090
``` 

When everything is running, use the following command to setup tunnels:
```bash
ssh -L 2381:localhost:8080 -L 2382:localhost:3000 -L 2383:localhost:9090 -L 2384:localhost:9100 -L 2385:localhost:7777 kim@<server-ip>
```
then you can access Grafana at `localhost:2382`, Prometheus at `localhost:2383`, Node exporter at `localhost:2384`, and PyCr Monitor at `localhost:2385`

## Note

Note that if you have started the pycr_monitor but cannot access the app from a SSH tunnel, you may need to
edit `pycr_monitor/server/server.py` and update the hostname (e.g. `0.0.0.0` instead of `localhost`).

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](../../LICENSE.md)

Creative Commons

(C) 2020, Kim Hammar