# OS
FROM csle/blank_ubuntu_20:0.0.1
USER root

# Add start script
ADD blank_1/docker/start.sh /start.sh
RUN chmod 777 /start.sh

# CMD to run when container starts, starts the services (e.g. telnet and SSH)
CMD ["/start.sh"]
