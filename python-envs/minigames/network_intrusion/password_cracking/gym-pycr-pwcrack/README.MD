# `gym-pycr-pwcrack`

`gym-pycr-pwcrack` is a reinforcement learning environment for studying the "first line of defense" against
network intrusions. Specifically the environment focuses on reconnaissance, password vulnerabilities, 
intrusion detection, and dictionary attacks. The environment provides a MDP or Markov Game interface for 
OpenAI Gym that can be used to train reinforcement learning agents. 

Moreover, the repository contains code to reproduce baseline results for various reinforcement learning algorithms, including:

- DQN
- REINFORCE with baseline
- PPO
- AC3

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
sudo route add -net 172.18.1.0 netmask 255.255.255.0 gw 172.18.1.1
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](LICENSE.md)

Creative Commons

(C) 2020, Kim Hammar