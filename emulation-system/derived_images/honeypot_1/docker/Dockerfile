# OS
FROM kimham/csle_ubuntu_20_base:0.0.3
USER root

# Add start script
ADD start.sh /start.sh
RUN chmod 777 /start.sh

# setup SNMP
RUN service snmpd restart

# setup NTP
RUN service ntp restart

# SSH
RUN service ssh start

# CMD to run when container starts, starts the services (e.g. telnet and SSH)
CMD ["/start.sh"]
