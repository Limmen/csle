# OS
# Debian 10.2
FROM kimham/csle_cve_2017_7494:0.7.0
USER root

# Install dependencies
RUN apt-get update
RUN echo "postfix postfix/mailname string csle" | debconf-set-selections &&\
        echo "postfix postfix/main_mailer_type string 'Internet Site'" | debconf-set-selections &&\
        apt-get install -y lsb-release apt-utils sudo openssl net-tools iputils-ping emacs curl htop ssh openssh-server \
                       ftp snmpd snmp mailutils inspircd postgresql ntp vsftpd bind9 bind9utils bind9-doc bind9-host \
                       dnsutils git swi-prolog sshpass iptables unzip nmap git telnet xinetd telnetd lftp zip arptables\
                       wget openssl libssl-dev irssi irssi-scripts screen postgresql-client-common \
                       postgresql-client-common snmp postgresql-client smbclient fail2ban rsyslog \
                       netcat traceroute sysstat iproute2 iperf3

# Add users script
ADD docker_files/common/make_root_users.sh /make_root_users.sh
ADD docker_files/common/root_users.txt /root_users.txt
RUN chmod 777 /make_root_users.sh

# setup root users
RUN /make_root_users.sh

# Setup FTP
RUN mkdir -p /var/ftp &&\
    mv /etc/vsftpd.conf /etc/vsftpd.conf.bak
ADD docker_files/common/vsftpd.conf /etc/vsftpd.conf

# Pengine Server
RUN git clone https://github.com/Limmen/erl_pengine

# Setup root SSH
RUN mv /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
ADD docker_files/common/sshd_config_14 /etc/ssh/sshd_config
RUN service ssh start

# Setup password-less sudo
RUN mv /etc/sudoers /etc/sudoers.bak
ADD docker_files/common/sudoers /etc/sudoers

# SecLists
RUN git clone https://github.com/Limmen/SecLists

# NMAP vuln scan
RUN git clone https://github.com/Limmen/vulscan scipag_vulscan &&\
    ln -s `pwd`/scipag_vulscan /usr/share/nmap/scripts/vulscan

# NMAP nmap-vulners
RUN git clone https://github.com/Limmen/nmap-vulners &&\
    cp nmap-vulners/vulners.nse /usr/share/nmap/scripts/ &&\
    nmap --script-updatedb

# Install NMAP manually since the version in jessie repos is too old
#RUN git clone https://github.com/nmap/nmap
#RUN cd nmap && ./configure && make && make install

RUN wget --no-check-certificate https://nmap.org/dist/nmap-7.90.tar.bz2 && tar xvf nmap-7.90.tar.bz2 && cd ./nmap-7.90/ &&\
     ./configure && make && make install

# Setup Tomcat
RUN wget --no-check-certificate https://archive.apache.org/dist/tomcat/tomcat-8/v8.0.1/bin/apache-tomcat-8.0.1.tar.gz &&\
    tar xvzf apache-tomcat-8.0.1.tar.gz &&\
    mv apache-tomcat-8.0.1 /usr/local/tomcat &&\
    mv /usr/local/tomcat/conf/tomcat-users.xml /usr/local/tomcat/conf/tomcat-users.xml.bak
ADD docker_files/common/tomcat-users.xml /usr/local/tomcat/conf/tomcat-users.xml

# Setup TeamSpeak 3 Server
RUN wget --no-check-certificate https://files.teamspeak-services.com/releases/server/3.12.1/teamspeak3-server_linux_amd64-3.12.1.tar.bz2 &&\
    tar xvfj teamspeak3-server_linux_amd64-3.12.1.tar.bz2 &&\
    touch ./teamspeak3-server_linux_amd64/.ts3server_license_accepted

# setup IRC
RUN mv /etc/inspircd/inspircd.conf /etc/inspircd/inspircd.conf.bak
ADD docker_files/common/inspircd.conf /etc/inspircd/inspircd.conf

# Telnet config (disabled by default for security reasons)
ADD docker_files/common/telnet /etc/xinetd.d/telnet
ADD docker_files/common/xinetd.conf /etc/xinetd.conf
RUN chmod 644 /etc/xinetd.d/telnet &&\
    chmod 644 /etc/xinetd.conf

# Conda
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN wget --no-check-certificate \
    https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-py39_4.12.0-Linux-x86_64.sh -b \
    && rm -f Miniconda3-py39_4.12.0-Linux-x86_64.sh

# make non-activate conda commands available
ENV PATH=$CONDA_DIR/bin:$PATH
# make conda activate command available from /bin/bash --login shells
RUN echo ". $CONDA_DIR/etc/profile.d/conda.sh" >> ~/.profile
# make conda activate command available from /bin/bash --interative shells
RUN conda init bash

