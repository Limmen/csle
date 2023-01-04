---
title: Installing CSLE
permalink: /docs/installing/
---

## Installing CSLE

The installation of CSLE can be divided in four main steps (see Fig. 26). 
The first step is "Installation setup", which comprises installation configuration 
and installation of build tools. 
In the second step, the metastore and the simulation system are installed. 
Lastly, in the third and the fourth steps, 
the emulation system and the management system are installed, respectively.

<p align="center">
<img src="./../../img/installation_steps.png" width="70%">
<p class="captionFig">
Figure 26: Steps to install CSLE.
</p>
</p>

### Prerequisites

To install and run CSLE you need at least one server or virtual machine that meets the following criteria:

- Ubuntu 18.04+;
- at least 16GB RAM (the exact amount of RAM necessary depends on the emulations to deploy; 16GB is sufficient for the smallest emulations, e.g. in the size of 5-10 containers);
- at least 2 CPUs;
- 50 GB of free hard-disk space;
- outside Internet access;
- and a UNIX user account with `sudo` privileges.

Below are a list of dependencies that will be installed with CSLE (unless they are already installed):

- Docker 20.10.14+;
- Python 3.9+;
- Python libraries: `torch`, `numpy`, `gym`, `docker`, `paramiko`, `stable-baselines3`, `psycopg`, `pyglet`, `flask`, `click`, `waitress`, `scp`, `psutil`, `grpcio`, `grpcio-tools`, `scipy`, `confluent-kafka`, `requests`, `pyopenssl`, `sphinx`, `mypy`, `flake8`, `pytest`, `gevent`, `eventlet`, `ryu`, `gpytorch`, `pulp`, `Bayesian optimization`.
- PostgreSQL 12+;
- `make`, `git`, `bzip2`;
- Prometheus 2.23+;
- Node exporter 1.0.1+;
- cAdvisor (any version);
- Grafana (any version);
- Node v16.13.1+;
- and `npm` v6.14.8+.

### Installation Setup

In this step of the installation, the source code of CSLE is downloaded, 
configuration parameters are set, and tools required in later steps of the installation are installed.

Start with installing the necessary build tools and version management tools by running the following commands:

```bash
apt install make
apt install git
apt install bzip2
wget https://repo.anaconda.com/archive/Anaconda3-5.0.0-Linux-x86_64.sh
chmod u+rwx Anaconda3-5.0.0-Linux-x86_64.sh
./Anaconda3-5.0.0-Linux-x86_64.sh
```
<p class="captionFig">
Listing 5: Commands to install build tools and version management tools.
</p>

Next, clone the CSLE repository and setup environment variables by running the commands:
```bash
git clone https://github.com/Limmen/clse
export CSLE_HOME=/path/to/csle/ # for bash
set -gx CSLE_HOME "/path/to/csle"  # for fish
```
<p class="captionFig">
Listing 6: Commands to clone the CSLE repository and setup environment variables.
</p>

Further, add the following line to `.bashrc` to set the environment variable `CSLE_HOME` permanently:
```bash
export CSLE_HOME=/path/to/csle/
```
<p class="captionFig">
Listing 7: Line to add to `.bashrc` to set the `CSLE_HOME` environment variable.
</p>

After performing the steps above, you should have the directory layout shown in Fig. 27.

<p align="center">
<img src="./../../img/dir_layout.png" width="70%">
<p class="captionFig">
Figure 27: The directory layout of the CSLE code repository.
</p>
</p>

Next, create a directory to store PID files by running the following commands:
```bash
mkdir /var/log/csle
chmod -R u+rw /var/log/csle
```
<p class="captionFig">
Listing 8: Commands to setup the pid file directory of CSLE.
</p>

Similarly, create a directory to store log files by running the following commands:

```bash
mkdir /tmp/csle
chmod -R u+rw /tmp/csle
```

<p class="captionFig">
Listing 9: mkdir /tmp/csle
chmod -R u+rw /tmp/csle
</p>

Lastly, define default username and password to the management system by editing the file: `csle/config.json`.

### Installing the Metastore
The metastore is based on PostgreSQL and installing the metastore thus corresponds to installing and configuring PostgreSQL.

To install PostgreSQL, run the following commands:

```bash
sudo apt-get install postgresql
sudo apt-get install libpq-dev
```

<p class="captionFig">
Listing 10: Commands to install PostgreSQL.
</p>

Next, setup a password for the `postgres` user by running the commands:

```bash
sudo -u postgres psql  # start psql session
psql> \password postgres # set postgres password
```
<p class="captionFig">
Listing 11: Commands to setup a password for the `postgres` user.
</p>

Next, setup password authentication for the `postgres` user and allow 
remote connections by performing the following steps:

