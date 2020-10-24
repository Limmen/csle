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
RUN apt-get -y install sshpass

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

# Setup password-less sudo
RUN mv /etc/sudoers /etc/sudoers.bak
ADD docker/sudoers /etc/sudoers

# CMD to run when container starts, starts the services (e.g. telnet and SSH)
#CMD /start.sh

# Hack to keep container running (otherwise K8 thinks task is finished)
#CMD ["sh", "-c", "tail -f /dev/null"]
