---
title: Installing CSLE
permalink: /docs/ansible-installing/
---

## Installing CSLE

This section contains instructions for installing CSLE. A video that walks through the installation process is
available [here](https://www.youtube.com/watch?v=l_g3sRJwwhc).

### Prerequisites

To install and run CSLE you need at least one server or virtual machine that meets the following criteria:

- Ubuntu 18.04+;
- at least 16GB RAM (the exact amount of RAM necessary depends on the emulations to deploy; 16GB is sufficient for the smallest emulations, e.g., in the size of 5-10 containers);
- at least 2 CPUs;
- 50 GB of free hard-disk space;
- outside Internet access;
- and a UNIX user account with `sudo` privileges.

Below are a list of dependencies that will be installed with CSLE (unless they are already installed):

- Docker 20.10.14+;
- Python 3.9+;
- Python libraries: `torch`, `numpy`, `gym`, `docker`, `paramiko`, `stable-baselines3`, `psycopg`, `pyglet`, `flask`, `click`, `waitress`, `scp`, `psutil`, `grpcio`, `grpcio-tools`, `scipy`, `confluent-kafka`, `requests`, `pyopenssl`, `sphinx`, `mypy`, `mypy-extensions`, `mypy-protobuf`, `types-PyYAML`, `types-protobuf`, `types-paramiko`, `types-requests`, `types-urllib3`, `flake8`, `pytest`, `gevent`, `eventlet`, `dnspython`, `csle-ryu-fork`, `gpytorch`, `pulp`, `Bayesian optimization`, `emukit`, `cma`, `pycryptodome`, `mitreattack-python`.
- PostgreSQL 12+;
- `make`, `git`, `bzip2`, `build-essential`;
- Prometheus 2.23+;
- Node exporter 1.0.1+;
- cAdvisor (any version);
- Grafana (any version);
- Node v16.13.1+;
- and `npm` v6.14.8+.


### Running the Installation

The network setup for a minimal installation includes (i) a leader server; (ii)
zero or more worker servers; and (iii) a user host, e.g., a laptop or workstation
(see Fig. 26.)

<p align="center">
<img src="./../../img/ansible_installation_setup.png" width="70%">
<p class="captionFig">
Figure 26: Network topology of a typical CSLE installation; the cluster consists of a 
leader and zero or more workers; the installation commands are executed from an 
external user host that runs Ansible; the servers are connected through a private 
network as well as to the Internet; the user host has access to the private network.
</p>
</p>

Start by setting up SSH keys so that a) all servers (leader and workers) have 
SSH access to each other without requiring a password; and b) the user host from which 
the installation will be executed has SSH access to all servers. To do this, start by 
generating an SSH key pair on each host using the command ssh-keygen. 
After generating the keys, copy the public key of each host (e.g., `id_rsa.pub`) 
to the file `.ssh/authorized_keys` on the other hosts.

Next, clone the CSLE git repository on the user host by running the following command.

```bash
git clone https://github.com/Limmen/csle
```

<p class="captionFig">
Listing 5: Commands to clone the CSLE git-repository.
</p>

Now configure the installation by setting the parameters in the files:

- `csle/ansible/inventory`
- `csle/ansible/groups_vars/all/variables.yml`

In most cases the default parameters can be used. However, you must always configure the 
IP addresses of the servers in your cluster in `csle/ansible/inventory`
as well as configure the variables `leader_ip`, `leader_public_ip`, `metastore_ip`,
and cluster_nodes in the file `csle/ansible/groups_vars/all/variables.yml`.

After configuring the installation, install Ansible on the user host by running the command:

```bash
pip install ansible
```

<p class="captionFig">
Listing 6:  Command to install Ansible.
</p>

Finally, start the automated installation by running the following commands on the user host:

```bash
cd csle/ansible; ansible-playbook --ask-become-pass install.yml
```

<p class="captionFig">
Listing 7:   Command to run the automated installation of CSLE with Ansible.
</p>

The above command will ask for a sudo password to the servers. 
After entering the password, Ansible will install all components of CSLE on all
servers in your cluster. This process usually takes around 40 minutes.
