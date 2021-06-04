# Blank Container Test - Version 001

A virtual environment with a set of blank containers that contain no preconfigured software except the operating system 

## Useful commands

```bash
make rm-image # Delete all built images
make build # Build all docker images
make clean # Stop all running containers
make run # Run all containers
make router # Run router container
make ssh # Run ssh container
make telnet # Run telnet container
make honeypot # Run honeypot container
make net # Create Docker sub-network
make rm-net # Remove Docker sub-network
make traffic # create traffic generators and start them on each node
make stop_traffic # stop traffic_generators that are running on each node
python run.py --build # build all containers with custom config
python run.py --run # run all containers with custom config
docker container ls --all # list all running containers
docker image ls --all # list all images
docker system prune # remove unused images and containers
docker container prune # remove stopped containers
sudo useradd -rm -d /home/pycr_admin -s /bin/bash -g root -G sudo -p "$(openssl passwd -1 'pycr@admin-pw_191')" pycr_admin   
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](../../../../../../LICENSE.md)

Creative Commons

(C) 2021, Kim Hammar