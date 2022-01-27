# OS
FROM csle/cve_2010_0426_base:0.0.1
USER root

# Add start script
ADD cve_2010_0426_1/docker/start.sh /start.sh
RUN chmod 777 /start.sh

# CMD to run when container starts, starts the services
CMD ["/start.sh"]
