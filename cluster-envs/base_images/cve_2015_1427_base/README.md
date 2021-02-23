# CVE-2015-1427 Base Image

Base docker image with the CVE 2015-1427 vulnerability.

## Description

The bug is found in the REST API, which does not require authentication, where the search function allows groovy code execution and its sandbox can be bypassed using `java.lang.Math.class.forName` to reference arbitrary classes. It can be used to execute arbitrary Java code. The bug is found in the REST API, which does not require authentication, where the search function allows groovy code execution and its sandbox can be bypassed using java.lang.Math.class.forName to reference arbitrary classes. It can be used to execute arbitrary Java code.    

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

(C) 2021, Kim Hammar