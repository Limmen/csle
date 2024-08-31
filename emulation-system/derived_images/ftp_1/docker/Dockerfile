# OS
FROM kimham/csle_ubuntu_14_base:0.7.0
USER root

# timezone env with default
ENV TZ=Europe/Stockholm

# Add start script
ADD start.sh /start.sh
RUN chmod 777 /start.sh

# Setup Finger
RUN /etc/init.d/inetutils-inetd restart

# Setup Mongo
RUN mkdir -p /data/db

# SSH
RUN service ssh start


# CMD to run when container starts, starts the services (e.g. telnet and SSH)
CMD ["/start.sh"]

