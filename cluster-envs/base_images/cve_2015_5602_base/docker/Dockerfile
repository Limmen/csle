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

## create default user
#RUN useradd -d /home/user \
#    -s /bin/bash \
#    -ms /bin/bash user

# backup sudoers
RUN cp /etc/sudoers /etc/sudoers.bak
RUN chmod 440 /etc/sudoers

# add sudoers entry
#RUN echo 'user ALL=NOPASSWD: sudoedit /home/*/*/esc.txt' >> /etc/sudoers
#RUN chmod 440 /etc/sudoers

# SSH
RUN mv /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
ADD docker/sshd_config /etc/ssh/sshd_config
RUN service ssh start

