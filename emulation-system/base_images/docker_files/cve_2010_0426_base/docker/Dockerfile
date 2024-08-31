# OS
# Debian 10.2
FROM kimham/csle_debian_10_base:0.7.0
USER root

# configure vuln application
#https://www.sudo.ws/dist/OLD/sudo-1.7.2.tar.gz
RUN wget --no-check-certificate http://repository.timesys.com/buildsources/s/sudo/sudo-1.7.2/sudo-1.7.2.tar.gz -O /tmp/sudo.tar.gz && \
    tar xfz /tmp/sudo.tar.gz -C /tmp/ && \
    cd /tmp/sudo-1.7.2 && \
    ./configure && \
    make && make install
RUN rm -rf /tmp/sudo*

# backup sudoers
RUN cp /etc/sudoers /etc/sudoers.bak
RUN chmod 440 /etc/sudoers

# SSH
RUN mv /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
ADD docker_files/cve_2010_0426_base/docker/sshd_config /etc/ssh/sshd_config
RUN service ssh start

# Backdoor
ADD docker_files/cve_2010_0426_base/docker/create_backdoor_cve_2010_0426.sh /create_backdoor_cve_2010_0426.sh
RUN chmod 777 /create_backdoor_cve_2010_0426.sh