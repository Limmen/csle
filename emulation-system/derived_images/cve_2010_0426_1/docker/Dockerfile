# OS
FROM kimham/csle_cve_2010_0426_base:0.0.2
USER root

# Add start script
ADD start.sh /start.sh
RUN chmod 777 /start.sh

# CMD to run when container starts, starts the services
CMD ["/start.sh"]
