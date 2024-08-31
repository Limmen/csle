# OS
# Ubuntu 20
FROM kimham/csle_ubuntu_20_base:0.7.0
USER root

RUN apt-get install -y --force-yes lsb-release libtinfo5 apache2

SHELL ["/bin/bash", "-c"]

# Apache2 Shellshock setup
ADD docker_files/shellshock_base/docker/packages /packages
RUN dpkg -i /packages/*
ADD docker_files/shellshock_base/docker/vulnerable /usr/lib/cgi-bin/
ADD docker_files/shellshock_base/docker/index.html /var/www/html
RUN chown www-data:www-data /var/www/html/index.html
ADD docker_files/shellshock_base/docker/main.sh /main.sh
RUN mv /etc/apache2/envvars /etc/apache2/envvars.backup
ADD docker_files/common/apache_envvars /etc/apache2/envvars

RUN chown -R csle_admin:root /run &&\
    chmod -R 777 /var &&\
    chown -R csle_admin:root /var
