# SambaCry Base Image

Samba base docker image, used for implementing sambacry cve-2017-7494 vulnerabilities  

## Useful commands

```bash
make rm-image # Delete built image
make build # Build docker image
make clean # Stop running container
make run # Run container
make net # Create Docker sub-network
make rm-net # Remove Docker sub-network
docker container ls --all # list all running containers
docker image ls --all # list all images
docker system prune # remove unused images and containers
docker container prune # remove stopped containers
sudo nmap -sU -p 161 <ip> # UDP scan to test that SNMP port is open
nmap -p- <ip> # Scan TCP ports   
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](LICENSE.md)

Creative Commons

(C) 2020, Kim Hammar