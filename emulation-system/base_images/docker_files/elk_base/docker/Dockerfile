ARG IMAGE=focal-1.1.0
FROM phusion/baseimage:${IMAGE}

RUN set -x \
 && apt update -qq \
 && apt install -qqy --no-install-recommends ca-certificates curl gosu tzdata openjdk-11-jdk-headless \
 && apt clean \
 && rm -rf /var/lib/apt/lists/* \
 && gosu nobody true \
 && set +x


RUN apt-get update
RUN echo "postfix postfix/mailname string csle" | debconf-set-selections &&\
        echo "postfix postfix/main_mailer_type string 'Internet Site'" | debconf-set-selections &&\
        echo "snort snort/address_range string 172.18.1.0/24" | debconf-set-selections &&\
        apt-get -y install --fix-missing lsb-release apt-utils sudo openssl net-tools iputils-ping emacs curl htop ssh openssh-server \
        ftp snmpd snmp mailutils inspircd postgresql ntp vsftpd bind9 bind9utils bind9-doc bind9-host dnsutils git \
        swi-prolog openjdk-8-jdk sshpass iptables unzip nmap git telnet xinetd telnetd lftp zip snort arptables \
        irssi irssi-scripts screen postgresql-client-common snmp mongodb-clients postgresql-client smbclient fail2ban \
        rsyslog netcat traceroute sysstat iproute2 iperf3 libpcap-dev libpcre3-dev libdumbnet-dev flex bison lsof  \
        default-jre default-jdk


# Add users script
ADD docker_files/common/make_root_users.sh /make_root_users.sh
ADD docker_files/common/root_users.txt /root_users.txt
RUN chmod 777 /make_root_users.sh

# setup root users
RUN /make_root_users.sh

# Setup root SSH
RUN mv /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
ADD docker_files/common/sshd_config /etc/ssh/sshd_config
RUN service ssh start

# Setup password-less sudo
RUN mv /etc/sudoers /etc/sudoers.bak
ADD docker_files/common/sudoers /etc/sudoers

### set current package version

ARG ELK_VERSION=8.3.3

# base version (i.e. remove OSS prefix) for Elasticsearch and Kibana (no OSS version since 7.11.0)
ARG ELK_BASE_VERSION=8.3.3

# replace with aarch64 for ARM64 systems
ARG ARCH=x86_64 


### install Elasticsearch

# predefine env vars, as you can't define an env var that references another one in the same block
ENV \
 ES_VERSION=${ELK_BASE_VERSION} \
 ES_HOME=/opt/elasticsearch

ENV \
 ES_PACKAGE=elasticsearch-${ES_VERSION}-linux-${ARCH}.tar.gz \
 ES_GID=991 \
 ES_UID=991 \
 ES_PATH_CONF=/etc/elasticsearch \
 ES_PATH_BACKUP=/var/backups

RUN DEBIAN_FRONTEND=noninteractive \
 && mkdir ${ES_HOME} \
 && curl -O https://artifacts.elastic.co/downloads/elasticsearch/${ES_PACKAGE} \
 && tar xzf ${ES_PACKAGE} -C ${ES_HOME} --strip-components=1 \
 && rm -f ${ES_PACKAGE} \
 && groupadd -r elasticsearch -g ${ES_GID} \
 && useradd -r -s /usr/sbin/nologin -M -d ${ES_HOME} -c "Elasticsearch service user" -u ${ES_UID} -g elasticsearch elasticsearch \
 && mkdir -p /var/log/elasticsearch ${ES_PATH_CONF} ${ES_PATH_CONF}/scripts ${ES_PATH_CONF}/jvm.options.d /var/lib/elasticsearch ${ES_PATH_BACKUP} \
 && chown -R elasticsearch:elasticsearch ${ES_HOME} /var/log/elasticsearch /var/lib/elasticsearch ${ES_PATH_CONF} ${ES_PATH_BACKUP}


### install Logstash

ENV \
 LOGSTASH_VERSION=${ELK_VERSION} \
 LOGSTASH_HOME=/opt/logstash

ENV \
 LOGSTASH_PACKAGE=logstash-${LOGSTASH_VERSION}-linux-${ARCH}.tar.gz \
 LOGSTASH_GID=992 \
 LOGSTASH_UID=992 \
 LOGSTASH_PATH_CONF=/etc/logstash \
 LOGSTASH_PATH_SETTINGS=${LOGSTASH_HOME}/config

RUN mkdir ${LOGSTASH_HOME} \
 && curl -O https://artifacts.elastic.co/downloads/logstash/${LOGSTASH_PACKAGE} \
 && tar xzf ${LOGSTASH_PACKAGE} -C ${LOGSTASH_HOME} --strip-components=1 \
 && rm -f ${LOGSTASH_PACKAGE} \
 && groupadd -r logstash -g ${LOGSTASH_GID} \
 && useradd -r -s /usr/sbin/nologin -M -d ${LOGSTASH_HOME} -c "Logstash service user" -u ${LOGSTASH_UID} -g logstash logstash \
 && mkdir -p /var/log/logstash ${LOGSTASH_PATH_CONF}/conf.d \
 && chown -R logstash:logstash ${LOGSTASH_HOME} /var/log/logstash ${LOGSTASH_PATH_CONF}


### install Kibana

ENV \
 KIBANA_VERSION=${ELK_BASE_VERSION} \
 KIBANA_HOME=/opt/kibana

ENV \
 KIBANA_PACKAGE=kibana-${KIBANA_VERSION}-linux-${ARCH}.tar.gz \
 KIBANA_GID=993 \
 KIBANA_UID=993

RUN mkdir ${KIBANA_HOME} \
 && curl -O https://artifacts.elastic.co/downloads/kibana/${KIBANA_PACKAGE} \
 && tar xzf ${KIBANA_PACKAGE} -C ${KIBANA_HOME} --strip-components=1 \
 && rm -f ${KIBANA_PACKAGE} \
 && groupadd -r kibana -g ${KIBANA_GID} \
 && useradd -r -s /usr/sbin/nologin -d ${KIBANA_HOME} -c "Kibana service user" -u ${KIBANA_UID} -g kibana kibana \
 && mkdir -p /var/log/kibana \
 && chown -R kibana:kibana ${KIBANA_HOME} /var/log/kibana


###############################################################################
#                              START-UP SCRIPTS
###############################################################################

### Elasticsearch
ADD docker_files/elk_base/docker/elasticsearch-init /etc/init.d/elasticsearch
RUN sed -i -e 's#^ES_HOME=$#ES_HOME='$ES_HOME'#' /etc/init.d/elasticsearch \
 && chmod +x /etc/init.d/elasticsearch


### Logstash

ADD docker_files/elk_base/docker/logstash-init /etc/init.d/logstash
RUN sed -i -e 's#^LS_HOME=$#LS_HOME='$LOGSTASH_HOME'#' /etc/init.d/logstash \
 && chmod +x /etc/init.d/logstash


### Kibana

ADD docker_files/elk_base/docker/kibana-init /etc/init.d/kibana
RUN sed -i -e 's#^KIBANA_HOME=$#KIBANA_HOME='$KIBANA_HOME'#' /etc/init.d/kibana \
 && chmod +x /etc/init.d/kibana


###############################################################################
#                               CONFIGURATION
###############################################################################

### configure Elasticsearch

ADD docker_files/elk_base/docker/elasticsearch.yml ${ES_PATH_CONF}/elasticsearch.yml
ADD docker_files/elk_base/docker/elasticsearch-default /etc/default/elasticsearch
RUN cp ${ES_HOME}/config/log4j2.properties ${ES_HOME}/config/jvm.options \
    ${ES_PATH_CONF} \
 && chown -R elasticsearch:elasticsearch ${ES_PATH_CONF} \
 && chmod -R +r ${ES_PATH_CONF}


### configure Logstash

# certs/keys for Beats and Lumberjack input
RUN mkdir -p /etc/pki/tls/{certs,private}
ADD docker_files/elk_base/docker/logstash-beats.crt /etc/pki/tls/certs/logstash-beats.crt
ADD docker_files/elk_base/docker/logstash-beats.key /etc/pki/tls/private/logstash-beats.key

# pipelines
ADD docker_files/elk_base/docker/pipelines.yml ${LOGSTASH_PATH_SETTINGS}/pipelines.yml

# filters
ADD docker_files/elk_base/docker/logstash-conf/*.conf ${LOGSTASH_PATH_CONF}/conf.d/

# patterns
ADD docker_files/elk_base/docker/nginx.pattern ${LOGSTASH_HOME}/patterns/nginx
RUN chown -R logstash:logstash ${LOGSTASH_HOME}/patterns

# Fix permissions
RUN chmod -R +r ${LOGSTASH_PATH_CONF} ${LOGSTASH_PATH_SETTINGS} \
 && chown -R logstash:logstash ${LOGSTASH_PATH_SETTINGS}


### configure logrotate

ADD docker_files/elk_base/docker/elasticsearch-logrotate /etc/logrotate.d/elasticsearch
ADD docker_files/elk_base/docker/logstash-logrotate /etc/logrotate.d/logstash
ADD docker_files/elk_base/docker/kibana-logrotate /etc/logrotate.d/kibana
RUN chmod 644 /etc/logrotate.d/elasticsearch \
 && chmod 644 /etc/logrotate.d/logstash \
 && chmod 644 /etc/logrotate.d/kibana


### configure Kibana

ADD docker_files/elk_base/docker/kibana.yml ${KIBANA_HOME}/config/kibana.yml

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

# Setup base environment with csle-collector
#SHELL ["conda", "run", "-n", "base", "/bin/bash", "-c"]
RUN pip install flask && \
    pip install waitress && \
    pip install csle-collector

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

###############################################################################
#                                   START
###############################################################################

ADD docker_files/elk_base/docker/start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

# Add Tini
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]


