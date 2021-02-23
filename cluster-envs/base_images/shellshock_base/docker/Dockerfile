# OS
# Debian GNU/Linux 8 (wheezy)
FROM debian/eol:wheezy
USER root

RUN apt-get update

RUN echo "postfix postfix/mailname string pwcrack_minigame.pycr" | debconf-set-selections &&\
        echo "postfix postfix/main_mailer_type string 'Internet Site'" | debconf-set-selections &&\
        DEBIAN_FRONTEND=noninteractive apt-get install -y lsb-release apt-utils sudo openssl net-tools iputils-ping \
        emacs curl htop ssh openssh-server build-essential \
        ftp snmpd snmp mailutils inspircd postgresql ntp vsftpd bind9 bind9utils bind9-doc bind9-host \
        dnsutils git swi-prolog sshpass iptables unzip nmap git telnet xinetd telnetd lftp zip arptables\
        wget apache2 &&\
        apt-get clean &&\
        rm -rf /var/lib/apt/lists/*

# Add users script
ADD docker/make_root_users.sh /make_root_users.sh
ADD docker/root_users.txt /root_users.txt
RUN chmod 777 /make_root_users.sh

# setup root users
RUN /make_root_users.sh

# Apache2 Shellshock setup
ADD docker/packages /packages
RUN dpkg -i /packages/*
ADD docker/vulnerable /usr/lib/cgi-bin/
ADD docker/index.html /var/www
RUN chown www-data:www-data /var/www/index.html
ADD docker/main.sh /main.sh
RUN mv /etc/apache2/envvars /etc/apache2/envvars.backup
ADD docker/apache_envvars /etc/apache2/envvars
RUN chown -R pycr_admin:root /run &&\
    chmod -R 777 /var &&\
    chown -R pycr_admin:root /var

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

# Cockroach DB
RUN wget https://binaries.cockroachdb.com/cockroach-v20.1.8.linux-amd64.tgz &&\
    tar -xvzf cockroach-v20.1.8.linux-amd64.tgz

# setup SNMP
RUN mv /etc/snmp/snmpd.conf /etc/snmp/snmpd.conf.backup
ADD docker/snmpd.conf /etc/snmp/snmpd.conf
RUN service snmpd restart

# setup IRC
RUN mv /etc/inspircd/inspircd.conf /etc/inspircd/inspircd.conf.bak
ADD docker/inspircd.conf /etc/inspircd/inspircd.conf

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

# DWVA WebApp Exploit
ADD docker/sql_injection_exploit.sh /sql_injection_exploit.sh
RUN chmod 777 /sql_injection_exploit.sh

## Setup Samba
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
    conda create --name samba python=2.7 -y
# Make subsequent RUN commands use the samba env
SHELL ["conda", "run", "-n", "samba", "/bin/bash", "-c"]
#RUN conda activate samba
RUN pip install pycrypto==2.6 &&\
    pip install git+git://github.com/opsxcq/impacket.git &&\
    pip install pyasn1

# CVE-2015-3306 Exploit
ADD docker/cve_2015_3306_exploit.py /cve_2015_3306_exploit.py
RUN chmod 777 /cve_2015_3306_exploit.py

# CVE-2015-1427 Exploit
ADD docker/cve_2015_1427_exploit.sh /cve_2015_1427_exploit.sh
RUN chmod 777 /cve_2015_1427_exploit.sh
