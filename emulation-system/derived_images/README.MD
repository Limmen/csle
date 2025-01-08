# Derived Images

This directory contains derived Docker images used in `csle` when emulating computer infrastructures. 
These images are derivations of the [base images](../base_images) of `csle`. The derived images include
kali images, vulnerable images, and images with general network services. These images can be used to 
generate containers for emulating various network infrastructures.

## List of Derived Images

- `cve_2010_0426_1` ([cve_2010_0426_1](./cve_2010_0426_1)): an image with the CVE-2010-0426 vulnerability.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_cve_2010_0426_1?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_cve_2010_0426_1/)
     - OS: Debian:10.2. 
     - Inherits from `cve_2010_0426_base`.
     - Services: teamspeak3, tomcat, ssh
- `cve_2015_1427_1` ([cve_2015_1427_1](./cve_2015_1427_1)): an image with the CVE-2015-1427 vulnerability.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_cve_2015_1427_1?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_cve_2015_1427_1/)
     - OS: Debian:10.2. 
     - Inherits from `cve_2015_1427_base`.
     - Services: SNMP, elasticsearch, apache webserver, ssh
- `cve_2015_3306_1` ([cve_2015_3306_1](./cve_2015_3306_1)): an image with the CVE-2015-3306 vulnerability.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_cve_2015_3306_1?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_cve_2015_3306_1/)
     - OS: Debian:10.2. 
     - Inherits from `cve_2015_3306_base`.
     - Services: ssh, SNMP, proftpd, apache2
- `cve_2015_5602_1` ([cve_2015_5602_1](./cve_2015_5602_1)): an image with the CVE-2015-5602 vulnerability.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_cve_2015_5602_1?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_cve_2015_5602_1/)
     - OS: Debian:10.2. 
     - Inherits from `cve_2015_5602_base`.
     - Services: ssh
- `cve_2016_10033_1` ([cve_2016_10033_1](./cve_2016_10033_1)): an image with the CVE-2016-10033 vulnerability.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_cve_2016_10033_1?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_cve_2016_10033_1/)
     - OS: Debian:10.2. 
     - Inherits from `cve_2010_0426_1`.
     - Services: ssh, apache2, SMTPD
- `hacker_kali_1` ([hacker_kali_1](./hacker_kali_1)): a Kali image, used to generate containers with tools for penetration testing.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_hacker_kali_1?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_hacker_kali_1/)
     - OS: Kali (Latest). 
     - Inherits from `kali_base`.
     - Services: ssh
- `samba_1` ([samba_1](./samba_1)): an image with the SambaCry CVE-2017-7494 vulnerabilitiy.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_samba_1?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_samba_1/)
     - OS: Debian:10.2. 
     - Inherits from `samba_base`.
     - Services: ssh, NTP, samba
- `samba_2` ([samba_2](./samba_2)): an image with the SambaCry CVE-2017-7494 vulnerabilitiy and a telnet server.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_samba_2?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_samba_2/)
     - OS: Debian:10.2. 
     - Inherits from `samba_base`.
     - Services: ssh, NTP, samba, telnet     
- `shellshock_1` ([shellshock_1](./shellshock_1)): an image with the ShellShock CVE-2014-6271 vulnerabilitiy.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_shellshock_1?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_shellshock_1/)
     - OS: Debian:Wheezy. 
     - Inherits from `shellshock_base`.
     - Services: ssh, SNMP, apache2
- `sql_injection_1` ([sql_injection_1](./sql_injection_1)): an image with a webapp that is vulnerable to SQL injections.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_sql_injection_1?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_sql_injection_1/)
     - OS: Debian:9.2. 
     - Inherits from `sql_injection_base`.
     - Services: IRC, apache2, ssh
- `ftp_1` ([ftp_1](./ftp_1)): an image with a FTP server that can be used to generate containers vulnerable to brute-force attacks.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_ftp_1?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_ftp_1/)
     - OS: Ubuntu:14. 
     - Inherits from `ubuntu_14_base`.
     - Services: VSFTPD, MongoDB, SMTP, tomcat, teamspeak3, ssh
