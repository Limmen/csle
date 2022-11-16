# `csle`: Cyber Security Learning Environment

## A research platform to develop self-learning systems for cyber security using reinforcement learning

`csle` is a platform for evaluating and developing reinforcement learning agents for control problems in cyber security.
It can be considered as a cyber range specifically designed for reinforcement learning agents. Everything from network
emulation, to simulation and implementation of network commands have been co-designed to provide an environment where it
is possible to train and evaluate reinforcement learning agents on practical problems in cyber security.

The platform can be used to implement different use cases. Each use case consist of an emulated infrastructure (used for
evaluation), and a MDP/POMDP/Markov Game interface for training agents. For example, the platform can be used to study
the use case of intrusion prevention and train a reinforcement learning agent to prevent network intrusions by attackers
in real-time.


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

The method used in `csle` for learning and validating policies includes two systems. First, we develop an **emulation
system** where key functional components of the target infrastructure are replicated. In this system, we run attack
scenarios and defender responses. These runs produce system metrics and logs that we use to estimate empirical
distributions of infrastructure metrics, which are needed to simulate MDP/POMDP/Markov Game episodes. Second, we develop
a **simulation system** where MDP/POMDP/Markov Game episodes are executed and policies are incrementally learned.
Finally, the policies are extracted and evaluated in the emulation system, and can also be implemented in the target
infrastructure. In short, the emulation system is used to provide the statistics needed to simulate the MDP/POMDP/Markov
Game and to evaluate policies, whereas the simulation system is used to learn policies.


<p align="center">
<img src="docs/arch.png" width="600">
</p>

### Emulation System

The emulation system executes on a cluster of machines that runs a virtualization layer provided by Docker containers
and virtual links. The system emulates the clients, the attacker, the defender, as well as physical components of the
target infrastructure (e.g application servers and gateways). Physical entities are emulated and software functions are
executed in Docker containers of the emulation system. The software functions replicate important components of the
target infrastructure, such as, web servers, databases, and an IDS.

### Simulation System

The simulation system implements a MDP/POMDP/Markov Game that can be used to train defender policies using reinforcement
learning. It exposes an OpenAI-gym interface.

### Monitoring System

The monitoring system allows to track the execution of running emulations and their resource consumptions. It also
includes an operations center where emulations can be managed and learned policies can be examines. Specifically, the
policy examination component of the monitoring system is a component for interactive examination of learned security
policies. It allows a user to traverse episodes of Markov decision processes in a controlled manner and to track the
actions triggered by security policies. Similar to a software debugger, a user can continue or or halt an episode at any
time step and inspect parameters and probability distributions  
of interest. The system enables insight into the structure of a given policy and in the behavior of a policy in edge
cases.

## Features

- **Emulations**
    - [x] 50+ pre-defined versions of emulation environments
    - [x] Automatic generation of custom emulation environment
    - [x] Monitoring Framework with Webapp, Grafana, Prometheus, C-advisor, Node-exporter
    - [x] Automatic Network Traffic Simulation
    - [x] 20+ vulnerable containers with exploits

- **Open-AI Gym Environment**
    - [x] GUI rendering
    - [x] optimal stopping game
    - [x] Simulation-mode
    - [x] Emulation-mode

- **Learning Process**
    - [x] Attacker training
    - [x] Defender training
    - [x] Self-play

- **System Identification**
    - [x] Custom system identifification algorithm to learn model of emulation
    - [ ] Function approximation

- **Policy-examination**
    - [x] A System for Inspecting Automated Intrusion Prevention Policies

- **Management and Monitoring**
    - [x] A distributed telemetry system for real-time monitoring
    - [x] A management platform with an extensive REST API and web frontend

## Installation

Follow the instructions below to install CSLE on a Ubuntu server.

### Install from source

1. **Install build tools and version management tools**

