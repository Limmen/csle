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
- `hacker_kali1` ([hacker_kali1](./hacker_kali1)): a Kali image, used to generate containers with tools for penetration testing. 
     - OS: Kali (Latest). 
     - Inherits from `kali_base`.
     - Services: ssh
- `samba1` ([samba1](./samba1)): an image with the SambaCry CVE-2017-7494 vulnerabilitiy. 
     - OS: Debian:Jessie. 
     - Inherits from `samba_base`.
     - Services: ssh, NTP, samba
- `samba2` ([samba1](./samba1)): an image with the SambaCry CVE-2017-7494 vulnerabilitiy and a telnet server. 
     - OS: Debian:Jessie. 
     - Inherits from `samba_base`.
     - Services: ssh, NTP, samba, telnet     
- `shellshock1` ([shellshock1](./shellshock1)): an image with the ShellShock CVE-2014-6271 vulnerabilitiy. 
     - OS: Debian:Wheezy. 
     - Inherits from `shellshock_base`.
     - Services: ssh, SNMP, apache2
- `sql_injection1` ([sql_injection1](./sql_injection1)): an image with a webapp that is vulnerable to SQL injections. 
     - OS: Debian:9.2. 
     - Inherits from `sql_injection_base`.
     - Services: IRC, apache2, ssh
- `ftp1` ([ftp1](./ftp1)): an image with a FTP server that can be used to generate containers vulnerable to brute-force attacks. 
     - OS: Ubuntu:14. 
     - Inherits from `ubuntu_14_base`.
     - Services: VSFTPD, MongoDB, SMTP, tomcat, teamspeak3, ssh
- `ftp2` ([ftp2](./ftp2)): an image with a FTP server that can be used to generate containers vulnerable to brute-force attacks. 
     - OS: Ubuntu:14. 
     - Inherits from `ubuntu_14_base`.
     - Services: VSFTPD, ssh, DNS
- `ssh1` ([ssh1](./ssh1)): an image with a SSH server that can be used to generate containers vulnerable to brute-force attacks. 
     - OS: Ubuntu:20. 
     - Inherits from `ssh_base`.
     - Services: ssh, erl_pengine webapp, DNS
- `ssh2` ([ssh2](./ssh2)): an image with a SSH server that can be used to generate containers vulnerable to brute-force attacks. 
     - OS: Ubuntu:20. 
     - Inherits from `ssh_base`.
     - Services: ssh, DNS, NTP
- `ssh3` ([ssh3](./ssh3)): an image with a SSH server that can be used to generate containers vulnerable to brute-force attacks. 
     - OS: Ubuntu:20. 
     - Inherits from `ssh_base`.
     - Services: ssh, IRC, RethinkDB
- `telnet1` ([telnet1](./telnet1)): an image with a Telnet server that can be used to generate containers vulnerable to brute-force attacks. 
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh, Flask server, telnet
- `telnet2` ([telnet2](./telnet2)): an image with a Telnet server that can be used to generate containers vulnerable to brute-force attacks. 
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh, telnet, CockroachDB
- `telnet3` ([telnet3](./telnet3)): an image with a Telnet server that can be used to generate containers vulnerable to brute-force attacks. 
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh, Glassfish, telnet
- `honeypot1` ([honeypot1](./honeypot1)): an image with a set of arbitrary network services that can be used to generate honeypot containers. 
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh, IRC, SNMP, SMTP, PostgreSQL, NTP
- `honeypot2` ([honeypot2](./honeypot2)): an image with a set of arbitrary network services that can be used to generate honeypot containers. 
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh, SNMP, PostgreSQL, IRC, NTP
- `router1` ([router1](./router1)): an image without any particular services that can be used to generate containers acting as gateways. 
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh
- `router2` ([router2](./router1)): an image with the Snort IDS that can be used to generate containers acting as gateways. 
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh, Snort
- `client1` ([client1](./client1)): an image without any particular services that can be used to generate containers acting as clients. 
     - OS: Ubuntu:20. 
     - Inherits from `ubuntu_20_base`.
     - Services: ssh
 - `blank1` ([blank1](./blank1)): a blank image for testing purposes 
     - OS: Ubuntu:20. 
     - Inherits from `blank_ubuntu_20`.
     - Services: None
- `pengine_exploit1` ([pengine_exploit1](./pengine_exploit1)): an image with a vulnerable Prolog SLD Pengine Server 
     - OS: Ubuntu:20. 
     - Inherits from `pengine_exploit_base`.
     - Services: Pengine server, SSH

## Useful commands

```bash
make rm-image # Delete all base images
make build # Build all base images
make all # Build all base images

make samba1 # Build samba1
make shellshock1 # Build shellshock1
make sql_injection1 # Build sql_injection1
make debian_jessie_base # Build debian_jessie_1
make cve_2015_3306_1 # Build cve_2015_3306_1
make cve_2015_1427_1 # Build cve_2015_1427_1
make cve_2016_10033_1 # Build cve_2016_10033_1
make cve_2010_0426_1 # Build cve_2010_0426_1
make cve_2015_5602_1 # Build cve_2010_0426_1
make ftp1 # Build ftp1
make ftp2 # Build ftp2
make hacker_kali1 # Build hacker_kali1
make honeypot1 # Build honeypot1
make honeypot2 # Build honeypot2
make router1 # Build router1
make router2 # Build router2
make ssh1 # Build ssh1
make ssh2 # Build ssh2
make ssh3 # Build ssh3
make telnet1 # Build telnet1
make telnet2 # Build telnet2
make telnet3 # Build telnet3
make client1 # Build client1
make blank1 # Build blank1
make pengine_exploit1 # Build pengine_exploit1

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

(C) 2020, Kim Hammar