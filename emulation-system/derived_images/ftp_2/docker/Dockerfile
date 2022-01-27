# OS
FROM csle/ubuntu_14_base:0.0.1
USER root

# Add start script
ADD ftp_2/docker/start.sh /start.sh
RUN chmod 777 /start.sh

# CMD to run when container starts, starts the services (e.g. telnet and SSH)
CMD ["/start.sh"]

