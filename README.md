# `pycr` The Python Cyber Range for Self-Learning Cyber Security Systems

TODO abstract

<p align="center">
    <a href="https://img.shields.io/badge/license-CC%20BY--SA%204.0-green">
        <img src="https://img.shields.io/badge/license-CC%20BY--SA%204.0-green" /></a>
    <a href="https://img.shields.io/badge/version-0.0.1-blue">
        <img src="https://img.shields.io/badge/version-0.0.1-blue" /></a>               
</p>

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
    - [x] 50+ pre-defined versions of emulation environments
    - [x] Automatic generation of custom emulation environment
    - [x] Monitoring Framework with Webapp, Grafana, Prometheus, C-advisor, Node-exporter
    - [x] Automatic Network Traffic Simulation
    - [x] 20+ vulnerable containers with exploits
    - [x] CTF challenges
    - [ ] Malware challenges
    - [ ] DoS challenges
    - [ ] Web hacking challenges  

- **Open-AI Gym Environment**
     - [x] GUI rendering
     - [x] 50+ versions of gym environments
     - [x] Simulation-mode
     - [x] Emulation-mode
     - [x] Manual-mode
     - [x] Emulation+Simulation-model (using system identification)
     - [x] Support for massively parallel training with distributed emulation/simulation environments
     
- **Learning Process**
     - [x] Attacker training
     - [x] Defender training
     - [x] Self-play                    
   
- **Reinforcement Learning Algorithms**
     - [x] PPO baseline
     - [x] DQN baseline
     - [x] DDPG baseline
     - [x] REINFORCE baseline
     - [x] TD3 baseline
     - [ ] MuZero baseline
     - [ ] Value Prediction Network baseline
     - [ ] Bayesian REINFORCE
     - [ ] Monte-Carlo Tree Search                    

- **System Identification**
     - [x] Custom system identifification algorithm to learn model of emulation
     - [x] Custom domain randomization algorithm
     - [ ] Function approximation

## Installation
TODO

## Quickstart
TODO

## Documentation

For basic documentation, see the README.md files inside each sub-directory,

- **Emulation Environments** ([emulation-envs](./emulation-envs)).
- **Python Environments** ([python-envs](./python-envs)).
- **Notebooks** ([notebooks](./notebooks)).
- **Documentation** ([docs](./docs)).

### API Documentation
For API documentation follow the links inside each python project's README:

- ([gym-pycr-ctf](./python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/README.MD)). 

### Technical Documentation
For technical documentation see: TODO

## Video tutorial

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](LICENSE.md)

Creative Commons

(C) 2021, Kim Hammar

## Publications

- **Finding Effective Security Strategies through Reinforcement Learning and Self-Play (https://arxiv.org/abs/2009.08120)**
```
@INPROCEEDINGS{Hamm2011:Finding,
AUTHOR="Kim Hammar and Rolf Stadler",
TITLE="Finding Effective Security Strategies through Reinforcement Learning and
{Self-Play}",
BOOKTITLE="International Conference on Network and Service Management (CNSM 2020)
(CNSM 2020)",
ADDRESS="Izmir, Turkey",
DAYS=1,
MONTH=nov,
YEAR=2020,
KEYWORDS="Network Security; Reinforcement Learning; Markov Security Games",
ABSTRACT="We present a method to automatically find security strategies for the use
case of intrusion prevention. Following this method, we model the
interaction between an attacker and a defender as a Markov game and let
attack and defense strategies evolve through reinforcement learning and
self-play without human intervention. Using a simple infrastructure
configuration, we demonstrate that effective security strategies can emerge
from self-play. This shows that self-play, which has been applied in other
domains with great success, can be effective in the context of network
security. Inspection of the converged policies show that the emerged
policies reflect common-sense knowledge and are similar to strategies of
humans. Moreover, we address known challenges of reinforcement learning in
this domain and present an approach that uses function approximation, an
opponent pool, and an autoregressive policy representation. Through
evaluations we show that our method is superior to two baseline methods but
that policy convergence in self-play remains a challenge."
}
```
- **Learning Intrusion Prevention Policies through Optimal Stopping (https://arxiv.org/abs/2106.07160)**
``` bash
@misc{hammar2021learning,
      title={Learning Intrusion Prevention Policies through Optimal Stopping},
      author={Kim Hammar and Rolf Stadler},
      year={2021},
      eprint={2106.07160},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
```

## See also

- [gym-idsgame](https://github.com/Limmen/gym-idsgame)
- [gym-optimal-intrusion-response](https://github.com/Limmen/gym-optimal-intrusion-response)

## Disclaimer

All code and software in this repository is for Educational purpose ONLY. 
Do not use it without permission. 
The usual disclaimer applies, especially the fact that me (Kim Hammar) is not liable for any damages caused by direct or indirect use of the information or functionality provided by these programs. 
The author or any Internet provider bears NO responsibility for content or misuse of these programs or any derivatives thereof. 
By using these programs you accept the fact that any damage (dataloss, system crash, system compromise, etc.) 
caused by the use of these programs is not Kim Hammar's responsibility.