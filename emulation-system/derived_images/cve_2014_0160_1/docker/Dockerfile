# OS
FROM kimham/csle_cve_2014_0160_base:0.7.0
USER root

# Add start script
ADD start.sh /start.sh
RUN chmod 777 /start.sh

# nmap -sV -p 443 --script=ssl-heartbleed 55.144.78.232

# timezone env with default
ENV TZ=Europe/Stockholm

# CMD to run when container starts, starts the services
CMD ["/start.sh"]
