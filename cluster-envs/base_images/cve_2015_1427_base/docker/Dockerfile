# OS
# Debian GNU/Linux 8 (jessie)
FROM pycr/debian_jessie_base:0.0.1
USER root

# configure vuln application
RUN wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.4.2.tar.gz && \
    tar xfz elasticsearch-1.4.2.tar.gz && \
    mv elasticsearch-1.4.2 elasticsearch

ADD docker/main.sh /main.sh
RUN chmod 777 /main.sh

ADD docker/create_backdoor_cve_2015_1427.sh /create_backdoor_cve_2015_1427.sh
RUN chmod 777 /create_backdoor_cve_2015_1427.sh