# OS
# Debian GNU/Linux 8 (wheezy)
FROM debian/eol:wheezy
USER root

# Setup wheezy packet repos
RUN echo 'deb http://archive.debian.org/debian wheezy-backports main' > /etc/apt/sources.list.d/wheezy-backports.list &&\
    sed -i '/wheezy-updates/d' /etc/apt/sources.list &&\
    echo "deb [check-valid-until=no] http://archive.debian.org/debian/ wheezy-backports main" >> /etc/apt/sources.list &&\
    apt-get -o Acquire::Check-Valid-Until=false update

# Install dependencies
RUN apt-get update
RUN echo "postfix postfix/mailname string csle" | debconf-set-selections &&\
        echo "postfix postfix/main_mailer_type string 'Internet Site'" | debconf-set-selections &&\
        DEBIAN_FRONTEND=noninteractive apt-get install -y lsb-release apt-utils sudo openssl net-tools iputils-ping \
        emacs curl htop ssh openssh-server build-essential \
        ftp snmpd snmp mailutils inspircd postgresql ntp vsftpd bind9 bind9utils bind9-doc bind9-host \
        dnsutils git swi-prolog sshpass iptables unzip nmap git telnet xinetd telnetd lftp zip arptables\
        wget apache2 irssi irssi-scripts screen openssh-server snmp mongodb-clients postgresql-client smbclient \
        fail2ban rsyslog netcat traceroute sysstat iproute2

RUN apt-get install -y openssl libssl-dev -t wheezy-backports

# Add users script
ADD docker_files/common/make_root_users.sh /make_root_users.sh
ADD docker_files/common/root_users.txt /root_users.txt
RUN chmod 777 /make_root_users.sh

# setup root users
RUN /make_root_users.sh

# Apache2 Shellshock setup
ADD docker_files/shellshock_debian_wheezy_base/docker/packages /packages
RUN dpkg -i /packages/*
ADD docker_files/shellshock_debian_wheezy_base/docker/vulnerable /usr/lib/cgi-bin/
ADD docker_files/shellshock_debian_wheezy_base/docker/index.html /var/www
RUN chown www-data:www-data /var/www/index.html
ADD docker_files/shellshock_debian_wheezy_base/docker/main.sh /main.sh
RUN mv /etc/apache2/envvars /etc/apache2/envvars.backup
ADD docker_files/common/apache_envvars /etc/apache2/envvars
RUN chown -R csle_admin:root /run &&\
    chmod -R 777 /var &&\
    chown -R csle_admin:root /var

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

## Install NMAP manually since the version in wheezy repos is too old
RUN wget --no-check-certificate https://nmap.org/dist/nmap-7.90.tar.bz2 && tar xvf nmap-7.90.tar.bz2 && cd ./nmap-7.90/ &&\
     ./configure && make && make install

# setup SNMP
RUN mv /etc/snmp/snmpd.conf /etc/snmp/snmpd.conf.backup
ADD docker_files/common/snmpd.conf /etc/snmp/snmpd.conf
RUN service snmpd restart

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
    https://repo.anaconda.com/miniconda/Miniconda3-4.7.12.1-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-4.7.12.1-Linux-x86_64.sh -b \
    && rm -f Miniconda3-4.7.12.1-Linux-x86_64.sh

# make non-activate conda commands available
ENV PATH=$CONDA_DIR/bin:$PATH
# make conda activate command available from /bin/bash --login shells
RUN echo ". $CONDA_DIR/etc/profile.d/conda.sh" >> ~/.profile
# make conda activate command available from /bin/bash --interative shells
RUN conda init bash

# DWVA WebApp Exploit
ADD docker_files/common/sql_injection_exploit.sh /sql_injection_exploit.sh
RUN chmod 777 /sql_injection_exploit.sh

## Setup Samba
ADD docker_files/common/samba_exploit.py /samba_exploit.py
ADD docker_files/common/bindshell-samba.c /bindshell-samba.c
ADD docker_files/common/bindshell-samba.h /bindshell-samba.h
RUN gcc -c -fpic bindshell-samba.c &&\
    gcc -shared -o libbindshell-samba.so bindshell-samba.o &&\
    chmod 777 /samba_exploit.py &&\
    chmod 777 /bindshell-samba.c &&\
    chmod 777 /bindshell-samba.h &&\
    chmod 777 /libbindshell-samba.so &&\
    conda create --clone base --name samba -y

# TODO Solve this
# Make subsequent RUN commands use the samba env
SHELL ["conda", "run", "-n", "samba", "/bin/bash", "-c"]

## Install pycrypto, pyasn and impacket
RUN pip install pycrypto==2.6 &&\
    pip install git+https://github.com/Limmen/impacket.git &&\
    pip install pyasn1==0.4.8

# Setup base environment with csle-collector
SHELL ["conda", "run", "-n", "base", "/bin/bash", "-c"]
RUN pip install flask &&\
    pip install waitress
#    pip install csle-collector

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

# Setup Sysstat
RUN mv /etc/default/sysstat /etc/default/sysstat.bak
ADD docker_files/common/sysstat /etc/default/sysstat
RUN service sysstat restart

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