```bash
apt install make
apt install git
apt install bzip2
wget https://repo.anaconda.com/archive/Anaconda3-5.0.0-Linux-x86_64.sh
chmod u+rwx Anaconda3-5.0.0-Linux-x86_64.sh
./Anaconda3-5.0.0-Linux-x86_64.sh
```

2. **Setup the configuration**

- Setup your configuration (e.g define username and passwords) by editing the config file `csle/config.json`

3. **Clone the repository, set CSLE_HOME environment variable and setup logging directory**

```bash
git clone https://github.com/Limmen/clse
export CSLE_HOME=/path/to/csle/ # for bash
set -gx CSLE_HOME "/path/to/csle"  # for fish
```

To set CSLE_HOME permanently, add the following line to the .bashrc: `export CSLE_HOME=/path/to/csle/`

PID files of CSLE will be stored in `/var/log/csle`, create this directory and set the permissions so that the user used for
running commands can read and write to this directory.

Logs of CSLE will be stored in `/tmp/csle`, create this directory and set the permissions so that the user used for
running commands can read and write to this directory.

4. **Create log directory**
   - ```bash
     mkdir /tmp/csle     
     ```

5. **Create PID file directory**
   - ```bash
     mkdir /var/log/csle
     mkdir /var/log/csle/datasets
     chmod -R 777 /var/log/csle     
     ```

6. **Install PostgreSQL as a metastore (see ([README](metastore/README.MD)) for more information)**
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
    - Setup password authentication for user postgres and allow remote connections:
        1. Open file `/etc/postgresql/<YOUR_VERSION>/main/pg_hba.conf`
        2. Change `peer` to `md5` on line: `local all postgres peer`
        3. Add the line `host    all             all             0.0.0.0/0            md5`
        4. Open file `/etc/postgresql/<YOUR_VERSION>/main/postgresql.conf`
        5. Change `localhost` to `*` on line `listen_addresses = 'localhost'`
        6. Save and close the file
        7. Restart postgres with the command `sudo service postgresql restart`
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

7. **Install the simulation system**
    - Install Python 3.8 or higher:
        - Using conda:
          ```bash
           conda create -n py38 python=3.8
          ```
        - Using apt:
          ```bash
           sudo apt install python3.8
          ```
    - Activate the conda environment
    ```bash
    source activate python38
    ```

    - Install `csle-collector` (see ([README](simulation-system/csle-collector/README.md)) for more information)
      ```bash
       cd simulation-system/python/csle-collector/
       pip install -e .
       cd ../../../
      ```

    - Install `csle-common` (see ([README](simulation-system/csle-common/README.md)) for more information)
      ```bash
       cd simulation-system/python/csle-common/
       pip install -e .
       cd ../../../
      ```

    - Install `csle-attacker` (see ([README](simulation-system/csle-attacker/README.md)) for more information)
      ```bash
      cd simulation-system/python/csle-attacker/
      pip install -e .
      cd ../../../
      ```

    - Install `csle-defender` (see ([README](simulation-system/csle-defender/README.md)) for more information)
      ```bash
      cd simulation-system/python/csle-defender/
      pip install -e .
      cd ../../../
      ```

    - Install `gym-csle-stopping-game` (see ([README](simulation-system/gym-csle-stopping-game/README.MD)) for more
      information)
      ```bash
      cd simulation-system/python/gym-csle-stopping-game/
      pip install -e .
      cd ../../../
      ```

    - Install `csle-system-identification` (see ([README](simulation-system/csle-system-identification/README.MD)) for more
      information)
      ```bash
      cd simulation-system/python/csle-system-identification/
      pip install -e .
      cd ../../../
      ```

    - Install `csle-agents` (see ([README](simulation-system/csle-agents/README.MD)) for more
      information)
      ```bash
      cd simulation-system/python/csle-agents/
      pip install -e .
      cd ../../../
      ```

    - Install `csle-ryu` (see ([README](simulation-system/csle-ryu/README.MD)) for more
      information)
      ```bash
      cd simulation-system/python/csle-ryu/
      pip install -e .
      cd ../../../
      ```

    - Install `csle-rest-api` (see ([README](simulation-system/csle-rest-api/README.MD)) for more
      information)
      ```bash
      cd simulation-system/python/csle-rest-api/
      pip install -e .
      cd ../../../
      ```

    - Install simulation envs (see [README](simulation-system/envs/README.MD) for more information)
      ```bash
      cd simulation-system/envs
      make install
      cd ../../
      ```

