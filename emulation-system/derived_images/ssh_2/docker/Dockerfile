# OS
FROM kimham/csle_ssh_base:0.8.0
USER root

# Add start script
ADD start.sh /start.sh
RUN chmod 777 /start.sh

# timezone env with default
ENV TZ=Europe/Stockholm

# SSH
RUN service ssh start

# setup NTP
RUN service ntp restart

# DNS
RUN service named start

# CMD to run when container starts, starts the services (e.g. telnet and SSH)
CMD ["/start.sh"]
