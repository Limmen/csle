# CVE 2010-0426 Base Image

Base docker image with the CVE 2010-0426 vulnerability.

## Description
The bug was found in sudoedit, which does not handle the 'sudoedit' command correctly, this allows a malicious user to replace the real sudoedit command with an arbitrary command.

Local attackers could exploit this issue to run arbitrary commands as the 'root' user. Successful exploits can completely compromise an affected computer.    

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