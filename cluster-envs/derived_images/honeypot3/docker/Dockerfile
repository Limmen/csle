# OS
FROM pycr/ubuntu_20_base:0.0.1
USER root

# Add start script
ADD docker/start.sh /start.sh
RUN chmod 777 /start.sh

# setup SNMP
RUN service snmpd restart

# setup NTP
RUN service ntp restart

# setup Postgres
RUN service postgresql restart

# CMD to run when container starts, starts the services (e.g. telnet and SSH)
CMD /start.sh