- `ftp_2` ([ftp_2](./ftp_2)): an image with a FTP server that can be used to generate containers vulnerable to brute-force attacks.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_ftp_2?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_ftp_2/)
     - OS: Ubuntu:14. 
     - Inherits from `ubuntu_14_base`.
     - Services: VSFTPD, ssh, DNS
- `ssh_1` ([ssh_1](./ssh_1)): an image with a SSH server that can be used to generate containers vulnerable to brute-force attacks.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_ssh_1?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_ssh_1/)
     - OS: Ubuntu:20. 
     - Inherits from `ssh_base`.
     - Services: ssh, erl_pengine webapp, DNS
- `ssh_2` ([ssh_2](./ssh_2)): an image with a SSH server that can be used to generate containers vulnerable to brute-force attacks.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_ssh_2?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_ssh_2/)
     - OS: Ubuntu:20. 
     - Inherits from `ssh_base`.
     - Services: ssh, DNS, NTP
- `ssh_3` ([ssh_3](./ssh_3)): an image with a SSH server that can be used to generate containers vulnerable to brute-force attacks.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_ssh_3?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_ssh_3/)
     - OS: Ubuntu:20. 
     - Inherits from `ssh_base`.
     - Services: ssh, IRC, RethinkDB
- `telnet_1` ([telnet_1](./telnet_1)): an image with a Telnet server that can be used to generate containers vulnerable to brute-force attacks.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_telnet_1?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_telnet_1/)
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh, Flask server, telnet
- `telnet_2` ([telnet_2](./telnet_2)): an image with a Telnet server that can be used to generate containers vulnerable to brute-force attacks.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_telnet_2?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_telnet_2/)
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh, telnet, CockroachDB
- `telnet_3` ([telnet_3](./telnet_3)): an image with a Telnet server that can be used to generate containers vulnerable to brute-force attacks.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_telnet_3?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_telnet_3/)
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh, Glassfish, telnet
- `honeypot_1` ([honeypot_1](./honeypot_1)): an image with a set of arbitrary network services that can be used to generate honeypot containers.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_honeypot_1?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_honeypot_1/)
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh, IRC, SNMP, SMTP, PostgreSQL, NTP
- `honeypot_2` ([honeypot_2](./honeypot_2)): an image with a set of arbitrary network services that can be used to generate honeypot containers.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_honeypot_2?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_honeypot_2/)
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh, SNMP, PostgreSQL, IRC, NTP
- `router_1` ([router_1](./router_1)): an image without any particular services that can be used to generate containers acting as gateways.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_router_1?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_router_1/)
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh
- `router_2` ([router_2](./router_2)): an image with the Snort IDS that can be used to generate containers acting as gateways.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_router_2?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_router_2/)
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh, Snort
- `client_1` ([client_1](./client_1)): an image without any particular services that can be used to generate containers acting as clients.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_client_1?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_client_1/)
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh
- `blank_1` ([blank_1](./blank_1)): a blank image for testing purposes
    - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_blank_1?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_blank_1/)
    - OS: Ubuntu:20. 
    - Inherits from `blank_ubuntu_20`.
    - Services: None
- `blank_2` ([blank_2](./blank_2)): a blank image for testing purposes
    - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_blank_2?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_blank_2/)
    - OS: Ubuntu:22.
    - Inherits from `blank_ubuntu_22`.
    - Services: None  
- `pengine_exploit_1` ([pengine_exploit_1](./pengine_exploit_1)): an image with a vulnerable Prolog SLD Pengine Server
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_pengine_exploit_1?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_pengine_exploit_1/)
     - OS: Ubuntu:20. 
     - Inherits from `pengine_exploit_base`.
     - Services: Pengine server, SSH
- `ovs_1` ([ovs_1](./ovs_1)): an image with a OVS virtual switch
    - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_ovs_1?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_ovs_1/)
    - OS: Ubuntu:20.
    - Inherits from `ovs_base`.
    - Services: OVS switch, SSH
- `ryu_1` ([ryu_1](./ryu_1)): an image with the Ryu SDN controller
    - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_ryu_1?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_ryu_1/)
    - OS: Ubuntu:20.
    - Inherits from `ryu_base`.
    - Services: Ryu SDN controller, SSH
