# Base Images

This directory contains the *base* Docker images used in `csle` when emulating computer infrastructures. 
These images contains base configurations of different operating systems and services that are used as base to define 
more specific Docker images.

## List of Base Images

- `cve_2010_0426_base` ([cve_2010_0426_base](./cve_2010_0426_base)): a base image for csle emulations with the CVE-2010-0426 vulnerability. 
     - OS: Debian:Jessie. 
     - Inherits from `debian_jessie_base`.
- `cve_2015_1427_base` ([cve_2015_1427_base](./cve_2015_1427_base)): a base image for csle emulations with the CVE-2015-1427 vulnerability. 
     - OS: Debian:Jessie. 
     - Inherits from `debian_jessie_base`.
- `cve_2015_3306_base` ([cve_2015_3306_base](./cve_2015_3306_base)): a base image for csle emulations with the CVE-2015-3306 vulnerability. 
     - OS: Debian:Jessie. 
     - Inherits from `debian_jessie_base`.
- `cve_2015_5602_base` ([cve_2015_5602_base](./cve_2015_5602_base)): a base image for csle emulations with the CVE-2015-5602 vulnerability. 
     - OS: Debian:Jessie. 
     - Inherits from `debian_jessie_base`.
- `cve_2016_10033_base` ([cve_2016_10033_base](./cve_2016_10033_base)): a base image for csle emulations with the CVE-2016-10033 vulnerability.
     - OS: Debian:Jessie. 
     - Inherits from `debian_jessie_base`.
- `debian_jessie_base` ([debian_jessie_base](./debian_jessie_base)): a base debian image for csle emulations. 
     - OS: Debian:Jessie.
- `kali_base` ([kali_base](./kali_base)): a base Kali image for csle emulations, used to generate containers with tools for penetration testing. 
     - OS: Kali (Latest).
- `samba_base` ([samba_base](./samba_base)): a base image for csle emulations with the SambaCry CVE-2017-7494 vulnerability. 
     - OS: Debian:Jessie.
- `shellshock_base` ([shellshock_base](./shellshock_base)): a base image for csle emulations with the ShellShock CVE-2014-6271 vulnerability. 
     - OS: Debian:Wheezy.
- `sql_injection_base` ([sql_injection_base](./sql_injection_base)): a base image for csle emulations with a webapp that is vulnerable to SQL injections. 
     - OS: Debian:9.2.
- `ssh_base` ([ssh_base](./ssh_base)): a base image for csle emulations with a SSH server that accepts arbitrary login attempts logins. 
     - OS: Ubuntu:20.
- `ubuntu_14_base` ([ubuntu_14_base](./ubuntu_14_base)): a base image for csle emulations with Ubuntu 14. 
     - OS: Ubuntu:14.
- `ubuntu_20_base` ([ubuntu_20_base](./ubuntu_20_base)): a base image for csle emulations with Ubuntu 20. 
     - OS: Ubuntu:20.
- `blank_ubuntu_20` ([blank_ubuntu_20](./blank_ubuntu_20)): a plain base image with Ubuntu 20. 
     - OS: Ubuntu:20.
- `pengine_exploit_base` ([pengine_exploit_base](./pengine_exploit_base)): a base image with a vulnerable prolog SLD pengine server 
     - OS: Ubuntu:20.      

## Useful commands

```bash
make rm-image # Delete all base images
make build # Build all base images
make all # Build all base images

make kali_base # Build kali_base
make ubuntu_20_base # Build ubuntu_20_base
make ubuntu_14_base # Build ubuntu_14_base
make ssh_base # Build ssh_base
make samba_base # Build samba_base
make shellshock_base # Build shellshock_base
make sql_injection_base # Build sql_injection_base
make debian_jessie_base # Build debian_jessie_base
make cve_2015_3306_base # Build cve_2015_3306_base
make cve_2015_1427_base # Build cve_2015_1427_base
make cve_2016_10033_base # Build cve_2016_10033_base
make cve_2010_0426_base # Build cve_2010_0426_base
make cve_2015_5602_base # Build cve_2010_0426_base
make blank_ubuntu_20 # Build blank_ubuntu_20
make pengine_exploit_base # Build pengine_exploit_base

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

(C) 2022, Kim Hammar