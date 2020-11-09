# OS
FROM pycr/ubuntu_20_base:0.0.1
USER root

# Add start script
ADD docker/start.sh /start.sh
RUN chmod 777 /start.sh

# Setup users

# Add users script
ADD docker/make_root_users.sh /make_root_users.sh
ADD docker/make_non_root_users.sh /make_non_root_users.sh
ADD docker/root_users.txt /root_users.txt
ADD docker/non_root_users.txt /non_root_users.txt
RUN chmod 777 /make_root_users.sh
RUN chmod 777 /make_non_root_users.sh

# setup root users
RUN /make_root_users.sh

# setup non-root users
RUN /make_non_root_users.sh

# setup SNMP
RUN service snmpd restart

# setup NTP
RUN service ntp restart

# setup Postgres
RUN service postgresql restart

# CMD to run when container starts, starts the services (e.g. telnet and SSH)
CMD /start.sh