1. Open the file "`/etc/postgresql/<YOUR_VERSION>/main/pg_hba.conf`".
2. Change "`peer`" to "`md5`" on the line that contains "`local all postgres peer`".
3. Add the line: "`host    all             all             0.0.0.0/0            md5  `".
4. Open the file `/etc/postgresql/<YOUR_VERSION>/main/postgresql.conf`.
5. Change "`localhost`" to "`*`" on the line that contains "`listen_addresses = 'localhost'`".
6. Save and close the file.
7. Restart PostgreSQL with the command:

```bash
sudo service postgresql restart
```

<p class="captionFig">
Listing 12: Command to restart PostgreSQL
</p>


After completing the steps above, create the CSLE database and tables by 
running **one** of the commands below:

```bash
sudo psql -U postgres -a -f metastore/create_tables.sql
cd metastore; make build
```

<p class="captionFig">
Listing 13: Commands to create the CSLE database and tables (both commands have the same effect).
</p>

### Installing the Simulation System
The simulation system consists of a set of Python libraries and a set of configuration files.
To install the simulation system, the Python libraries need to be installed and
the configuration files need to be inserted into the metastore.

Start with installing Python 3.9 by running the commands:

```bash
conda create -n py39 python=3.9
source activate python39
```

<p class="captionFig">
Listing 14: Command to install Python 3.9 using Anaconda \cite{anaconda`.
</p>

The simulation system includes 10 Python libraries: 
`csle-collector`, `csle-ryu`, `csle-common`, `csle-attacker`, 
`csle-defender`, `csle-system-identification`, `gym-csle-stopping-game`, 
`csle-agents`, `csle-rest-api`, and `csle-cli`. 
These libraries can either be installed from 
<a href="https://pypi.org/">PyPi</a> or directly from source.

Install `csle-collector` from PyPi by running the command:

```bash
pip install csle-collector
```

<p class="captionFig">
Listing 15: Command to install `csle-collector` from PyPi.
</p>


Alternatively, install `csle-collector` from source by running the commands:

```bash
cd simulation-system/libs/csle-collector/
pip install -e .
cd ../../../
```

<p class="captionFig">
Listing 16: Commands to install `csle-collector` from source.
</p>

Next, install `csle-ryu` from PyPi by running the command:

```bash
pip install csle-ryu
```

<p class="captionFig">
Listing 17: Command to install `csle-ryu` from PyPi.
</p>

Alternatively, install `csle-ryu` from source by running the commands:

```bash
cd simulation-system/libs/csle-ryu/
pip install -e .
cd ../../../
```

<p class="captionFig">
Listing 18: Commands to install `csle-ryu` from source. 
</p>

Next, install `csle-common` from PyPi by running the command:

```bash
pip install csle-common
```

<p class="captionFig">
Listing 19: Command to install `csle-common` from PyPi.
</p>

Alternatively, install `csle-common` from source by running the commands:

```bash
cd simulation-system/libs/csle-common/
pip install -e .
cd ../../../
```

<p class="captionFig">
Listing 20: Commands to install `csle-common` from source.
</p>

Next, install `csle-attacker` from PyPi by running the command:

```bash
pip install csle-attacker
```

<p class="captionFig">
Listing 21: Command to install `csle-attacker` from PyPi.
</p>

Alternatively, install `csle-attacker` from source by running the commands:

```bash
cd simulation-system/libs/csle-attacker/
pip install -e .
cd ../../../
```

<p class="captionFig">
Listing 22: Commands to install `csle-attacker` from source.
</p>

Next, install `csle-defender` from PyPi by running the command:

```bash
pip install csle-defender
```

<p class="captionFig">
Listing 23: Command to install `csle-defender` from PyPi.
</p>

Alternatively, install `csle-defender` from source by running the commands:

```bash
cd simulation-system/libs/csle-defender/
pip install -e .
cd ../../../
```

<p class="captionFig">
Listing 24: Commands to install `csle-defender` from source.
</p>

Next, install `csle-system-identification` from PyPi by running the command:

```bash
pip install csle-system-identification
```
<p class="captionFig">
Listing 25: Command to install `csle-system-identification` from PyPi.
</p>

Alternatively, install `csle-system-identification` from source by running the commands:

```bash
cd simulation-system/libs/csle-system-identification/
pip install -e .
cd ../../../
```

<p class="captionFig">
Listing 26: Commands to install `csle-system-identification` from source.
</p>

Next, install `gym-csle-stopping-game` from PyPi by running the command:

```bash
pip install gym-csle-stopping-game
```

<p class="captionFig">
Listing 27: Command to install `gym-csle-stopping-game` from PyPi.
</p>

Alternatively, install `gym-csle-stopping-game` from source by running the commands:

```bash
cd simulation-system/libs/gym-csle-stopping-game/
pip install -e .
cd ../../../
```

<p class="captionFig">
Listing 28: Commands to install `gym-csle-stopping-game` from source.
</p>

Next, install `csle-agents` from PyPi by running the command:

```bash
Next, install `csle-agents` from PyPi by running the command:
```

<p class="captionFig">
Listing 29: Command to install `csle-agents` from PyPi. 
</p>

Alternatively, install `csle-agents` from source by running the commands:

```bash
cd simulation-system/libs/csle-agents/
pip install -e .
cd ../../../
```

<p class="captionFig">
Listing 30: Commands to install `csle-agents` from source.
</p>

Next, install `csle-rest-api` from PyPi by running the command:

```bash
pip install csle-rest-api
```
<p class="captionFig">
Listing 31: Command to install `csle-rest-api` from PyPi. 
</p>

Alternatively, install `csle-rest-api` from source by running the commands:

```bash
cd simulation-system/libs/csle-rest-api/
pip install -e .
cd ../../../
```

<p class="captionFig">
Listing 32: Commands to install `csle-rest-api` from source.
</p>

Next, install `csle-cli` from PyPi by running the command:
```bash
pip install csle-cli
```
<p class="captionFig">
Listing 33: Command to install `csle-cli` from PyPi.
</p>

Alternatively, install `csle-cli` from source by running the commands:
```bash
cd simulation-system/libs/csle-cli/
pip install -e .
cd ../../../
```
<p class="captionFig">
Listing 34: {Commands to install `csle-cli` from source.
</p>

Finally, insert the simulation configurations into the metastore by running the commands:

```bash
cd simulation-system/envs
make install
cd ../../
```

<p class="captionFig">
Listing 35: Commands to insert simulation configurations into the metastore.
</p>

### Installing the Emulation System
The emulation system consists of a set of configuration files and a set of Docker images, 
which are divided into a set of "base images" and a set of "derived images". 
The base images contain common functionality required by all images in CSLE 
whereas the derived images add specific configurations to the base images, 
e.g. specific vulnerabilities. To install the emulation system, 
the configuration files must be inserted into the metastore and 
the Docker images must be built or downloaded.

Start with adding Docker's official GPG key to Ubuntu's package manager by running the commands:

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
<p class="captionFig">
Listing 36: Commands to add Docker's official GPG key to Ubuntu's package manager.
</p>

Next, install Docker by running the commands:
```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo groupadd docker
sudo usermod -aG docker $USER
```
<p class="captionFig">
Listing 37: Commands to install Docker.
</p>

After completing the Docker installation, pull the base images of CSLE from DockerHub by running the commands:

```bash
cd emulation-system/base_images
make pull
cd ../../
```
<p class="captionFig">
Listing 38: Commands to pull CSLE base images from DockerHub.
</p>

Alternatively, you can build the base images locally (this takes several hours) by running the commands:

```bash
cd emulation-system/base_images
make build
cd ../../
```
<p class="captionFig">
Listing 39: Commands to build CSLE base images.
</p>

Next, pull the derived images of CSLE from DockerHub by running the commands:

```bash
cd emulation-system/derived_images
make pull
cd ../../
```

<p class="captionFig">
Listing 40: Commands to pull CSLE derived images from DockerHub.
</p>

Alternatively, you can build the derived images locally by running the commands:

```bash
cd emulation-system/derived_images
make build
cd ../../
```

<p class="captionFig">
Listing 41: Commands to build CSLE derived images.
</p>

Next, insert the emulation configurations into the metastore by running the commands:

```bash
cd emulation-system/envs
make install
cd ../../
```
<p class="captionFig">
Listing 42: Commands to insert emulation configurations into the metastore.
</p>

Alternatively, you can install the base images, the derived images, and the emulation configurations all at once by running the commands:

```bash
cd emulation-system
make build
cd ../
```

<p class="captionFig">
Listing 43: Commands to install base images, derived images, and emulation environments.
</p>

A few configuration parameters of the kernel need to be updated to be able to execute emulations. 
In particular, the configuration variables `max_map_count` 
and `max_user_watches` need to be updated.

Update `max_map_count` by editing the file `/etc/sysctl.conf` and add the following line:

```bash
vm.max_map_count=262144
```
<p class="captionFig">
Listing 44: Line to add to `/etc/sysctl.conf`.
</p>

Alternatively, for a non-persistent configuration, run the command:

```bash
sysctl -w vm.max_map_count=262144
```

<p class="captionFig">
Listing 45: Command to update the configuration variable `max_map_count`.
</p>


You can check the configuration by running the command:

```bash
sysctl vm.max_map_count
```

<p class="captionFig">
Listing 46: Command to check the configuration of "`max_map_count`".
</p>

Finally, update `max_user_watches` by running the command:

```bash
echo fs.inotify.max_user_watches=524288 | \
     sudo tee -a /etc/sysctl.conf && \
     sudo sysctl -p
```

<p class="captionFig">
Listing 47: Command to set the configuration variable `max_user_watches`.
</p>

### Installing the Management System
The management system consists of monitoring systems 
(i.e. Grafana, Prometheus, Node exporter, and cAdvisor) and the web application 
that implements the web interface, 
which is based on `node.js`. 
Hence, installing the management system corresponds to installing these services and applications.

Start by installing `node.js`, its version manager `nvm`, 
and its package manager `npm` by running the commands:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.2/install.sh | bash # install nvm
nvm -v # Verify nvm installation
nvm install node # Install node
npm install -g npm # Update npm
node -v # Verify version of node
npm -v # Verify version of npm
```

<p class="captionFig">
Listing 48: Commands to install `node.js`, `nvm`, and `npm`.
</p>

If the `nvm` installation failed, manually add the following lines to `.bashrc`:

```bash
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-`" ] && \
       printf %s "${HOME`/.nvm" || \
       printf %s "${XDG_CONFIG_HOME`/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \\
    \. "$NVM_DIR/nvm.sh" # This loads nvm
```

<p class="captionFig">
Listing 49: Commands to setup NVM environment variables.
</p>

Next, configure Nginx by editing the file "`/etc/nginx/sites-available/default`" 
and modify the text string "`location /`" inside the server object 
by adding the following lines:

```bash
location / {
    proxy_pass http://localhost:7777/;
    proxy_buffering off;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-Port $server_port;
`
```

<p class="captionFig">
Listing 50: Lines to add to ```/etc/nginx/sites-available/default`'' to configure Nginx.
</p>

Restart Nginx by running the command:

```bash
sudo service nginx restart
```

<p class="captionFig">
Listing 51: Command to restart Nginx.
</p>

If you have HTTPS enabled on the REST API and have certificates you can configure them 
in Nginx by editing the file "`/etc/nginx/sites-available/default`" as follows:

```bash
server {
     listen 80 default_server;
     listen [::]:80 default_server;
     server_name _;
     return 301 https://$host$request_uri;
 `

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
     `
 `
```

<p class="captionFig">
Listing 52: Contents of the file "`/etc/nginx/sites-available/default`" 
to allow HTTPS traffic to the web interface.
</p>

After completing the steps above, install the web application and 
the monitoring services by running the commands:

```bash
cd management-system
chmod u+x install.sh
./install.sh
```

<p class="captionFig">
Listing 53: Commands to install the management system and associated tools.
</p>

Next, configure IPs of the servers where the management system runs by editing the file:

```bash
csle/management-system/csle-mgmt-webapp/src
    /components/Common/serverIp.js
```

<p class="captionFig">
Listing 54: File to configure the IPs of servers in the management system.
</p>

Next, configure the port of the web interface by editing the file:

```bash
  csle/management-system/csle-mgmt-webapp/src
      /components/Common/serverPort.js
```

<p class="captionFig">
Listing 55: File to configure the port of the web interface.
</p>

To start and stop the monitoring systems using the CSLE CLI, their binaries need to be added to the system path.

Add Prometheus binary to the system path by adding the following line to `.bashrc`:

```bash
export PATH=/path/to/csle/management-system/prometheus/:$PATH
```

<p class="captionFig">
Listing 56: Line to add to `.bashrc` to add Prometheus to the path.
</p>

If you have fish shell instead of bash, add the following line to the configuration file of fish:

```bash
fish_add_path /path/to/csle/management-system/prometheus/
```

<p class="captionFig">
Listing 57: Line to add to the configuration file of fish to add Prometheus to the path.
</p>

Similarly, to add the Node exporter binary to the path, add the following line to `.bashrc`:

```bash
export PATH=/path/to/csle/management-system/node_exporter/:$PATH
```

<p class="captionFig">
Listing 58: Line to add to `.bashrc` to add Node exporter to the path.
</p>

If you have fish shell instead of bash, add the following line to the configuration file of fish:

```bash
fish_add_path /path/to/csle/management-system/node_exporter/
```

<p class="captionFig">
Listing 59: Line to add to the configuration file of fish shell to add Node exporter to the path.
</p>

Finally, setup the management user account with administrator privileges by running the command:

```bash
csle init
```

<p class="captionFig">
Listing 60: Command to setup the management user account with administrator privileges.
</p>
