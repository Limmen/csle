# CVE 2015-5602 Base Image

Base docker image with the CVE 2010-0426 vulnerability.

## Description
The bug was found in sudoedit, which does not check the full path if a wildcard is used twice 
(e.g. `/home/*/*/esc.txt`), this allows a malicious user to replace the esc.txt real file with a symbolic link to a different location 
(e.g. `/etc/shadow`).

Successfully exploiting this issue may allow an attacker to manipulate files and to gain root privileges 
on host system through symlink attacks.    

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