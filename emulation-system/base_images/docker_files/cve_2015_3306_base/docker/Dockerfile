# OS
# Debian 10.2
FROM kimham/csle_debian_10_base:0.7.0
USER root

# configure vuln application
RUN wget --no-check-certificate ftp://ftp.proftpd.org/distrib/source/proftpd-1.3.5.tar.gz && \
    tar xfz proftpd-1.3.5.tar.gz && \
    cd proftpd-1.3.5 && \
    ./configure --with-modules=mod_copy && \
    make && make install
RUN chmod 777 -R /var/www/html/
RUN mv /etc/apache2/envvars /etc/apache2/envvars.backup
ADD docker_files/common/apache_envvars /etc/apache2/envvars
RUN chown -R csle_admin:root /run/apache2 &&\
    chmod -R 777 /var/www &&\
    chown -R csle_admin:root /var/www
ADD docker_files/cve_2015_3306_base/docker/main.sh /main.sh
RUN chmod 777 /main.sh
