# OS
FROM ubuntu:20.04
USER root

# Add start script
ADD docker/start.sh /start.sh
RUN chmod 777 /start.sh

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
RUN apt-get -y install bind9
RUN apt-get -y install bind9utils
RUN apt-get -y install bind9-doc
RUN apt-get -y install bind9-host
RUN apt-get -y install dnsutils
RUN apt-get -y install git
RUN apt-get -y install swi-prolog
RUN apt-get -y install openjdk-8-jdk
RUN apt-get -y install sshpass
RUN apt-get -y install ntp
RUN apt-get -y install inspircd
RUN apt-get -y install gnupg
RUN apt-get -y install ca-certificates
#RUN /bin/bash -c "source /etc/lsb-release && echo 'deb https://download.rethinkdb.com/repository/ubuntu-$DISTRIB_CODENAME $DISTRIB_CODENAME main' | sudo tee /etc/apt/sources.list.d/rethinkdb.list"
RUN /bin/bash -c "source /etc/lsb-release && echo 'deb https://download.rethinkdb.com/repository/ubuntu-focal focal main' | sudo tee /etc/apt/sources.list.d/rethinkdb.list"
RUN wget -qO- https://download.rethinkdb.com/repository/raw/pubkey.gpg | sudo apt-key add -
RUN apt-get update
RUN apt-get -y install rethinkdb

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

# SSH
RUN service ssh start

# setup IRC
RUN mv /etc/inspircd/inspircd.conf /etc/inspircd/inspircd.conf.bak
ADD docker/inspircd.conf /etc/inspircd/inspircd.conf

# Setup root SSH
RUN mv /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
ADD docker/sshd_config /etc/ssh/sshd_config

# Setup password-less sudo
RUN mv /etc/sudoers /etc/sudoers.bak
ADD docker/sudoers /etc/sudoers

# CMD to run when container starts, starts the services (e.g. telnet and SSH)
CMD /start.sh

# Hack to keep container running (otherwise K8 thinks task is finished)
#CMD ["sh", "-c", "tail -f /dev/null"]
