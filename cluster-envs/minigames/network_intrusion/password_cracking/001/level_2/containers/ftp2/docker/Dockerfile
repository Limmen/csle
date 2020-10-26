# OS
FROM ubuntu:14.04
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
#RUN apt-get -y install htop
RUN apt-get -y install telnet
RUN apt-get -y install xinetd telnetd
RUN apt-get -y install ssh
RUN apt-get -y install openssh-server
RUN apt-get -y install ftp
RUN apt-get -y install vsftpd
RUN apt-get -y install inetutils-inetd fingerd
RUN apt-get -y install default-jdk
RUN apt-get -y install sshpass
RUN apt-get -y install inspircd
RUN apt-get -y install default-jdk
RUN apt-get -y install wget
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

# Create flag
ADD docker/create_flag.sh /create_flag.sh
ADD docker/fl_info.txt /fl_info.txt
RUN chmod 777 /create_flag.sh
RUN /create_flag.sh

# setup firewall
ADD docker/setup_firewall.sh /setup_firewall.sh
RUN chmod 777 /setup_firewall.sh

# Setup FTP
RUN mkdir -p /var/ftp
RUN mv /etc/vsftpd.conf /etc/vsftpd.conf.bak
ADD docker/vsftpd.conf /etc/vsftpd.conf

# Setup Finger
RUN /etc/init.d/inetutils-inetd restart

# Cockroach DB
RUN wget https://binaries.cockroachdb.com/cockroach-v20.1.8.linux-amd64.tgz
RUN tar -xvzf cockroach-v20.1.8.linux-amd64.tgz

# setup Kafka
RUN wget http://www-us.apache.org/dist/kafka/2.4.0/kafka_2.13-2.4.0.tgz
RUN tar xzf kafka_2.13-2.4.0.tgz
RUN mv kafka_2.13-2.4.0 /usr/local/kafka

# Setup password-less sudo
RUN mv /etc/sudoers /etc/sudoers.bak
ADD docker/sudoers /etc/sudoers

# Setup firewall service on boot
ADD docker/pycr-firewall /etc/init.d/pycr-firewall
RUN chmod 777 /etc/init.d/pycr-firewall
# enable on boot
RUN update-rc.d pycr-firewall defaults

# CMD to run when container starts, starts the services (e.g. telnet and SSH)
CMD /start.sh

# Hack to keep container running (otherwise K8 thinks task is finished)
#CMD ["sh", "-c", "tail -f /dev/null"]