8. **Install the CLI tool**
    - Install the CLI tool and make it executable as a script:
      ```bash
      cd csle-cli
      pip install -e .
      cd ../../../     
      ```
    - Setup auto-completion in BASH by generating the following file:
      ```bash
      _CSLE_COMPLETE=bash_source csle > ~/.csle-complete.bash
      ```
      and then adding the following line to ~/.bashrc
      ```bash
      . ~/.csle-complete.bash
      ```
    - Setup auto-completion in Fish:
      ```bash
      _CSLE_COMPLETE=fish_source csle > ~/.config/fish/completions/csle.fish 
      ```
   - Initialize management users
     ```bash
     csle init 
     ```      

9. **Install the emulation system**
    - Add Docker's official GPG key:
      ```bash
      sudo mkdir -p /etc/apt/keyrings
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
      echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
      ```
    - Install Docker (see ([README](emulation-system/README.MD)) for more information)
      ```bash
      sudo apt-get update
      sudo apt-get install docker-ce docker-ce-cli containerd.io
      sudo groupadd docker
      sudo usermod -aG docker $USER
      ```
    - Install base images (see ([README](emulation-system/base_images/README.MD)) for more information) (this may take a
      while, e.g. an hour)
      ```bash
      cd emulation-system/base_images
      make build
      cd ../../
      ```
    - Install derived images (see ([README](emulation-system/derived_images/README.MD)) for more information)
      ```bash
      cd emulation-system/derived_images
      make build
      cd ../../
      ```
    - Install emulation envs (see [README](emulation-system/envs/README.MD) for more information)
      ```bash
      cd emulation-system/envs
      make install
      cd ../../
      ```
    - Alternatively you can install everything at once (assuming you have already installed Docker and the metastore)
      by running the commands:
      ```bash
      cd emulation-system
      make build
      cd ../
      ```   

