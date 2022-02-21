# `csle`: Cyber Security Learning Environment

## A research platform to develop self-learning systems for cyber security using reinforcement learning 

`csle` is a platform for evaluating and developing reinforcement learning agents
for control problems in cyber security. It can be considered as a cyber range
specifically designed for reinforcement learning agents. Everything from
network emulation, to simulation and implementation of network commands have been
co-designed to provide an environment where it is possible to train and evaluate
reinforcement learning agents on practical problems in cyber security.

The platform can be used to implement different use cases. Each use case consist of an
emulated infrastructure (used for evaluation), and a MDP/POMDP/Markov Game interface for training agents.
For example, the platform can be used to study the use case of intrusion prevention and
train a reinforcement learning agent to prevent network intrusions by attackers in real-time.


<p align="center">
    <a href="https://img.shields.io/badge/license-CC%20BY--SA%204.0-green">
        <img src="https://img.shields.io/badge/license-CC%20BY--SA%204.0-green" /></a>
    <a href="https://img.shields.io/badge/version-0.0.1-blue">
        <img src="https://img.shields.io/badge/version-0.0.1-blue" /></a>
</p>

## Outline

 * [What is csle?](#what-is-csle)
 * [Architecture](#architecture)
 * [Features](#features)
 * [Quickstart](#quickstart)
 * [Documentation](#documentation)
 * [Author &amp; Maintainer](#author--maintainer)
 * [Copyright and license](#copyright-and-license)
 * [Disclaimer](#disclaimer)


## Architecture

The method used in `csle` for learning and validating policies includes two systems. 
First, we develop an **emulation system** where key functional components of 
the target infrastructure are replicated. In this system, we run attack scenarios and defender responses. 
These runs produce system metrics and logs that we use to estimate empirical distributions 
of infrastructure metrics, which are needed to simulate MDP/POMDP/Markov Game episodes. 
Second, we develop a **simulation system** where MDP/POMDP/Markov Game episodes are executed and 
policies are incrementally learned. 
Finally, the policies are extracted and evaluated in the emulation system, 
and can also be implemented in the target infrastructure. 
In short, the emulation system is used to provide the statistics needed to simulate the MDP/POMDP/Markov Game 
and to evaluate policies, whereas the simulation system is used to learn policies.


<p align="center">
<img src="docs/arch.png" width="600">
</p>

### Emulation System

The emulation system executes on a cluster of machines that runs a virtualization layer provided by 
Docker containers and virtual links. 
The system emulates the clients, the attacker, the defender, as well as physical components of the 
target infrastructure (e.g application servers and gateways). 
Physical entities are emulated and software functions are executed in Docker containers of the emulation system. 
The software functions replicate important components of the target infrastructure, 
such as, web servers, databases, and an IDS.

### Simulation System

The simulation system implements a MDP/POMDP/Markov Game that can be used to 
train defender policies using reinforcement learning. It exposes an OpenAI-gym interface.

### Policy Examination System

The policy examination system is a system for interactive examination of  learned security policies. It allows a user to traverse episodes of
Markov decision processes in a controlled manner and to track the actions triggered by security policies. Similar to a software 
debugger, a user can continue or or halt an episode at any time step and inspect parameters and probability distributions  
of interest. The system enables insight into the structure of a given policy and in the behavior of a policy in edge cases.

### Monitoring System

The monitoring system allows to track the execution of running emulations and their resource consumptions.

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
     
- **Demonstrations**
      
     - [x] A Dashboard for Inspecting Automated Intrusion Prevention Policies     

## Installation

Follow the instructions below to install CSLE.

### Install from source

1. **Clone the repository**
```bash
git clone https://github.com/Limmen/clse
```

2. **Install PostgreSQL as a metastore (see ([README](metastore/README.MD)) for more information)**
    - Installation:
      ```bash
      sudo apt-get install postgresql
      sudo apt-get install libpq-dev 
      ```
    - Setup a password for the postgres user:
      ```bash
      sudo -u postgres psql  # start psql session as admin user posgres
      psql> \password postgres # set postgres password
      ```
    - Setup password authentication for user postgres:
      1. Open file `/etc/postgresql/10/main/pg_hba.conf`
      2. Change `peer` to `md5` on line: `local all postgres peer`
      3. Save and close the file
      4. Restart postgres with the command `sudo service postgresql restart`
    - Create database and tables:
     ```bash
     sudo psql -U postgres -a -f metastore/create_tables.sql
     ```
     Alternatively:
    ```bash
     cd metastore; make build
     ```
   - To reset the metastore, run:
    ```bash
     cd metastore; make clean
     ```
   and then rebuild it with the commands above.

3. **Install the simulation system**
    - Install Python 3.8 or higher:
        - Using conda:
          ```bash
           conda create -n py38 python=3.8
          ```
        - Using apt:
          ```bash
           sudo apt install python3.8
          ```

   - Install `csle_collector` (see ([README](simulation-system/csle-collector/README.md)) for more information)
     ```bash
      cd simulation-system/csle-collector/
      pip install -e .
     ```

    - Install `csle_common` (see ([README](simulation-system/csle-common/README.md)) for more information)
      ```bash
       cd simulation-system/csle-common/
       pip install -e .
      ```

    - Install `gym_csle_ctf` (see ([README](simulation-system/gym-csle-ctf/README.MD)) for more information)
      ```bash
      cd simulation-system/gym-csle-ctf/
      pip install -e .
      ```
    
4. **Install the CLI tool**
    - Make the CLI tool executable:
      ```bash
      sudo chmod u+x bin/csle
      ```
    - Add the CLI tool to the $PATH environment variable (replace `/path/to` with the full path)
      ```bash
      export PATH=/path/to/csle/bin/:$PATH
      ```
    - To have the binary permanently in $PATH, add the following line to the .bashrc: `export PATH=/path/to/csle/bin/$PATH`

5. **Install the emulation system** 
    - Install Docker (see ([README](emulation-system/README.MD)) for more information)
      ```bash
      sudo apt-get update
      sudo apt-get install docker-ce docker-ce-cli containerd.io
      sudo groupadd docker
      sudo usermod -aG docker $USER
      ```
    - Install base images (see ([README](emulation-system/base_images/README.MD)) for more information) (this may take a while, e.g. an hour) 
      ```bash
      cd emulation-system/base_images
      make build
      ```
    - Install derived images (see ([README](emulation-system/derived_images/README.MD)) for more information)
      ```bash
      cd emulation-system/derived_images
      make build
      ```
    - Install emulation envs (see [README](emulation-system/envs/README.MD) for more information)
      ```bash
      cd emulation-system/envs
      make install
      ```
    - Alternatively you can install everything at once (assuming you have already installed Docker and the metastore) 
     by running the commands:
      ```bash
      cd emulation-system
      make build
      ```   

6. **Install the monitoring system**
   - To build the webapp used in the monitoring system and in the policy examination system 
   you need node.js and npm installed, to install node and npm execute:
      ```bash
      curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash # install nvm
      command -v nvm # Verify nvm installation
      nvm install node # Install node
      npm install -g npm # Update npm
      node -v # Verify version of node
      npm -v # Verify version of npm
      ```
   - Install the monitoring system and associated tools:
    ```bash
      cd monitoring-system
      chmod u+x install.sh
      ./install.sh
    ```
   - Run the monitoring system (for more instructions see [README](monitoring system/README.MD)):
    ```bash
      cd monitoring-system
      chmod u+x run_all.sh
      ./run_all.sh
    ```
    
7. **Install the policy examination system** 
   - Build the policy examination system (assuming that node and npm is already installed) (for more instructions see [README](policy-examination-system/README.MD)):
   ```bash
   cd policy-examination-system
   ./install_csle_pes.sh   
   ```
   - Start the policy examination system:
   ```bash
   cd policy-examination-system/csle_pvs/server
   nohup python server.py &  
   ```

## Uninstall

```bash
csle rm all
csle clean emulations
csle rm emulations
pip uninstall gym-csle-ctf
pip uninstall csle-common
cd emulation-system && make rm
cd metastore; make clean
```

## Quickstart

To see the available commands, run:
```bash
csle --help
```

Examples:

- List available containers, emulations, images, and networks:
```bash
csle ls --all
```

- List containers only
```bash
csle ls containers --all
```

- List running containers only
```bash
csle ls containers
```

- List emulations
```bash
csle ls emulations --all
```

- List running emulations only
```bash
csle ls emulations
```

- Inspect a specific emulation/container/image/network
```bash
csle ls <name>
```

- Start/Stop/Clean a specific emulation/container
```bash
csle start| stop | clean <name>
```

- Open a shell in a given container
```bash
csle shell <container-name>
```

- Remove a container, image, network, emulation, or all
```bash
csle rm <container-name> | <network-name> | <image-name> | <emulation-name> all
```

## Documentation

For documentation, see the README.md files inside each sub-directory,

- **Emulation System** ([emulation-system](./emulation-system)).
- **Simulation System** ([simulation-system](./simulation-system)).
- **Monitoring System** ([monitoring-system](./monitoring-system)).
- **Policy Examination System** ([policy-examination-system](./policy-examination-system)).
- **Metastore** ([metastore](./metastore)).
- **General Documentation** ([docs](./docs)).

## Video tutorial

TODO

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](LICENSE.md)

Creative Commons

(C) 2022, Kim Hammar

## Publications

- **Finding Effective Security Strategies through Reinforcement Learning and Self-Play (CNSM 2020) (preprint: https://arxiv.org/abs/2009.08120, proceedings: https://ieeexplore.ieee.org/document/9269092, IFIP Open Library Conference proceedings: http://dl.ifip.org/db/conf/cnsm/cnsm2020/index.html)**
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
- **Learning Intrusion Prevention Policies through Optimal Stopping (CNSM 2021) (preprint: https://arxiv.org/abs/2106.07160, IEEE Proceedings: https://ieeexplore.ieee.org/document/9615542, IFIP Open Library Conference proceedings: http://dl.ifip.org/db/conf/cnsm/cnsm2021/1570732932.pdf)**
``` bash
@INPROCEEDINGS{hammar_stadler_cnsm_21,
AUTHOR="Kim Hammar and Rolf Stadler",
TITLE="Learning Intrusion Prevention Policies through Optimal Stopping",
BOOKTITLE="International Conference on Network and Service Management (CNSM 2021)",
ADDRESS="Izmir, Turkey",
DAYS=1,
YEAR=2021,
note={\url{http://dl.ifip.org/db/conf/cnsm/cnsm2021/1570732932.pdf}},
KEYWORDS="Network Security, automation, optimal stopping, reinforcement learning, Markov Decision Processes",
ABSTRACT="We study automated intrusion prevention using reinforcement learning. In a novel approach, we formulate the problem of intrusion prevention as an optimal stopping problem. This formulation allows us insight into the structure of the optimal policies, which turn out to be threshold based. Since the computation of the optimal defender policy using dynamic programming is not feasible for practical cases, we approximate the optimal policy through reinforcement learning in a simulation environment. To define the dynamics of the simulation, we emulate the target infrastructure and collect measurements. Our evaluations show that the learned policies are close to optimal and that they indeed can be expressed using thresholds."
}
```

- **Intrusion Prevention through Optimal Stopping (Preprint: https://arxiv.org/abs/2111.00289)**

```bash
@misc{hammar2021intrusion,
      title={Intrusion Prevention through Optimal Stopping},
      author={Kim Hammar and Rolf Stadler},
      year={2021},
      eprint={2111.00289},
      archivePrefix={arXiv},
      primaryClass={cs.LG}
}
```

- **A System for Interactive Examination  of Learned Security Policies (Preprint: https://limmen.dev/assets/papers/NOMS22_Demo_Policy_Examination_System_Hammar_Stadler_28_Jan_2022.pdf)**

```bash
@misc{hammar2022policyexamination,
      title={A System for Interactive Examination  of Learned Security Policies},
      author={Kim Hammar and Rolf Stadler},
      year={2022}
}
```

## See also

- [gym-idsgame](https://github.com/Limmen/gym-idsgame)
- [gym-optimal-intrusion-response](https://github.com/Limmen/gym-optimal-intrusion-response)
- [awesome-rl-for-cybersecurity](https://github.com/Limmen/awesome-rl-for-cybersecurity)

## Disclaimer

All code and software in this repository is for Educational purpose ONLY.
Do not use it without permission.
The usual disclaimer applies, especially the fact that me (Kim Hammar) is not liable for any damages caused by direct or indirect use of the information or functionality provided by these programs.
The author or any Internet provider bears NO responsibility for content or misuse of these programs or any derivatives thereof.
By using these programs you accept the fact that any damage (dataloss, system crash, system compromise, etc.)
caused by the use of these programs is not Kim Hammar's responsibility.
