# OS
FROM kimham/csle_cve_2015_3306_base:0.0.2
USER root

# Add start script
ADD start.sh /start.sh
RUN chmod 777 /start.sh

# Override base image's entrypoint
ENTRYPOINT ["/usr/bin/env"]

# CMD to run when container starts, starts the services (e.g. Samba)
#CMD ["bash", "/start.sh"]
CMD ["/start.sh"]
