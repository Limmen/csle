# OS
FROM kimham/csle_elk_base:0.8.0
USER root

# Add start script
ADD start.sh /start.sh
RUN chmod 777 /start.sh

# timezone env with default
ENV TZ=Europe/Stockholm

# SSH
RUN service ssh start

# CMD to run when container starts
CMD ["/start.sh"]
