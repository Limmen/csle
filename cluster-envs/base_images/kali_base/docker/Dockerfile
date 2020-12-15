# OS
FROM kalilinux/kali-rolling
USER root

# Install dependencies
RUN apt-get update
RUN apt-get -y install apt-utils
RUN apt-get -y install openssl
RUN apt-get -y install net-tools
RUN apt-get -y install iputils-ping
RUN apt-get -y install sudo
RUN apt-get -y install emacs
RUN apt-get -y install curl
RUN apt-get -y install htop
RUN apt-get -y install telnet
RUN apt-get -y install ssh
RUN apt-get -y install openssh-server
RUN apt-get -y install ftp
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y kali-tools-top10
#RUN apt-get -y install man-db
RUN apt-get -y install exploitdb
RUN apt-get -y install nikto
RUN apt-get -y install traceroute
RUN apt-get -y install finger
RUN apt-get -y install git
RUN apt-get -y install sshpass
RUN apt-get -y install lftp
RUN apt-get -y install recon-ng
RUN apt-get -y install netdiscover
RUN apt-get -y install hping3
RUN apt-get -y install netcat
RUN apt-get -y install masscan
RUN apt-get -y install iptables
RUN apt-get -y install proxychains
RUN apt-get -y install zip
RUN apt-get -y install unzip
RUN apt-get -y install arptables

# Setup users

# Add users script
ADD docker/make_root_users.sh /make_root_users.sh
ADD docker/root_users.txt /root_users.txt
RUN chmod 777 /make_root_users.sh

# setup root users
RUN /make_root_users.sh

# SSH
RUN service ssh start

# NMAP vuln scan
RUN git clone https://github.com/scipag/vulscan scipag_vulscan
RUN ln -s `pwd`/scipag_vulscan /usr/share/nmap/scripts/vulscan

# NMAP nmap-vulners
RUN git clone https://github.com/vulnersCom/nmap-vulners
RUN cp nmap-vulners/vulners.nse /usr/share/nmap/scripts/
RUN nmap --script-updatedb

# SecLists
RUN git clone https://github.com/Limmen/SecLists

# Alias
RUN echo "alias ll='ls -al'" >> /root.bashrc

# Setup root passwd
RUN echo "root:root" | /usr/sbin/chpasswd

# Setup root SSH
RUN mv /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
ADD docker/sshd_config /etc/ssh/sshd_config

# Setup password-less sudo
RUN mv /etc/sudoers /etc/sudoers.bak
ADD docker/sudoers /etc/sudoers

# Download nmap-services
RUN wget https://raw.githubusercontent.com/nmap/nmap/master/nmap-services

# Download CVEs
RUN wget https://cve.mitre.org/data/downloads/allitems.csv

# Conda
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh

# make non-activate conda commands available
ENV PATH=$CONDA_DIR/bin:$PATH
# make conda activate command available from /bin/bash --login shells
RUN echo ". $CONDA_DIR/etc/profile.d/conda.sh" >> ~/.profile
# make conda activate command available from /bin/bash --interative shells
RUN conda init bash

# Prep CVEs
ADD docker/cve_prep.py /cve_prep.py
RUN python /cve_prep.py

# Setup firewall service on boot
ADD docker/pycr-firewall /etc/init.d/pycr-firewall
RUN chmod 777 /etc/init.d/pycr-firewall

# enable on boot
RUN update-rc.d pycr-firewall defaults