- `elk_1` ([elk_1](./elk_1)): an image with the ELK stack
    - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_elk_1?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_elk_1/)
    - OS: Ubuntu:20.
    - Inherits from `elk_base`.
    - Services: Elastic search, Kibana, Logstash, SSH
- `kafka_1` ([kafka_1](./kafka_1)): an image with Kafka
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_kafka_1?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_kafka_1/)
     - OS: Ubuntu:20.
     - Inherits from `ubuntu_20_base`.
     - Services: Kafka, SSH
- `spark_1` ([spark_1](./spark_1)): an image with Spark
  - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_spark_1?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_spark_1/)
  - OS: Ubuntu:22.
  - Inherits from `spark_base`.
  - Services: Spark, SSH

## Useful commands

```bash
make rm-image # Delete all derived images
make build # Build all derived images
make all # Build all derived images
make pull # Pull all images
make push # Push all images

make samba_1 # Build samba_1
make shellshock_1 # Build shellshock_1
make sql_injection_1 # Build sql_injection_1
make debian_10_1 # Build debian_10_1
make cve_2015_3306_1 # Build cve_2015_3306_1
make cve_2015_1427_1 # Build cve_2015_1427_1
make cve_2016_10033_1 # Build cve_2016_10033_1
make cve_2010_0426_1 # Build cve_2010_0426_1
make cve_2015_5602_1 # Build cve_2010_0426_1
make ftp_1 # Build ftp_1
make ftp_2 # Build ftp_2
make hacker_kali_1 # Build hacker_kali_1
make honeypot_1 # Build honeypot_1
make honeypot_2 # Build honeypot_2
make router_1 # Build router_1
make router_2 # Build router_2
make ssh_1 # Build ssh_1
make ssh_2 # Build ssh_2
make ssh_3 # Build ssh_3
make telnet_1 # Build telnet_1
make telnet_2 # Build telnet_2
make telnet_3 # Build telnet_3
make client_1 # Build client_1
make blank_1 # Build blank_1
make blank_2 # Build blank_2
make pengine_exploit_1 # Build pengine_exploit_1
make ovs_1 # Build ovs_1
make ryu_1 # Build ryu_1
make elk_1 # Build elk_1
make kafka_1 # Build kafka_1
make spark_1 # Build spark_1

make rm_samba_1 # Remove samba_1
make rm_shellshock_1 # Remove shellshock_1
make rm_sql_injection_1 # Remove sql_injection_1
make rm_debian_10_1 # Remove debian_10_1
make rm_cve_2015_3306_1 # Remove cve_2015_3306_1
make rm_cve_2015_1427_1 # Remove cve_2015_1427_1
make rm_cve_2016_10033_1 # Remove cve_2016_10033_1
make rm_cve_2010_0426_1 # Remove cve_2010_0426_1
make rm_cve_2015_5602_1 # Remove cve_2010_0426_1
make rm_ftp_1 # Remove ftp_1
make rm_ftp_2 # Remove ftp_2
make rm_hacker_kali_1 # Remove hacker_kali_1
make rm_honeypot_1 # Remove honeypot_1
make rm_honeypot_2 # Remove honeypot_2
make rm_router_1 # Remove router_1
make rm_router_2 # Remove router_2
make rm_ssh_1 # Remove ssh_1
make rm_ssh_2 # Remove ssh_2
make rm_ssh_3 # Remove ssh_3
make rm_telnet_1 # Remove telnet_1
make rm_telnet_2 # Remove telnet_2
make rm_telnet_3 # Remove telnet_3
make rm_client_1 # Remove client_1
make rm_blank_1 # Remove blank_1
make rm_blank_2 # Remove blank_2
make rm_pengine_exploit_1 # Remove pengine_exploit_1
make rm_ovs_1 # Remove ovs_1
make rm_ryu_1 # Remove ryu_1
make rm_elk_1 # Remove elk_1
make rm_kafka_1 # Remove kafka_1
make rm_spark_1 # Remove spark_1

make push_samba_1 # Push samba_1 to DockerHub
make push_shellshock_1 # Push shellshock_1 to DockerHub
make push_sql_injection_1 # Push sql_injection_1 to DockerHub
make push_debian_10_1 # Push debian_10_1 to DockerHub
make push_cve_2015_3306_1 # Push cve_2015_3306_1 to DockerHub
make push_cve_2015_1427_1 # Push cve_2015_1427_1 to DockerHub
make push_cve_2016_10033_1 # Push cve_2016_10033_1 to DockerHub
make push_cve_2010_0426_1 # Push cve_2010_0426_1 to DockerHub
make push_cve_2015_5602_1 # Push cve_2010_0426_1 to DockerHub
make push_ftp_1 # Push ftp_1 to DockerHub
make push_ftp_2 # Push ftp_2 to DockerHub
make push_hacker_kali_1 # Push hacker_kali_1 to DockerHub
make push_honeypot_1 # Push honeypot_1 to DockerHub
make push_honeypot_2 # Push honeypot_2 to DockerHub
make push_router_1 # Push router_1 to DockerHub
make push_router_2 # Push router_2 to DockerHub
make push_ssh_1 # Push ssh_1 to DockerHub
make push_ssh_2 # Push ssh_2 to DockerHub
make push_ssh_3 # Push ssh_3 to DockerHub
make push_telnet_1 # Push telnet_1 to DockerHub
make push_telnet_2 # Push telnet_2 to DockerHub
make push_telnet_3 # Push telnet_3 to DockerHub
make push_client_1 # Push client_1 to DockerHub
make push_blank_2 # Push blank_2 to DockerHub
make push_pengine_exploit_1 # Push pengine_exploit_1 to DockerHub
make push_ovs_1 # Push ovs_1 to DockerHub
make push_ryu_1 # Push ryu_1 to DockerHub
make push_elk_1 # Push elk_1 to DockerHub
make push_kafka_1 # Push kafka_1 to DockerHub
make push_spark_1 # Push spark_1 to DockerHub

make pull_samba_1 # pull samba_1 from DockerHub
make pull_shellshock_1 # pull shellshock_1 from DockerHub
make pull_sql_injection_1 # pull sql_injection_1 from DockerHub
make pull_debian_10_1 # pull debian_10_1 from DockerHub
make pull_cve_2015_3306_1 # pull cve_2015_3306_1 from DockerHub
make pull_cve_2015_1427_1 # pull cve_2015_1427_1 from DockerHub
make pull_cve_2016_10033_1 # pull cve_2016_10033_1 from DockerHub
make pull_cve_2010_0426_1 # pull cve_2010_0426_1 from DockerHub
make pull_cve_2015_5602_1 # pull cve_2010_0426_1 from DockerHub
make pull_ftp_1 # pull ftp_1 from DockerHub
make pull_ftp_2 # pull ftp_2 from DockerHub
make pull_hacker_kali_1 # pull hacker_kali_1 from DockerHub
make pull_honeypot_1 # pull honeypot_1 from DockerHub
make pull_honeypot_2 # pull honeypot_2 from DockerHub
make pull_router_1 # pull router_1 from DockerHub
make pull_router_2 # pull router_2 from DockerHub
make pull_ssh_1 # pull ssh_1 from DockerHub
make pull_ssh_2 # pull ssh_2 from DockerHub
make pull_ssh_3 # pull ssh_3 from DockerHub
make pull_telnet_1 # pull telnet_1 from DockerHub
make pull_telnet_2 # pull telnet_2 from DockerHub
make pull_telnet_3 # pull telnet_3 from DockerHub
make pull_client_1 # pull client_1 from DockerHub
make pull_blank_2 # pull blank_2 from DockerHub
make pull_pengine_exploit_1 # pull pengine_exploit_1 from DockerHub
make pull_ovs_1 # pull ovs_1 from DockerHub
make pull_ryu_1 # pull ryu_1 from DockerHub
make pull_elk_1 # pull elk_1 from DockerHub
make pull_kafka_1 # pull kafka_1 from DockerHub
make pull_spark_1 # pull spark_1 from DockerHub

docker container ls --all # list all running containers
docker image ls --all # list all images
docker system prune # remove unused images and containers
docker container prune # remove stopped containers      
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](../../LICENSE.md)

Creative Commons

(C) 2020-2025, Kim Hammar