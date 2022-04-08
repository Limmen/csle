# Derived Images

This directory contains derived Docker images used in `csle` when emulating computer infrastructures. 
These images are derivations of the [base images](../base_images) of `csle`. The derived images include
kali images, vulnerable images, and images with general network services. These images can be used to 
generate containers for emulating various network infrastructures.

## List of Derived Images

- `cve_2010_0426_1` ([cve_2010_0426_1](./cve_2010_0426_1)): an image with the CVE-2010-0426 vulnerability. 
     - OS: Debian:Jessie. 
     - Inherits from `cve_2010_0426_base`.
     - Services: teamspeak3, tomcat, ssh
- `cve_2015_1427_1` ([cve_2015_1427_1](./cve_2015_1427_1)): an image with the CVE-2015-1427 vulnerability. 
     - OS: Debian:Jessie. 
     - Inherits from `cve_2015_1427_base`.
     - Services: SNMP, elasticsearch, apache webserver, ssh
- `cve_2015_3306_1` ([cve_2015_3306_1](./cve_2015_3306_1)): an image with the CVE-2015-3306 vulnerability. 
     - OS: Debian:Jessie. 
     - Inherits from `cve_2015_3306_base`.
     - Services: ssh, SNMP, proftpd, apache2
- `cve_2015_5602_1` ([cve_2015_5602_1](./cve_2015_5602_1)): an image with the CVE-2015-5602 vulnerability. 
     - OS: Debian:Jessie. 
     - Inherits from `cve_2015_5602_base`.
     - Services: ssh
- `cve_2016_10033_1` ([cve_2016_10033_1](./cve_2016_10033_1)): an image with the CVE-2016-10033 vulnerability. 
     - OS: Debian:Jessie. 
     - Inherits from `cve_2010_0426_1`.
     - Services: ssh, apache2, SMTPD
- `hacker_kali_1` ([hacker_kali_1](./hacker_kali_1)): a Kali image, used to generate containers with tools for penetration testing. 
     - OS: Kali (Latest). 
     - Inherits from `kali_base`.
     - Services: ssh
- `samba_1` ([samba_1](./samba_1)): an image with the SambaCry CVE-2017-7494 vulnerabilitiy. 
     - OS: Debian:Jessie. 
     - Inherits from `samba_base`.
     - Services: ssh, NTP, samba
- `samba_2` ([samba_1](./samba_1)): an image with the SambaCry CVE-2017-7494 vulnerabilitiy and a telnet server. 
     - OS: Debian:Jessie. 
     - Inherits from `samba_base`.
     - Services: ssh, NTP, samba, telnet     
- `shellshock_1` ([shellshock_1](./shellshock_1)): an image with the ShellShock CVE-2014-6271 vulnerabilitiy. 
     - OS: Debian:Wheezy. 
     - Inherits from `shellshock_base`.
     - Services: ssh, SNMP, apache2
- `sql_injection_1` ([sql_injection_1](./sql_injection_1)): an image with a webapp that is vulnerable to SQL injections. 
     - OS: Debian:9.2. 
     - Inherits from `sql_injection_base`.
     - Services: IRC, apache2, ssh
- `ftp_1` ([ftp_1](./ftp_1)): an image with a FTP server that can be used to generate containers vulnerable to brute-force attacks. 
     - OS: Ubuntu:14. 
     - Inherits from `ubuntu_14_base`.
     - Services: VSFTPD, MongoDB, SMTP, tomcat, teamspeak3, ssh
- `ftp_2` ([ftp_2](./ftp_2)): an image with a FTP server that can be used to generate containers vulnerable to brute-force attacks. 
     - OS: Ubuntu:14. 
     - Inherits from `ubuntu_14_base`.
     - Services: VSFTPD, ssh, DNS
- `ssh_1` ([ssh_1](./ssh_1)): an image with a SSH server that can be used to generate containers vulnerable to brute-force attacks. 
     - OS: Ubuntu:20. 
     - Inherits from `ssh_base`.
     - Services: ssh, erl_pengine webapp, DNS
- `ssh_2` ([ssh_2](./ssh_2)): an image with a SSH server that can be used to generate containers vulnerable to brute-force attacks. 
     - OS: Ubuntu:20. 
     - Inherits from `ssh_base`.
     - Services: ssh, DNS, NTP
- `ssh_3` ([ssh_3](./ssh_3)): an image with a SSH server that can be used to generate containers vulnerable to brute-force attacks. 
     - OS: Ubuntu:20. 
     - Inherits from `ssh_base`.
     - Services: ssh, IRC, RethinkDB
- `telnet_1` ([telnet_1](./telnet_1)): an image with a Telnet server that can be used to generate containers vulnerable to brute-force attacks. 
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh, Flask server, telnet
- `telnet_2` ([telnet_2](./telnet_2)): an image with a Telnet server that can be used to generate containers vulnerable to brute-force attacks. 
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh, telnet, CockroachDB
- `telnet_3` ([telnet_3](./telnet_3)): an image with a Telnet server that can be used to generate containers vulnerable to brute-force attacks. 
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh, Glassfish, telnet
- `honeypot_1` ([honeypot_1](./honeypot_1)): an image with a set of arbitrary network services that can be used to generate honeypot containers. 
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh, IRC, SNMP, SMTP, PostgreSQL, NTP
- `honeypot_2` ([honeypot_2](./honeypot_2)): an image with a set of arbitrary network services that can be used to generate honeypot containers. 
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh, SNMP, PostgreSQL, IRC, NTP
- `router_1` ([router_1](./router_1)): an image without any particular services that can be used to generate containers acting as gateways. 
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh
- `router_2` ([router_2](./router_1)): an image with the Snort IDS that can be used to generate containers acting as gateways. 
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh, Snort
- `client_1` ([client_1](./client_1)): an image without any particular services that can be used to generate containers acting as clients. 
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh
 - `blank_1` ([blank_1](./blank_1)): a blank image for testing purposes 
     - OS: Ubuntu:20. 
     - Inherits from `blank_ubuntu_20`.
     - Services: None
- `pengine_exploit_1` ([pengine_exploit_1](./pengine_exploit_1)): an image with a vulnerable Prolog SLD Pengine Server 
     - OS: Ubuntu:20. 
     - Inherits from `pengine_exploit_base`.
     - Services: Pengine server, SSH

## Useful commands

```bash
make rm-image # Delete all base images
make build # Build all base images
make all # Build all base images

make samba_1 # Build samba_1
make shellshock_1 # Build shellshock_1
make sql_injection_1 # Build sql_injection_1
make debian_jessie_base # Build debian_jessie_1
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
make pengine_exploit_1 # Build pengine_exploit_1

make rm_samba_1 # Remove samba_1
make rm_shellshock_1 # Remove shellshock_1
make rm_sql_injection_1 # Remove sql_injection_1
make rm_debian_jessie_base # Remove debian_jessie_1
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
make rm_pengine_exploit_1 # Remove pengine_exploit_1

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

(C) 2020-2022, Kim Hammar