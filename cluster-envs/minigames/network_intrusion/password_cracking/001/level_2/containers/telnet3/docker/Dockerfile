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
RUN apt-get -y install postgresql
RUN apt-get -y install openjdk-8-jdk
RUN apt-get -y install unzip
RUN apt-get -y install iptables

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

# setup firewall
ADD docker/setup_firewall.sh /setup_firewall.sh
RUN chmod 777 /setup_firewall.sh

# Telnet config (disabled by default for security reasons)
ADD docker/telnet /etc/xinetd.d/telnet
ADD docker/xinetd.conf /etc/xinetd.conf
RUN chmod 644 /etc/xinetd.d/telnet
RUN chmod 644 /etc/xinetd.conf

# setup Postgres
RUN mv /etc/postgresql/12/main/postgresql.conf /etc/postgresql/12/main/postgresql.conf.bak
ADD docker/postgresql.conf /etc/postgresql/12/main/postgresql.conf
RUN service postgresql restart

# Setup glassfish
RUN wget http://download.oracle.com/glassfish/5.0.1/nightly/latest-glassfish.zip
RUN unzip latest-glassfish.zip
#RUN ./*glassfish*/bin/asadmin create-domain --nopassword --adminport 4848 domain2

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

# CMD to run when container starts, starts the services (e.g. telnet and SSH)
CMD /start.sh

# Setup password-less sudo
RUN mv /etc/sudoers /etc/sudoers.bak
ADD docker/sudoers /etc/sudoers

# Hack to keep container running (otherwise K8 thinks task is finished)
#CMD ["sh", "-c", "tail -f /dev/null"]
