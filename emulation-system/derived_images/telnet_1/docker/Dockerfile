# OS
FROM kimham/csle_ubuntu_20_base:0.8.0
USER root

# SSH
RUN service ssh start

# Add start script
ADD start.sh /start.sh
RUN chmod 777 /start.sh

# timezone env with default
ENV TZ=Europe/Stockholm

# CMD to run when container starts, starts the services (e.g. telnet and SSH)
CMD ["/start.sh"]