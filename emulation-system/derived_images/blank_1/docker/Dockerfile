# OS
FROM kimham/csle_blank_ubuntu_20:0.0.2
USER root

# Add start script
ADD start.sh /start.sh
RUN chmod 777 /start.sh

# CMD to run when container starts, starts the services (e.g. telnet and SSH)
CMD ["/start.sh"]
