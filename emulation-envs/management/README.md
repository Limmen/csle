# PyCR Management Scripts

This directory includes scripts for starting Grafana+Prometheus+Cadvisor+NodeExporter for monitoring running
emulations as well as the host system. 

The directory also includes a scripts for starting a custom web-app (`pycr_monitor`) 
for keeping track of the emulation configurations.

## Useful scripts
```bash
./install.sh 
./pycr_monitor.sh 
./run_c_advisor.sh
./run_grafana.sh
./run_node_exporter.sh
./run_prometheus.sh
make all
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