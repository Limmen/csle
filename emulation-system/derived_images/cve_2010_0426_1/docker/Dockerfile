# OS
FROM kimham/csle_cve_2010_0426_base:0.8.0
USER root

# Add start script
ADD start.sh /start.sh
RUN chmod 777 /start.sh

# timezone env with default
ENV TZ=Europe/Stockholm

# CMD to run when container starts, starts the services
CMD ["/start.sh"]
