# OS
FROM kimham/csle_ovs_base:0.7.0
USER root

# Add start script
ADD start.sh /start.sh
RUN chmod 777 /start.sh

# SSH
RUN service ssh start

# timezone env with default
ENV TZ=Europe/Stockholm

# CMD to run when container starts
CMD ["/start.sh"]
