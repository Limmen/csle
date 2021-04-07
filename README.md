# `pycr` The Python Cyber Range for Self-Learning Cyber Security Systems

TODO abstract

## Outline

 * [What is pycr?](#what-is-pycr)
 * [Architecture](#architecture)
 * [Features](#features)
 * [Quickstart](#quickstart)
 * [Documentation](#documentation)
 * [Author &amp; Maintainer](#author--maintainer)
 * [Copyright and license](#copyright-and-license)
 * [Disclaimer](#disclaimer)


## What is `pycr`?

TODO

The environment implements virtual cyber ranges for training reinforcement learning agents. 
The environment exposes a Markov-game or Markov Decision Process API for OpenAI Gym.    

## Architecture

<p align="center">
<img src="docs/arch.png" width="600">
</p>

## Features

- **Emulations**
    - [x] 50+ pre-defined emulation environments
    - [x] Automatic generation of custom emulation environment
    - [x] Monitoring Framework with Webapp, Grafana, Prometheus, C-advisor, Node-exporter
    - [x] Automatic Network Traffic Simulation
    - [x] 20+ vulnerable containers with exploits 

- **Open-AI Gym Environment**
     - [x] GUI rendering
     - [x] 50+ gym environments
     - [x] Simulation-mode
     - [x] Emulation-mode
     - [x] Manual-mode
     - [x] Emulation+Simulation-model (using system identification)
     - [x] Support for massively parallel training with several emulation/simulation environments
     
- **Learning Process**
     - [x] Attacker training
     - [x] Defender training
     - [ ] Self-play                    
   
- **Reinforcement Learning Algorithms**
     - [x] PPO baseline
     - [x] DQN baseline
     - [x] DDPG baseline
     - [x] REINFORCE baseline
     - [x] TD3 baseline

- **System Identification**
     - [x] Custom system identifification algorithm to learn model of emulation
     - [x] Custom domain randomization algorithm          

## Quickstart
TODO

## Documentation

For documentation, see the README.md files inside each sub-directory,

- **Emulation Environments** ([emulation-envs](./emulation-envs)).
- **Python Environments** ([python-envs](./python-envs)).
- **Notebooks** ([notebooks](./notebooks)).
- **Documentation** ([docs](./docs)).

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](LICENSE.md)

Creative Commons

(C) 2021, Kim Hammar


## Disclaimer
All code and software in this repository is for Educational purpose ONLY. 
Do not use it without permission. 
The usual disclaimer applies, especially the fact that me (Kim Hammar) is not liable for any damages caused by direct or indirect use of the information or functionality provided by these programs. 
The author or any Internet provider bears NO responsibility for content or misuse of these programs or any derivatives thereof. 
By using these programs you accept the fact that any damage (dataloss, system crash, system compromise, etc.) 
caused by the use of these programs is not Kim Hammar's responsibility.