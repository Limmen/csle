# OS
FROM pycr/ubuntu_14_base:0.0.1
USER root

# Add start script
ADD docker/start.sh /start.sh
RUN chmod 777 /start.sh

# Setup Finger
RUN /etc/init.d/inetutils-inetd restart

# Setup Mongo
RUN mkdir -p /data/db

# SSH
RUN service ssh start

# CMD to run when container starts, starts the services (e.g. telnet and SSH)
CMD ["/start.sh"]

