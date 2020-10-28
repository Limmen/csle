# OS
FROM ubuntu:20.04
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
RUN apt-get -y install xinetd telnetd
RUN apt-get -y install ssh
RUN apt-get -y install openssh-server
RUN apt-get -y install ftp
RUN apt-get -y install sshpass
RUN apt-get -y install iptables
RUN apt-get -y install unzip
RUN apt-get -y install nmap
RUN apt-get -y install git

# Setup users

# Add users script
ADD docker/make_root_users.sh /make_root_users.sh
ADD docker/make_non_root_users.sh /make_non_root_users.sh
ADD docker/root_users.txt /root_users.txt
ADD docker/non_root_users.txt /non_root_users.txt
RUN chmod 777 /make_root_users.sh
RUN chmod 777 /make_non_root_users.sh

# setup root users
RUN /make_root_users.sh

# setup non-root users
RUN /make_non_root_users.sh

# Create flag
ADD docker/create_flag.sh /create_flag.sh
ADD docker/fl_info.txt /fl_info.txt
RUN chmod 777 /create_flag.sh
RUN /create_flag.sh

# setup firewall
ADD docker/setup_firewall.sh /setup_firewall.sh
RUN chmod 777 /setup_firewall.sh

# SSH
RUN service ssh start

# Telnet config (disabled by default for security reasons)
ADD docker/telnet /etc/xinetd.d/telnet
ADD docker/xinetd.conf /etc/xinetd.conf
RUN chmod 644 /etc/xinetd.d/telnet
RUN chmod 644 /etc/xinetd.conf

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

# Web server HTTP
RUN mkdir -p /web/
RUN mkdir -p /web/static
ADD docker/web_server.py /web/web_server.py
ADD docker/index.html /web/static/index.html
RUN pip install flask
RUN pip install waitress

# Setup firewall service on boot
ADD docker/pycr-firewall /etc/init.d/pycr-firewall
RUN chmod 777 /etc/init.d/pycr-firewall
# enable on boot
RUN update-rc.d pycr-firewall defaults

# Add start script
ADD docker/start.sh /start.sh
RUN chmod 777 /start.sh

# Setup root SSH
RUN mv /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
ADD docker/sshd_config /etc/ssh/sshd_config

# SecLists
RUN git clone https://github.com/danielmiessler/SecLists

# NMAP vuln scan
RUN git clone https://github.com/scipag/vulscan scipag_vulscan
RUN ln -s `pwd`/scipag_vulscan /usr/share/nmap/scripts/vulscan

# NMAP nmap-vulners
RUN git clone https://github.com/vulnersCom/nmap-vulners
RUN cp nmap-vulners/vulners.nse /usr/share/nmap/scripts/
RUN nmap --script-updatedb

# Setup password-less sudo
RUN mv /etc/sudoers /etc/sudoers.bak
ADD docker/sudoers /etc/sudoers

# CMD to run when container starts, starts the services (e.g. telnet and SSH)
CMD /start.sh

# Hack to keep container running (otherwise K8 thinks task is finished)
#CMD ["sh", "-c", "tail -f /dev/null"]
