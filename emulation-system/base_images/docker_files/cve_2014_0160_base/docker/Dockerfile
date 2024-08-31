# OS
# Debian 10.2
FROM kimham/csle_debian_10_base:0.7.0
USER root

# Environment
ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get install -y dialog apt-utils multiarch-support

RUN wget http://snapshot.debian.org/archive/debian/20170705T160707Z/pool/main/o/openssl/libssl1.0.0_1.0.2l-1%7Ebpo8%2B1_amd64.deb
RUN dpkg -i libssl1.0.0*.deb

# Install vulnerable versions from wayback/snapshot archive
RUN wget http://snapshot.debian.org/archive/debian/20130319T033933Z/pool/main/o/openssl/openssl_1.0.1e-2_amd64.deb -O /tmp/openssl_1.0.1e-2_amd64.deb && \
    dpkg -i /tmp/openssl_1.0.1e-2_amd64.deb
#
RUN wget http://snapshot.debian.org/archive/debian/20130319T033933Z/pool/main/o/openssl/libssl1.0.0_1.0.1e-2_amd64.deb -O /tmp/libssl1.0.0_1.0.1e-2_amd64.deb && \
    dpkg -i /tmp/libssl1.0.0_1.0.1e-2_amd64.deb

ENV DEBIAN_FRONTEND noninteractive

# Setup vulnerable web server and enable SSL based Apache instance

ADD docker_files/cve_2014_0160_base/docker/index.html /var/www/html/
RUN sed -i 's/^NameVirtualHost/#NameVirtualHost/g' /etc/apache2/ports.conf && \
    sed -i 's/^Listen/#Listen/g' /etc/apache2/ports.conf
RUN a2enmod ssl && \
    a2dissite 000-default.conf && \
    a2ensite default-ssl