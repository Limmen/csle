# OS
FROM kimham/csle_cve_2015_5602_base:0.7.0
USER root

# Add start script
ADD start.sh /start.sh
RUN chmod 777 /start.sh

# timezone env with default
ENV TZ=Europe/Stockholm

# CMD to run when container starts, starts the services
CMD ["/start.sh"]