10. **Install the monitoring system**
     - To build the webapp used in the monitoring system and in the policy examination system you need node.js and npm
       installed, to install node and npm execute:
        ```bash
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash # install nvm
        nvm -v # Verify nvm installation
        nvm install node # Install node
        npm install -g npm # Update npm
        node -v # Verify version of node
        npm -v # Verify version of npm       
        ```
     - To serve the webapp withe TLS you need nginx as a reverse proxy, install and start nginx with the following commands:
       ```bash
       sudo apt install nginx
       sudo service nginx start
       ```
     - Configure nginx by editing `/etc/nginx/sites-available/default` and modifying location `/` inside the server object 
       by adding the following:
       ```bash
       location / {
           proxy_pass http://localhost:7777/;
           proxy_buffering off;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-Host $host;
           proxy_set_header X-Forwarded-Port $server_port;
       }
       ```
     - Restart nginx:
       ```bash
       sudo service nginx restart
       ```
     - If you have HTTPS enabled on the REST API and have certificates you can configure them in NGINX as follows 
       by editing `/etc/nginx/sites-available/default`:
       ```bash
       server {                                                                                                                                                                                      
            listen 80 default_server;                                                                                                                                                             
            listen [::]:80 default_server;                                                                                                                                                        
            server_name _;                                                                                                                                                                        
            return 301 https://$host$request_uri;                                                                                                                                                 
        }
        
        server {                                                                                                                                                                                      
            listen 443 ssl default_server;                                                                                                                                                        
            listen [::]:443 ssl default_server;                                                                                                                                                   
            ssl_certificate /var/log/csle/certs/csle.dev.crt;                                                                                                                                     
            ssl_certificate_key /var/log/csle/certs/csle_private.key;                                                                                                                             
            root /var/www/html;                                                                                                                                                                   
            index index.html index.htm index.nginx-debian.html;                                                                                                                                   
            server_name csle.dev;                                                                                                                                                                 
            location / {                                                                                                                                                                          
            proxy_pass http://localhost:7777/;                                                                                                                                            
            proxy_buffering off;                                                                                                                                                          
            proxy_set_header X-Real-IP $remote_addr;                                                                                                                                      
            proxy_set_header X-Forwarded-Host $host;                                                                                                                                      
            proxy_set_header X-Forwarded-Port $server_port;                                                                                                                               
            }                                                                                                                                                                                     
        }
       ```
     - Install the monitoring system and associated tools:
     ```bash
       cd monitoring-system
       chmod u+x install.sh
       ./install.sh
     ```
     - Configure the IP of the server where the monitoring system runs by editing the file:
      ```bash
       csle/monitoring-system/csle-mgmt-webapp/src/components/Common/serverIp.js
      ```
     - Add prometheus binary to the path
       ```bash
        export PATH=/path/to/csle/monitoring-system/prometheus/:$PATH
        ```
       or for fish shell:
       ```bash
        fish_add_path /path/to/csle/monitoring-system/prometheus/
        ```
    To have the binary permanently in $PATH, add the following line to the
    .bashrc: `export PATH=/path/to/csle/monitoring-system/prometheus/:$PATH`
     - Add node_exporter binary to the path
       ```bash
        export PATH=/path/to/csle/monitoring-system/node_exporter/:$PATH
        ```
       or for fish shell:
       ```bash
        fish_add_path /path/to/csle/monitoring-system/node_exporter/
        ```
    To have the binary permanently in $PATH, add the following line to the
    .bashrc: `export PATH=/path/to/csle/monitoring-system/node_exporter/:$PATH`
     - Run the monitoring system (for more instructions see [README](monitoring system/README.MD)):
     ```bash
       cd monitoring-system
       chmod u+x run_all.sh
       ./run_all.sh
     ```

## Uninstall

```bash
csle rm all
csle clean emulations
csle rm emulations
pip uninstall gym-csle-stopping-game
pip uninstall csle-common
pip uninstall csle-collector
pip uninstall csle-agents
pip uninstall csle-ryu
pip uninstall csle-rest
pip uninstall csle-system-identification
pip uninstall csle-attacker
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

- Install emulations, simulations, or Docker images

```bash
csle install emulations | simulations | derived_images | base_images | <emulation_name> | <simulation_name> | <derived_image_name> | <base_image_name> | all
```

- Uninstall emulations, simulations, or Docker images

```bash
csle uninstall emulations | simulations | derived_images | base_images | <emulation_name> | <simulation_name> | <derived_image_name> | <base_image_name> | all
```

## Documentation

For documentation, see the README.md files inside each sub-directory,

- **Emulation System** ([emulation-system](./emulation-system)).
- **Simulation System** ([simulation-system](./simulation-system)).
- **Monitoring System** ([monitoring-system](./monitoring-system)).
- **Metastore** ([metastore](./metastore)).
- **General Documentation** ([docs](./docs)).

## Video tutorials

### NOMS22 Demo - A System for Interactive Examination of Learned Security Policies 

[![IMAGE ALT TEXT](http://img.youtube.com/vi/18P7MjPKNDg/0.jpg)](http://www.youtube.com/watch?v=18P7MjPKNDg "A System for Interactive Examination of Learned Security Policies - Hammar & Stadler")

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](LICENSE.md)

Creative Commons

(C) 2020-2022, Kim Hammar

## Publications

- **Finding Effective Security Strategies through Reinforcement Learning and Self-Play (CNSM 2020) (
  preprint: https://arxiv.org/abs/2009.08120, proceedings: https://ieeexplore.ieee.org/document/9269092, IFIP Open
  Library Conference proceedings: http://dl.ifip.org/db/conf/cnsm/cnsm2020/index.html)**

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

- **Learning Intrusion Prevention Policies through Optimal Stopping (CNSM 2021) 
  preprint: https://arxiv.org/abs/2106.07160, IEEE Proceedings: https://ieeexplore.ieee.org/document/9615542, IFIP Open
  Library Conference proceedings: http://dl.ifip.org/db/conf/cnsm/cnsm2021/1570732932.pdf**

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

- **Intrusion Prevention through Optimal Stopping (TNSM 2022) IEEE proceedings: https://ieeexplore.ieee.org/document/9779345, Preprint: https://arxiv.org/abs/2111.00289**

```bash
@ARTICLE{9779345,
  author={Hammar, Kim and Stadler, Rolf},
  journal={IEEE Transactions on Network and Service Management}, 
  title={Intrusion Prevention through Optimal Stopping}, 
  year={2022},
  volume={},
  number={},
  pages={1-1},
  doi={10.1109/TNSM.2022.3176781}}
