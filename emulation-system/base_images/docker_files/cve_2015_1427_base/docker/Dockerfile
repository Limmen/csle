# OS
FROM kimham/csle_debian_10_base:0.7.0
USER root

# configure vuln application
RUN wget --no-check-certificate https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.4.2.tar.gz && \
    tar xfz elasticsearch-1.4.2.tar.gz && \
    mv elasticsearch-1.4.2 elasticsearch
ADD docker_files/cve_2015_1427_base/docker/main.sh /main.sh
RUN chmod 777 /main.sh

# Add CVE-2015-1427 backdoor script
ADD docker_files/cve_2015_1427_base/docker/create_backdoor_cve_2015_1427.sh /create_backdoor_cve_2015_1427.sh
RUN chmod 777 /create_backdoor_cve_2015_1427.sh