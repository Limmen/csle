# OS
FROM csle/ubuntu_20_base:0.0.1
USER root

# SSH
RUN service ssh start

# Add start script
ADD docker/start.sh /start.sh
RUN chmod 777 /start.sh

# CMD to run when container starts, starts the services (e.g. telnet and SSH)
CMD ["/start.sh"]