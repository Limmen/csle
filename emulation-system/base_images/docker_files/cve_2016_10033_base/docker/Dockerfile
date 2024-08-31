# OS
# Debian GNU/Linux 8 (jessie)
FROM kimham/csle_debian_10_base:0.7.0
USER root

ADD docker_files/cve_2016_10033_base/docker/www /www

RUN git clone https://github.com/Limmen/exploit-CVE-2016-10033
RUN cp -r exploit-CVE-2016-10033/src /www/vulnerable/

RUN chmod 777 -R /www

ADD docker_files/cve_2016_10033_base/docker/virtual-host /etc/apache2/sites-enabled/000-default.conf

RUN mv /etc/apache2/envvars /etc/apache2/envvars.backup
ADD docker_files/common/apache_envvars /etc/apache2/envvars

RUN chown -R csle_admin:root /run/apache2 &&\
    chmod -R 777 /var/www &&\
    chown -R csle_admin:root /var/www

ADD docker_files/cve_2016_10033_base/docker/main.sh /main.sh
RUN chmod 777 /main.sh

ADD docker_files/cve_2016_10033_base/docker/create_backdoor_cve_2016_10033.sh /create_backdoor_cve_2016_10033.sh
RUN chmod 777 /create_backdoor_cve_2016_10033.sh