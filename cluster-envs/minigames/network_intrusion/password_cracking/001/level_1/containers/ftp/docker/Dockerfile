# OS
FROM ubuntu:14.04
USER root

# Add start script
ADD docker/start.sh /start.sh
RUN chmod 777 /start.sh

# Add mongo repo
RUN echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list

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
RUN apt-get -y --force-yes install mongodb-org
RUN apt-get -y install default-jdk
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

# Setup FTP
RUN mkdir -p /var/ftp
RUN mv /etc/vsftpd.conf /etc/vsftpd.conf.bak
ADD docker/vsftpd.conf /etc/vsftpd.conf

# Setup Finger
RUN /etc/init.d/inetutils-inetd restart

# Setup Mongo
RUN mkdir -p /data/db

# Setup Tomcat
RUN wget https://archive.apache.org/dist/tomcat/tomcat-8/v8.0.1/bin/apache-tomcat-8.0.1.tar.gz
RUN tar xvzf apache-tomcat-8.0.1.tar.gz
RUN mv apache-tomcat-8.0.1 /usr/local/tomcat
RUN mv /usr/local/tomcat/conf/tomcat-users.xml /usr/local/tomcat/conf/tomcat-users.xml.bak
ADD docker/tomcat-users.xml /usr/local/tomcat/conf/tomcat-users.xml

# Setup TeamSpeak 3 Server
RUN wget https://files.teamspeak-services.com/releases/server/3.12.1/teamspeak3-server_linux_amd64-3.12.1.tar.bz2
RUN tar xvfj teamspeak3-server_linux_amd64-3.12.1.tar.bz2
RUN touch ./teamspeak3-server_linux_amd64/.ts3server_license_accepted

# Setup password-less sudo
RUN mv /etc/sudoers /etc/sudoers.bak
ADD docker/sudoers /etc/sudoers

# CMD to run when container starts, starts the services (e.g. telnet and SSH)
CMD /start.sh

# Hack to keep container running (otherwise K8 thinks task is finished)
#CMD ["sh", "-c", "tail -f /dev/null"]

