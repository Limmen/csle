# `csle_pvs` CSLE Policy Validation System

A system for validating automated security policies 

<p align="center">
<img src="csle_pvs/docs/screen.png" width="1200">
</p>

## Architecture

<p align="center">
<img src="csle_pvs/docs/arch.png" width="400">
</p>

## Useful scripts

Start the `csle_pes` webapp:
```bash
./install_csle_pes.sh  # Installs the csle pes webapp
cd csle_pes/server
nohup python server.py & # Deploys the csle pes webbapp
```

When everything is running, use the following command to setup tunnels:
```bash
ssh -L 8888:localhost:8888 kim@<server-ip>
```
then you can access csle pes at `localhost:2385`

## Note

Note that if you have started the csle_monitor but cannot access the app from a SSH tunnel, you may need to
edit `csle_pes/server/server.py` and update the hostname (e.g. `0.0.0.0` instead of `localhost`).

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](../../LICENSE.md)

Creative Commons

(C) 2020, Kim Hammar