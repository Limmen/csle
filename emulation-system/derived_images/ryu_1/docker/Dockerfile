# OS
FROM csle/ryu_base:0.0.1
USER root

# Add start script
ADD start.sh /start.sh
RUN chmod 777 /start.sh

# SSH
RUN service ssh start

# CMD to run when container starts
CMD ["/start.sh"]
