# OS
FROM csle/ubuntu_20_base:0.0.1
USER root

# SSH
RUN mv /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
ADD docker_files/ssh_base/fdocker/sshd_config /etc/ssh/sshd_config
RUN service ssh start
