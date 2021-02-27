# OS
# Debian GNU/Linux 8 (jessie)
FROM pycr/debian_jessie_base:0.0.1
USER root

ADD docker/www /www

RUN git clone https://github.com/opsxcq/exploit-CVE-2016-10033
RUN cp -r exploit-CVE-2016-10033/src /www/vulnerable/

RUN chmod 777 -R /www

ADD docker/virtual-host /etc/apache2/sites-enabled/000-default.conf

RUN mv /etc/apache2/envvars /etc/apache2/envvars.backup
ADD docker/apache_envvars /etc/apache2/envvars

RUN chown -R pycr_admin:root /run/apache2 &&\
    chmod -R 777 /var/www &&\
    chown -R pycr_admin:root /var/www

ADD docker/main.sh /main.sh
RUN chmod 777 /main.sh

ADD docker/create_backdoor_cve_2016_10033.sh /create_backdoor_cve_2016_10033.sh
RUN chmod 777 /create_backdoor_cve_2016_10033.sh