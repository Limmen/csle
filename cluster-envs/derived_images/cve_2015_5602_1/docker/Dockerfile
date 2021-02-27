# OS
FROM pycr/cve_2015_5602_base:0.0.1
USER root

# Add start script
ADD docker/start.sh /start.sh
RUN chmod 777 /start.sh

# CMD to run when container starts, starts the services
CMD /start.sh
