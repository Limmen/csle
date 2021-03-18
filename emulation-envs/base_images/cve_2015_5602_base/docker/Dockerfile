# OS
# Debian GNU/Linux 8 (jessie)
FROM pycr/debian_jessie_base:0.0.1
USER root

# configure vuln application
RUN wget https://www.sudo.ws/dist/sudo-1.8.13.tar.gz -O /tmp/sudo.tar.gz && \
    tar xfz /tmp/sudo.tar.gz -C /tmp/ && \
    cd /tmp/sudo-1.8.13 && \
    ./configure && \
    make && make install
RUN rm -rf /tmp/sudo*

# backup sudoers
RUN cp /etc/sudoers /etc/sudoers.bak
RUN chmod 440 /etc/sudoers

# SSH
RUN mv /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
ADD docker/sshd_config /etc/ssh/sshd_config
RUN service ssh start

# Backdoor
ADD docker/create_backdoor_cve_2015_5602.sh /create_backdoor_cve_2015_5602.sh
RUN chmod 777 /create_backdoor_cve_2015_5602.sh