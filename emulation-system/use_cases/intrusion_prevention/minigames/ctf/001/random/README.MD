# Capture the Flag - Random Configuration

A virtual environment with a set of nodes that run common networked services such as SSH, FTP, Telnet, IRC, Kafka, 
Cassandra, etc. Some of the services are vulnerable to different types of network attacks. 
The task of an attacker agent is to identify the vulnerabilities and exploit them and discover hidden flags
on the nodes. Conversely, the task of the defender is to harden the defense of the nodes and to detect the 
attacker. 

The environment configuration is sampled randomly from the configuration space using a set of constraints on the number of nodes, number of flags,
number of vulnerabilities etc.  

## Architecture

The architecture is generated randomly using the preferential attachment theory. 

## Useful commands

```bash
make topology # Creates the topology configuration and saves to topology.json
make users # Creates the users configuration and saves to users.json
make flags # Creates the flags configuration and saves to flags.json
make vuln # Creates the vulnerabilities configuration and saves to vuln.json
make clean_config # Cleans the configuration files
make gen_config # Generates all of the configuration files
make clean_fs_cache # Cleans the cache files
make apply_config # Applies the generated configuration to a running emulation


make rm-image # Delete all built images
make build # Build all docker images
make clean # Stop all running containers
make run # Run all containers
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

[LICENSE](../../../../../../../LICENSE.md)

Creative Commons

(C) 2020, Kim Hammar