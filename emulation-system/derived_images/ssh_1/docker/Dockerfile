# OS
FROM kimham/csle_ssh_base:0.0.1
USER root

# Add start script
ADD start.sh /start.sh
RUN chmod 777 /start.sh

# SSH
RUN service ssh start

# DNS
RUN service named start

# CMD to run when container starts, starts the services (e.g. telnet and SSH)
CMD ["/start.sh"]