# Setup Samba
ADD docker_files/common/samba_exploit.py /samba_exploit.py
ADD docker_files/common/bindshell-samba.c /bindshell-samba.c
ADD docker_files/common/bindshell-samba.h /bindshell-samba.h
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
    pip install git+https://github.com/opsxcq/impacket.git &&\
    pip install pyasn1==0.4.8

# Web server HTTP
RUN mkdir -p /web/ &&\
    mkdir -p /web/static
ADD docker_files/common/web_server.py /web/web_server.py
ADD docker_files/common/index.html /web/static/index.html
RUN pip install flask &&\
    pip install waitress

# Setup base environment with csle-collector
SHELL ["conda", "run", "-n", "base", "/bin/bash", "-c"]
RUN pip install flask &&\
    pip install waitress &&\
    pip install csle-collector

# Setup glassfish
RUN wget --no-check-certificate http://download.oracle.com/glassfish/5.0.1/nightly/latest-glassfish.zip &&\
    unzip latest-glassfish.zip

# DWVA WebApp Exploit
ADD docker_files/common/sql_injection_exploit.sh /sql_injection_exploit.sh
RUN chmod 777 /sql_injection_exploit.sh

# CVE-2015-3306 Exploit
ADD docker_files/common/cve_2015_3306_exploit.py /cve_2015_3306_exploit.py
RUN chmod 777 /cve_2015_3306_exploit.py

# CVE-2015-1427 Exploit
ADD docker_files/common/cve_2015_1427_exploit.sh /cve_2015_1427_exploit.sh
RUN chmod 777 /cve_2015_1427_exploit.sh

# CVE-2016-10033 Exploit
ADD docker_files/common/cve_2016_10033_exploit.sh /cve_2016_10033_exploit.sh
RUN chmod 777 /cve_2016_10033_exploit.sh

# CVE-2010-0426 Exploit
ADD docker_files/common/cve_2010_0426_exploit.sh /cve_2010_0426_exploit.sh
RUN chmod 777 /cve_2010_0426_exploit.sh

# CVE-2015-5602 Exploit
ADD docker_files/common/cve_2015_5602_exploit.sh /cve_2015_5602_exploit.sh
RUN chmod 777 /cve_2015_5602_exploit.sh

# IRC Test Login
ADD docker_files/common/irc_login_test.sh /irc_login_test.sh
RUN chmod 777 /irc_login_test.sh

# Pengine Exploit
ADD docker_files/common/pengine_exploit.sh /pengine_exploit.sh
RUN chmod 777 /pengine_exploit.sh

# CVE-2014-0160 Exploit
ADD docker_files/common/heartbleed_exploit.py /heartbleed_exploit.py
RUN chmod 777 /heartbleed_exploit.py

# Setup Sysstat
RUN mv /etc/default/sysstat /etc/default/sysstat.bak
ADD docker_files/common/sysstat /etc/default/sysstat
RUN service sysstat restart

# Client manager
ADD docker_files/common/client_manager.py /client_manager.py
RUN chmod 777 /client_manager.py

# Kafka manager
ADD docker_files/common/kafka_manager.py /kafka_manager.py
RUN chmod 777 /kafka_manager.py

# Snort IDS manager
ADD docker_files/common/snort_ids_manager.py /snort_ids_manager.py
RUN chmod 777 /snort_ids_manager.py

# OSSEC IDS manager
ADD docker_files/common/ossec_ids_manager.py /ossec_ids_manager.py
RUN chmod 777 /ossec_ids_manager.py

# Host manager
ADD docker_files/common/host_manager.py /host_manager.py
RUN chmod 777 /host_manager.py

# ELK manager
ADD docker_files/common/elk_manager.py /elk_manager.py
RUN chmod 777 /elk_manager.py

# Traffic manager
ADD docker_files/common/traffic_manager.py /traffic_manager.py
RUN chmod 777 /traffic_manager.py

# Ryu manager
ADD docker_files/common/ryu_manager.py /ryu_manager.py
RUN chmod 777 /ryu_manager.py

# Beats
RUN curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.3.3-amd64.deb &&\
    dpkg -i filebeat-8.3.3-amd64.deb &&\
    curl -L -O https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-8.3.3-amd64.deb &&\
    dpkg -i metricbeat-8.3.3-amd64.deb &&\
    curl -L -O https://artifacts.elastic.co/downloads/beats/packetbeat/packetbeat-8.3.3-amd64.deb &&\
    dpkg -i packetbeat-8.3.3-amd64.deb &&\
    curl -L -O https://artifacts.elastic.co/downloads/beats/auditbeat/auditbeat-8.3.3-amd64.deb &&\
    dpkg -i auditbeat-8.3.3-amd64.deb &&\
    curl -L -O https://artifacts.elastic.co/downloads/beats/heartbeat/heartbeat-8.3.3-amd64.deb &&\
    dpkg -i heartbeat-8.3.3-amd64.deb

# Add Tini
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]