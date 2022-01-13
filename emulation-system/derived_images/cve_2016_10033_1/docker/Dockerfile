# OS
FROM csle/cve_2016_10033_base:0.0.1
USER root

# Add start script
ADD docker/start.sh /start.sh
RUN chmod 777 /start.sh

# CMD to run when container starts, starts the services (e.g. elastic)
CMD ["/start.sh"]
