# OS
# Debian GNU/Linux 8 (jessie)
FROM vulnerables/cve-2017-7494
USER root

#RUN echo "deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main" >> /etc/apt/sources.list

# Install dependencies
RUN apt-get update
RUN echo "postfix postfix/mailname string pwcrack_minigame.pycr" | debconf-set-selections &&\
        echo "postfix postfix/main_mailer_type string 'Internet Site'" | debconf-set-selections &&\
        apt-get install -y lsb-release apt-utils sudo openssl net-tools iputils-ping emacs curl htop ssh openssh-server \
                       ftp snmpd snmp mailutils inspircd postgresql ntp vsftpd bind9 bind9utils bind9-doc bind9-host \
                       dnsutils git swi-prolog sshpass iptables unzip nmap git telnet xinetd telnetd lftp zip arptables\
                       wget
#RUN apt-get -y install openjdk-8-jdk
#RUN echo "snort snort/address_range string 172.18.1.0/24" | debconf-set-selections &&\
#        apt-get install -y snort

# Add users script
ADD docker/make_root_users.sh /make_root_users.sh
ADD docker/root_users.txt /root_users.txt
RUN chmod 777 /make_root_users.sh

# setup root users
RUN /make_root_users.sh

# Setup FTP
RUN mkdir -p /var/ftp &&\
    mv /etc/vsftpd.conf /etc/vsftpd.conf.bak
ADD docker/vsftpd.conf /etc/vsftpd.conf

# Pengine Server
RUN git clone https://github.com/Limmen/erl_pengine

# Cassandra
RUN wget http://apache.mirror.digitalpacific.com.au/cassandra/2.1.22/apache-cassandra-2.1.22-bin.tar.gz &&\
    tar xzvf apache-cassandra-2.1.22-bin.tar.gz &&\
    mv /apache-cassandra-2.1.22/conf/cassandra.yaml /apache-cassandra-2.1.22/conf/cassandra.yaml.bak
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
RUN git clone https://github.com/scipag/vulscan scipag_vulscan &&\
    ln -s `pwd`/scipag_vulscan /usr/share/nmap/scripts/vulscan

# NMAP nmap-vulners
RUN git clone https://github.com/vulnersCom/nmap-vulners &&\
    cp nmap-vulners/vulners.nse /usr/share/nmap/scripts/ &&\
    nmap --script-updatedb

# Setup Tomcat
RUN wget https://archive.apache.org/dist/tomcat/tomcat-8/v8.0.1/bin/apache-tomcat-8.0.1.tar.gz &&\
    tar xvzf apache-tomcat-8.0.1.tar.gz &&\
    mv apache-tomcat-8.0.1 /usr/local/tomcat &&\
    mv /usr/local/tomcat/conf/tomcat-users.xml /usr/local/tomcat/conf/tomcat-users.xml.bak
ADD docker/tomcat-users.xml /usr/local/tomcat/conf/tomcat-users.xml

# Setup TeamSpeak 3 Server
RUN wget https://files.teamspeak-services.com/releases/server/3.12.1/teamspeak3-server_linux_amd64-3.12.1.tar.bz2 &&\
    tar xvfj teamspeak3-server_linux_amd64-3.12.1.tar.bz2 &&\
    touch ./teamspeak3-server_linux_amd64/.ts3server_license_accepted

# Cockroach DB
RUN wget https://binaries.cockroachdb.com/cockroach-v20.1.8.linux-amd64.tgz &&\
    tar -xvzf cockroach-v20.1.8.linux-amd64.tgz

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
RUN chmod 644 /etc/xinetd.d/telnet &&\
    chmod 644 /etc/xinetd.conf

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
ADD docker/samba_exploit.py /samba_exploit.py
ADD docker/bindshell-samba.c /bindshell-samba.c
ADD docker/bindshell-samba.h /bindshell-samba.h
RUN gcc -c -fpic bindshell-samba.c &&\
    gcc -shared -o libbindshell-samba.so bindshell-samba.o &&\
    chmod 777 /samba_exploit.py &&\
    chmod 777 /bindshell-samba.c &&\
    chmod 777 /bindshell-samba.h &&\
    chmod 777 /libbindshell-samba.so &&\
    chmod 777 /bindshell-samba.o &&\
    chmod -R 777 /data &&\
    conda create --name samba python=2.7 -y
# Make subsequent RUN commands use the samba env
SHELL ["conda", "run", "-n", "samba", "/bin/bash", "-c"]
#RUN conda activate samba
RUN pip install pycrypto==2.6 &&\
    pip install git+git://github.com/opsxcq/impacket.git &&\
    pip install pyasn1

# Web server HTTP
RUN mkdir -p /web/ &&\
    mkdir -p /web/static
ADD docker/web_server.py /web/web_server.py
ADD docker/index.html /web/static/index.html
RUN pip install flask &&\
    pip install waitress

# Setup glassfish
RUN wget http://download.oracle.com/glassfish/5.0.1/nightly/latest-glassfish.zip &&\
    unzip latest-glassfish.zip

# DWVA WebApp Exploit
ADD docker/sql_injection_exploit.sh /sql_injection_exploit.sh
RUN chmod 777 /sql_injection_exploit.sh

# CVE-2015-3306 Exploit
ADD docker/cve_2015_3306_exploit.py /cve_2015_3306_exploit.py
RUN chmod 777 /cve_2015_3306_exploit.py

# Setup Snort
#RUN wget https://www.snort.org/downloads/community/community-rules.tar.gz -O community-rules.tar.gz
#RUN tar -xvzf community-rules.tar.gz -C /etc/snort/rules
#RUN mkdir /var/snort
#RUN chmod 777 /var/snort
#RUN mv /etc/snort/snort.conf /etc/snort/snort.conf.bak
#ADD docker/snort.conf /etc/snort/snort.conf

