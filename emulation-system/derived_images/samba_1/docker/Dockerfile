# OS
FROM kimham/csle_samba_base:0.8.0
USER root

# Add start script
ADD start.sh /start.sh
RUN chmod 777 /start.sh

# timezone env with default
ENV TZ=Europe/Stockholm

# Override base image's entrypoint
ENTRYPOINT ["/usr/bin/env"]

# CMD to run when container starts, starts the services (e.g. Samba)
CMD ["/start.sh"]
