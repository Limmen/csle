# Derived Images

This directory contains derived Docker images used in `pycr` when emulating computer infrastructures. 
These images are derivations of the [base images](../base_images) of `pycr`. The derived images include
kali images, vulnerable images, and images with general network services. These images can be used to 
generate containers for emulating various network infrastructures.

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
python run.py --build # build all containers with custom config
python run.py --run # run all containers with custom config
docker container ls --all # list all running containers
docker image ls --all # list all images
docker system prune # remove unused images and containers
docker container prune # remove stopped containers   
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](LICENSE.md)

Creative Commons

(C) 2020, Kim Hammar