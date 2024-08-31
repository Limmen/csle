# OS
FROM kimham/csle_ubuntu_20_base:0.7.0
USER root

# SSH
RUN mv /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
ADD docker_files/ssh_base/docker/sshd_config /etc/ssh/sshd_config
RUN service ssh start