```

- **A System for Interactive Examination of Learned Security Policies (NOMS 2022 - BEST DEMO PAPER)(IEEE proceedings: https://ieeexplore.ieee.org/document/9789707
  Preprint: https://arxiv.org/abs/2204.01126)**

```bash
@INPROCEEDINGS{hammar_stadler_noms_22,
  author={Hammar, Kim and Stadler, Rolf},
  booktitle={NOMS 2022-2022 IEEE/IFIP Network Operations and Management Symposium},
  title={A System for Interactive Examination of Learned Security Policies},
  year={2022},
  volume={},
  number={},
  pages={1-3},
  doi={10.1109/NOMS54207.2022.9789707}}
```

- **Learning Security Strategies through Game Play and Optimal Stopping (ICML 2022 ML4Cyber Workshop)
  Preprint: https://arxiv.org/abs/2205.14694)**

```bash
@inproceedings{hammar_stadler_game_22_preprint,
  author = {Hammar, Kim and Stadler, Rolf},
  title = {Learning Security Strategies through Game Play and Optimal Stopping},
  booktitle = {Proceedings of the ML4Cyber workshop at the
               39th International Conference on Machine Learning,
               {ICML} 2022, Baltimore, USA, July
               17-23, 2022},
  publisher = {{PMLR}},
  year      = {2022}
}
```

- **An Online Framework for Adapting Security Policies in Dynamic IT Environments
  Preprint: https://limmen.dev/assets/papers/CNSM22_preprint_8_sep_Hammar_Stadler.pdf**

```bash
@inproceedings{hammar_stadler_cnsm22,
  author = {Hammar, Kim and Stadler, Rolf},
  title = {An Online Framework for Adapting Security Policies in Dynamic IT Environments},
  booktitle = {International Conference on Network and Service Management (CNSM 2022)},
  year      = {2022}
}
```

## See also

- [gym-idsgame](https://github.com/Limmen/gym-idsgame)
- [gym-optimal-intrusion-response](https://github.com/Limmen/gym-optimal-intrusion-response)
- [awesome-rl-for-cybersecurity](https://github.com/Limmen/awesome-rl-for-cybersecurity)

## Disclaimer

All code and software in this repository is for Educational purpose ONLY. Do not use it without permission. The usual
disclaimer applies, especially the fact that me (Kim Hammar) is not liable for any damages caused by direct or indirect
use of the information or functionality provided by these programs. The author or any Internet provider bears NO
responsibility for content or misuse of these programs or any derivatives thereof. By using these programs you accept
the fact that any damage (dataloss, system crash, system compromise, etc.)
caused by the use of these programs is not Kim Hammar's responsibility.
