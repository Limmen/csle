# OS
FROM kalilinux/kali-last-release
USER root

# Install dependencies
RUN apt update && apt -y reinstall ca-certificates
RUN apt-get -y install apt-utils  \
                       openssl net-tools iputils-ping sudo emacs curl htop telnet ssh openssh-server ftp \
                       exploitdb nikto traceroute finger git sshpass lftp recon-ng netdiscover hping3 ncat masscan \
                       iptables proxychains zip unzip arptables irssi irssi-scripts screen postgresql-client-common \
                       snmp postgresql-client smbclient tcpdump netcat-traditional traceroute sysstat iproute2  \
                       lsof

#RUN apt-get -y install man-db
#&& DEBIAN_FRONTEND=noninteractive apt -yqq install kali-linux-headless
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --fix-missing kali-tools-top10

# Setup users

# Add users script
ADD docker_files/common/make_root_users.sh /make_root_users.sh
ADD docker_files/common/root_users.txt /root_users.txt
RUN chmod 777 /make_root_users.sh

# setup root users
RUN /make_root_users.sh

# SSH
RUN service ssh start

# NMAP vuln scan
RUN git clone https://github.com/Limmen/vulscan scipag_vulscan &&\
    ln -s `pwd`/scipag_vulscan /usr/share/nmap/scripts/vulscan

# NMAP nmap-vulners
RUN git clone https://github.com/Limmen/nmap-vulners &&\
    cp nmap-vulners/vulners.nse /usr/share/nmap/scripts/ &&\
    nmap --script-updatedb

# SecLists
RUN git clone https://github.com/Limmen/SecLists

# 1. Alias
# 2. Setup root passwd
RUN echo "alias ll='ls -al'" >> /root.bashrc &&\
    echo "root:root" | /usr/sbin/chpasswd

# Setup root SSH
RUN mv /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
ADD docker_files/common/sshd_config /etc/ssh/sshd_config

# Setup password-less sudo
RUN mv /etc/sudoers /etc/sudoers.bak
ADD docker_files/common/sudoers /etc/sudoers

# 1. Download nmap-services
# 2. Download CVEs
RUN wget --no-check-certificate https://raw.githubusercontent.com/nmap/nmap/master/nmap-services &&\
    wget --no-check-certificate https://cve.mitre.org/data/downloads/allitems.csv

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
    conda create --name samba python=2.7 -y


## Make subsequent RUN commands use the samba env
SHELL ["conda", "run", "-n", "samba", "/bin/bash", "-c"]

RUN pip install pycrypto==2.6 &&\
    pip install git+https://github.com/opsxcq/impacket.git &&\
    pip install pyasn1==0.4.8

# Setup base environment with csle-collector
SHELL ["conda", "run", "-n", "base", "/bin/bash", "-c"]

RUN pip install flask &&\
    pip install waitress &&\
    pip install csle-collector &&\
    pip install pyspark &&\
    pip install netifaces

# Prep CVEs
ADD docker_files/kali_base/docker/cve_prep.py /cve_prep.py
RUN python /cve_prep.py

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

# Spark job
ADD docker_files/common/spark_job.py /spark_job.py
RUN chmod 777 /spark_job.py

# Add Tini
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]