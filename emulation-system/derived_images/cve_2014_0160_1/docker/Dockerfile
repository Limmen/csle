# OS
FROM csle/cve_2014_0160_base:0.0.1
USER root

# Add start script
ADD cve_2014_0160_1/docker/start.sh /start.sh
RUN chmod 777 /start.sh

# nmap -sV -p 443 --script=ssl-heartbleed 55.144.78.232

# CMD to run when container starts, starts the services
CMD ["/start.sh"]
