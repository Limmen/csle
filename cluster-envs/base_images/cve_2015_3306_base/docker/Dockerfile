# OS
# Debian GNU/Linux 8 (jessie)
FROM pycr/debian_jessie_base:0.0.1
USER root

# configure vuln application
RUN wget ftp://ftp.proftpd.org/distrib/source/proftpd-1.3.5.tar.gz && \
    tar xfz proftpd-1.3.5.tar.gz && \
    cd proftpd-1.3.5 && \
    ./configure --with-modules=mod_copy && \
    make && make install
RUN chmod 777 -R /var/www/html/

RUN mv /etc/apache2/envvars /etc/apache2/envvars.backup
ADD docker/apache_envvars /etc/apache2/envvars
RUN chown -R pycr_admin:root /run/apache2 &&\
    chmod -R 777 /var/www &&\
    chown -R pycr_admin:root /var/www

ADD docker/main.sh /main.sh
RUN chmod 777 /main.sh
