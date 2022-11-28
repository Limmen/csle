# OS
FROM kimham/csle_samba_base:0.0.1
USER root

# Add start script
ADD start.sh /start.sh
RUN chmod 777 /start.sh

# Override base image's entrypoint
ENTRYPOINT ["/usr/bin/env"]

# CMD to run when container starts, starts the services (e.g. Samba)
#CMD ["bash", "/start.sh"]
CMD ["/start.sh"]
#CMD /start.sh
