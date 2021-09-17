# Capture the Flag - Random Configurations

A set of virtual environment with a set of nodes that run common networked services such as SSH, FTP, Telnet, IRC, Kafka, 
Cassandra, etc. Some of the services are vulnerable to different types of network attacks. 
The task of an attacker agent is to identify the vulnerabilities and exploit them and discover hidden flags
on the nodes. Conversely, the task of the defender is to harden the defense of the nodes and to detect the 
attacker. 

The environment configurations are sampled randomly from the configuration space using a set of constraints on the number of nodes, number of flags,
number of vulnerabilities etc.  

## Architecture

The architecture is generated randomly using the preferental attachment theory. 

## Useful commands

```bash
make generate_envs # Generate the environments based on the configuration in `generate_config.py`
make topology # Generate the topology configuration according to `create_topology.py` and save to topology.json
make users # Generate the users configuration according to `create_users.py` and save to users.json
make flags # Generate the flags configuration according to `create_flags.py` and save to flags.json
make vuln # Generate the vulnerabilities configuration according to `create_vuln.py` and save to flags.json
make gen_config # Generate all configuration files according to `create_config.py`
make apply_config # Apply the configuration to the running emulations
make run # Runs the emulations (creates and starts them)
make stop # Stops the emulations
make start # Starts the emulations (assuming they are already created)
make clean # Cleans the emulations
make clean_envs # Cleans the emulation configurations
make clean_fs_cache # Cleans the cache files     
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](../../../../../../../LICENSE.md)

Creative Commons

(C) 2020, Kim Hammar