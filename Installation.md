# Installation 

Follow the instructions below to install CSLE.

## Requirements
Ubuntu server
TODO

## Install from source

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

- Setup your configuration (e.g define default username and passwords for the management system) by editing the config file `csle/config.json`

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

    - Install `csle-collector` (see ([README](simulation-system/python/csle-collector/README.md)) for more information)
      ```bash
       cd simulation-system/python/csle-collector/
       pip install -e . 
       cd ../../../
      ```

    - Install `csle-common` (see ([README](simulation-system/python/csle-common/README.md)) for more information)
      ```bash
       cd simulation-system/python/csle-common/
       pip install -e .
       cd ../../../
      ```

    - Install `csle-attacker` (see ([README](simulation-system/python/csle-attacker/README.md)) for more information)
      ```bash
      cd simulation-system/python/csle-attacker/
      pip install -e . 
      cd ../../../
      ```

    - Install `csle-defender` (see ([README](simulation-system/python/csle-defender/README.md)) for more information)
      ```bash
      cd simulation-system/python/csle-defender/
      pip install -e .
      cd ../../../
      ```

    - Install `gym-csle-stopping-game` (see ([README](simulation-system/python/gym-csle-stopping-game/README.MD)) for more
      information)
      ```bash
      cd simulation-system/python/gym-csle-stopping-game/
      pip install -e .
      cd ../../../
      ```

    - Install `csle-system-identification` (see ([README](simulation-system/python/csle-system-identification/README.MD)) for more
      information)
      ```bash
      cd simulation-system/python/csle-system-identification/
      pip install -e .
      cd ../../../
      ```

    - Install `csle-agents` (see ([README](simulation-system/python/csle-agents/README.MD)) for more
      information)
      ```bash
      cd simulation-system/python/csle-agents/
      pip install -e .
      cd ../../../
      ```

    - Install `csle-ryu` (see ([README](simulation-system/python/csle-ryu/README.MD)) for more
      information)
      ```bash
      cd simulation-system/python/csle-ryu/
      pip install -e .
      cd ../../../
      ```

    - Install `csle-rest-api` (see ([README](simulation-system/python/csle-rest-api/README.MD)) for more
      information)
      ```bash
      cd simulation-system/python/csle-rest-api/
      pip install -e .
      cd ../../../
      ```

    - Install `csle-cli` (see ([README](simulation-system/python/csle-cli/README.MD)) for more
      information)
      ```bash
      cd simulation-system/python/csle-cli/
      pip install -e .
      cd ../../../
      ```

    - Install simulation envs (see [README](simulation-system/envs/README.MD) for more information)
      ```bash
      cd simulation-system/envs
      make install
      cd ../../
      ```

8. **Initialize management users** 
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
    - Install base images (see ([README](emulation-system/base_images/README.MD)) for more information) 
      To install the base images you have two options: (1) pull the images from DockerHub; or (2), build the images locally.
      To build the images locally, run (this may take a while, e.g. an hour):
      ```bash
      cd emulation-system/base_images
      make build
      cd ../../
      ```     
      To pull the images from DockerHub, run:
      ```bash
      cd emulation-system/base_images
      make pull
      cd ../../
      ```

    - Install derived images (see ([README](emulation-system/derived_images/README.MD)) for more information)
      To install the derived images you have two options: (1) pull the images from DockerHub; or (2), build the images locally.
      To build the images locally, run (this may take a while, e.g. an hour):
      ```bash
      cd emulation-system/derived_images
      make build
      cd ../../
      ```
      To pull the images from DockerHub, run:
      ```bash
      cd emulation-system/derived_images
      make pull
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
    - Set `max_map_count`. Add the line
      ```bash
      vm.max_map_count=262144
      ```
      to the file `/etc/sysctl.conf` (you can also set a higher value).
      Alternatively, for a non-persisten configuration, run:
      ```bash
       sysctl -w vm.max_map_count=262144
      ```
      You can check the configuration by running:
      ```bash
      sysctl vm.max_map_count
      ```
    - Set `max_user_watches`. Run:
       ```bash
       echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p
       ```     

10. **Install the management system**
    - To build the webapp used in the management system and in the policy examination system you need node.js and npm
      installed, to install node and npm execute:
       ```bash
       curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.2/install.sh | bash # install nvm
       nvm -v # Verify nvm installation
       nvm install node # Install node
       npm install -g npm # Update npm
       node -v # Verify version of node
       npm -v # Verify version of npm
       ```
      If the nvm installation failed, manually add the following lines to `.bashrc`:
     ```bash
    export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
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
    - Install the management system and associated tools:
     ```bash
       cd management-system
       chmod u+x install.sh
       ./install.sh
     ```
    - Configure the IP of the server where the management system runs by editing the file:
      ```bash
       csle/management-system/csle-mgmt-webapp/src/components/Common/serverIp.js
      ```
    - Configure the Port of the server where the management system runs by editing the file:
      ```bash
       csle/management-system/csle-mgmt-webapp/src/components/Common/serverPort.js
      ```
    - Add prometheus binary to the path
      ```bash
       export PATH=/path/to/csle/management-system/prometheus/:$PATH
       ```
      or for fish shell:
      ```bash
       fish_add_path /path/to/csle/management-system/prometheus/
       ```
    To have the binary permanently in $PATH, add the following line to the
    .bashrc: `export PATH=/path/to/csle/management-system/prometheus/:$PATH`
    - Add node_exporter binary to the path
      ```bash
       export PATH=/path/to/csle/management-system/node_exporter/:$PATH
       ```
      or for fish shell:
      ```bash
       fish_add_path /path/to/csle/management-system/node_exporter/
       ```
    To have the binary permanently in $PATH, add the following line to the
    .bashrc: `export PATH=/path/to/csle/management-system/node_exporter/:$PATH`
    - Run the management system (for more instructions see [README](management system/README.MD)):
     ```bash
       cd management-system
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