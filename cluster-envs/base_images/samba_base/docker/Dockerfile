# OS
# Debian GNU/Linux 8 (jessie)
FROM vulnerables/cve-2017-7494
USER root

#RUN echo "deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main" >> /etc/apt/sources.list

# Install dependencies
RUN apt-get update
RUN apt-get -y install lsb-release
RUN apt-get -y install apt-utils
RUN apt-get -y install sudo
RUN apt-get update
RUN apt-get -y install openssl
RUN apt-get -y install net-tools
RUN apt-get -y install iputils-ping
RUN apt-get -y install emacs
RUN apt-get -y install curl
RUN apt-get -y install htop
RUN apt-get -y install ssh
RUN apt-get -y install openssh-server
RUN apt-get -y install ftp
RUN apt-get -y install snmpd
RUN apt-get -y install snmp
RUN echo "postfix postfix/mailname string pwcrack_minigame.pycr" | debconf-set-selections &&\
        echo "postfix postfix/main_mailer_type string 'Internet Site'" | debconf-set-selections &&\
        apt-get install -y mailutils
RUN apt-get -y install inspircd
RUN apt-get -y install postgresql
RUN apt-get -y install ntp
RUN apt-get -y install vsftpd
RUN apt-get -y install bind9
RUN apt-get -y install bind9utils
RUN apt-get -y install bind9-doc
RUN apt-get -y install bind9-host
RUN apt-get -y install dnsutils
RUN apt-get -y install git
RUN apt-get -y install swi-prolog
#RUN apt-get -y install openjdk-8-jdk
RUN apt-get -y install sshpass
RUN apt-get -y install iptables
RUN apt-get -y install unzip
RUN apt-get -y install nmap
RUN apt-get -y install git
RUN apt-get -y install telnet
RUN apt-get -y install xinetd telnetd
RUN apt-get -y install lftp
RUN apt-get -y install zip
#RUN echo "snort snort/address_range string 172.18.1.0/24" | debconf-set-selections &&\
#        apt-get install -y snort
RUN apt-get -y install arptables
RUN apt-get -y install wget

# Add users script
ADD docker/make_root_users.sh /make_root_users.sh
ADD docker/root_users.txt /root_users.txt
RUN chmod 777 /make_root_users.sh

# setup root users
RUN /make_root_users.sh

# Setup FTP
RUN mkdir -p /var/ftp
RUN mv /etc/vsftpd.conf /etc/vsftpd.conf.bak
ADD docker/vsftpd.conf /etc/vsftpd.conf

# Pengine Server
RUN git clone https://github.com/Limmen/erl_pengine

# Cassandra
RUN wget http://apache.mirror.digitalpacific.com.au/cassandra/2.1.22/apache-cassandra-2.1.22-bin.tar.gz
RUN tar xzvf apache-cassandra-2.1.22-bin.tar.gz
RUN mv /apache-cassandra-2.1.22/conf/cassandra.yaml /apache-cassandra-2.1.22/conf/cassandra.yaml.bak
ADD docker/cassandra.yaml /apache-cassandra-2.1.22/conf/cassandra.yaml

# Setup root SSH
RUN mv /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
ADD docker/sshd_config /etc/ssh/sshd_config
RUN service ssh start

# Setup password-less sudo
RUN mv /etc/sudoers /etc/sudoers.bak
ADD docker/sudoers /etc/sudoers

# Setup firewall service on boot
ADD docker/pycr-firewall /etc/init.d/pycr-firewall
RUN chmod 777 /etc/init.d/pycr-firewall

# enable on boot
RUN update-rc.d pycr-firewall defaults

# SecLists
RUN git clone https://github.com/Limmen/SecLists

# NMAP vuln scan
RUN git clone https://github.com/scipag/vulscan scipag_vulscan
RUN ln -s `pwd`/scipag_vulscan /usr/share/nmap/scripts/vulscan

# NMAP nmap-vulners
RUN git clone https://github.com/vulnersCom/nmap-vulners
RUN cp nmap-vulners/vulners.nse /usr/share/nmap/scripts/
RUN nmap --script-updatedb

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

# Cockroach DB
RUN wget https://binaries.cockroachdb.com/cockroach-v20.1.8.linux-amd64.tgz
RUN tar -xvzf cockroach-v20.1.8.linux-amd64.tgz

## setup Kafka
#RUN wget http://www-us.apache.org/dist/kafka/2.4.0/kafka_2.13-2.4.0.tgz
#RUN tar xzf kafka_2.13-2.4.0.tgz
#RUN mv kafka_2.13-2.4.0 /usr/local/kafka

# setup SNMP
RUN mv /etc/snmp/snmpd.conf /etc/snmp/snmpd.conf.backup
ADD docker/snmpd.conf /etc/snmp/snmpd.conf
RUN service snmpd restart

# setup IRC
RUN mv /etc/inspircd/inspircd.conf /etc/inspircd/inspircd.conf.bak
ADD docker/inspircd.conf /etc/inspircd/inspircd.conf

## setup Postgres
#RUN mv /etc/postgresql/12/main/postgresql.conf /etc/postgresql/12/main/postgresql.conf.bak
#ADD docker/postgresql.conf /etc/postgresql/12/main/postgresql.conf

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

# Setup Samba
ADD docker/exploit.py /exploit.py
ADD docker/bindshell-samba.c /bindshell-samba.c
ADD docker/bindshell-samba.h /bindshell-samba.h
RUN gcc -c -fpic bindshell-samba.c
RUN gcc -shared -o libbindshell-samba.so bindshell-samba.o
RUN chmod 777 /exploit.py
RUN chmod 777 /bindshell-samba.c
RUN chmod 777 /bindshell-samba.h
RUN chmod 777 /libbindshell-samba.so
RUN chmod 777 /bindshell-samba.o
RUN conda create --name samba python=2.7 -y
# Make subsequent RUN commands use the samba env
SHELL ["conda", "run", "-n", "samba", "/bin/bash", "-c"]
#RUN conda activate samba
RUN pip install pycrypto==2.6
RUN pip install git+git://github.com/opsxcq/impacket.git
RUN pip install pyasn1

# Web server HTTP
RUN mkdir -p /web/
RUN mkdir -p /web/static
ADD docker/web_server.py /web/web_server.py
ADD docker/index.html /web/static/index.html
RUN pip install flask
RUN pip install waitress

# Setup glassfish
RUN wget http://download.oracle.com/glassfish/5.0.1/nightly/latest-glassfish.zip
RUN unzip latest-glassfish.zip

# Setup Snort
#RUN wget https://www.snort.org/downloads/community/community-rules.tar.gz -O community-rules.tar.gz
#RUN tar -xvzf community-rules.tar.gz -C /etc/snort/rules
#RUN mkdir /var/snort
#RUN chmod 777 /var/snort
#RUN mv /etc/snort/snort.conf /etc/snort/snort.conf.bak
#ADD docker/snort.conf /etc/snort/snort.conf

