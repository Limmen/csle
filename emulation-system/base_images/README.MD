# Base Images

This directory contains the *base* Docker images used in `csle` when emulating computer infrastructures. 
These images contains base configurations of different operating systems and services that are used as base to define 
more specific Docker images.

## List of Base Images

- `cve_2010_0426_base` ([cve_2010_0426_base](./docker_files/cve_2010_0426_base)): a base image for csle emulations with the CVE-2010-0426 vulnerability.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_cve_2010_0426_base?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_cve_2010_0426_base/)
     - OS: Debian:10.2. 
     - Inherits from `debian_10_base`.
- `cve_2015_1427_base` ([cve_2015_1427_base](./docker_files/cve_2015_1427_base)): a base image for csle emulations with the CVE-2015-1427 vulnerability.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_cve_2015_1427_base?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_cve_2015_1427_base/)
     - OS: Debian:10.2. 
     - Inherits from `debian_10_base`.
- `cve_2015_3306_base` ([cve_2015_3306_base](./docker_files/cve_2015_3306_base)): a base image for csle emulations with the CVE-2015-3306 vulnerability.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_cve_2015_3306_base?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_csle_cve_2010_0426_1/)
     - OS: Debian:10.2. 
     - Inherits from `debian_10_base`.
- `cve_2015_5602_base` ([cve_2015_5602_base](./docker_files/cve_2015_5602_base)): a base image for csle emulations with the CVE-2015-5602 vulnerability.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_cve_2015_5602_base?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_cve_2015_5602_base/)
     - OS: Debian:10.2. 
     - Inherits from `debian_10_base`.
- `cve_2016_10033_base` ([cve_2016_10033_base](./docker_files/cve_2016_10033_base)): a base image for csle emulations with the CVE-2016-10033 vulnerability.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_cve_2016_10033_base?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_cve_2016_10033_base/)
     - OS: Debian:10.2. 
     - Inherits from `debian_10_base`.
- `debian_10_base` ([debian_10_base](./docker_files/debian_10_base)): a base debian image for csle emulations.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_debian_10_base?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_debian_10_base/)
     - OS: Debian:10.2.
- `kali_base` ([kali_base](./docker_files/kali_base)): a base Kali image for csle emulations, used to generate containers with tools for penetration testing.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_kali_base?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_kali_base/)
     - OS: Kali (Latest).
- `samba_base` ([samba_base](./docker_files/samba_base)): a base image for csle emulations with the SambaCry CVE-2017-7494 vulnerability.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_samba_base?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_samba_base/)
     - OS: Debian:10.2.
- `shellshock_base` ([shellshock_base](./docker_files/shellshock_base)): a base image for csle emulations with the ShellShock CVE-2014-6271 vulnerability.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_shellshock_base?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_shellshock_base/)
     - OS: Ubuntu:14.
- `shellshock_debian_wheezy_base` ([shellshock_base](./docker_files/shellshock_debian_wheezy_base)): a base image for csle emulations with the ShellShock CVE-2014-6271 vulnerability. 
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_shellshock_debian_wheezy_base?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_shellshock_debian_wheezy_base/)
     - OS: Debian:Wheezy.
- `sql_injection_base` ([sql_injection_base](./docker_files/sql_injection_base)): a base image for csle emulations with a webapp that is vulnerable to SQL injections.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_sql_injection_base?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_sql_injection_base/)
     - OS: Debian:9.2.
- `ssh_base` ([ssh_base](./docker_files/ssh_base)): a base image for csle emulations with a SSH server that accepts arbitrary login attempts logins.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_ssh_base?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_ssh_base/)
     - OS: Ubuntu:20.
- `ubuntu_14_base` ([ubuntu_14_base](./docker_files/ubuntu_14_base)): a base image for csle emulations with Ubuntu 14.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_ubuntu_14_base?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_ubuntu_14_base/)
     - OS: Ubuntu:14.
- `ubuntu_20_base` ([ubuntu_20_base](./docker_files/ubuntu_20_base)): a base image for csle emulations with Ubuntu 20.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_ubuntu_20_base?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_ubuntu_20_base/)
     - OS: Ubuntu:20.
- `ubuntu_22_base` ([ubuntu_22_base](./docker_files/ubuntu_22_base)): a base image for csle emulations with Ubuntu 22.
    - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_ubuntu_22_base?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_ubuntu_22_base/)
    - OS: Ubuntu:22.
- `blank_ubuntu_20` ([blank_ubuntu_20](./docker_files/blank_ubuntu_20)): a plain base image with Ubuntu 20.
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_blank_ubuntu_20?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_blank_ubuntu_20/)
     - OS: Ubuntu:20.
- `blank_ubuntu_22` ([blank_ubuntu_22](./docker_files/blank_ubuntu_22)): a plain base image with Ubuntu 22.
    - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_blank_ubuntu_22?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_blank_ubuntu_22/)
    - OS: Ubuntu:22.  
- `pengine_exploit_base` ([pengine_exploit_base](./docker_files/pengine_exploit_base)): a base image with a vulnerable prolog SLD pengine server
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_pengine_exploit_base?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_pengine_exploit_base/)
     - OS: Ubuntu:20.      
- `ovs_base` ([ovs_base](./docker_files/ovs_base)): a base image with a Open virtual Switch (OVS)
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_ovs_base?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_ovs_base/)
     - OS: Ubuntu:20.
     - Inherits from `ubuntu_20_base`
- `ryu_base` ([ryu_base](./docker_files/ryu_base)): a base image with the Ryu SDN controller
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_ryu_base?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_ryu_base/)
     - OS: Ubuntu:20.
     - Inherits from `ubuntu_20_base`
- `elk_base` ([elk_base](./docker_files/elk_base)): a base image with the ELK stack
     - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_elk_base?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_elk_base/)
     - OS: Ubuntu:20.
- `spark_base` ([spark_base](./docker_files/spark_base)): a base image with Spark
  - [![Docker Pulls](https://badgen.net/docker/pulls/kimham/csle_spark_base?icon=docker&label=pulls)](https://hub.docker.com/r/kimham/csle_spark_base/)
  - OS: Ubuntu:22.

## Useful commands

```bash
make rm-image # Delete all base images
make build # Build all base images
make all # Build all base images
make push # Push all base images to DockerHub
make pull # Pull all base images from DockerHub

make kali_base # Build kali_base
make ubuntu_20_base # Build ubuntu_20_base
make ubuntu_22_base # Build ubuntu_22_base
make ubuntu_14_base # Build ubuntu_14_base
make ssh_base # Build ssh_base
make samba_base # Build samba_base
make shellshock_base # Build shellshock_base
make shellshock_debian_wheezy_base # Build shellshock_base
make sql_injection_base # Build sql_injection_base
make debian_10_base # Build debian_10_base
make cve_2015_3306_base # Build cve_2015_3306_base
make cve_2015_1427_base # Build cve_2015_1427_base
make cve_2016_10033_base # Build cve_2016_10033_base
make cve_2010_0426_base # Build cve_2010_0426_base
make cve_2015_5602_base # Build cve_2010_0426_base
make blank_ubuntu_20 # Build blank_ubuntu_20
make blank_ubuntu_22 # Build blank_ubuntu_22
make pengine_exploit_base # Build pengine_exploit_base
make ovs_base # Build ovs_base
make ryu_base # Build ryu_base
make elk_base # Build elk_base
make spark_base # Build elk_base

make rm_kali_base # Remove kali_base
make rm_ubuntu_20_base # Remove ubuntu_20_base
make rm_ubuntu_22_base # Remove ubuntu_22_base
make rm_ubuntu_14_base # Remove ubuntu_14_base
make rm_ssh_base # Remove ssh_base
make rm_samba_base # Remove samba_base
make rm_shellshock_base # Remove shellshock_base
make rm_shellshock_debian_wheezy_base # Remove shellshock_base
make rm_sql_injection_base # Remove sql_injection_base
make rm_debian_10_base # Remove debian_10_base
make rm_cve_2015_3306_base # Remove cve_2015_3306_base
make rm_cve_2015_1427_base # Remove cve_2015_1427_base
make rm_cve_2016_10033_base # Remove cve_2016_10033_base
make rm_cve_2010_0426_base # Remove cve_2010_0426_base
make rm_cve_2015_5602_base # Remove cve_2010_0426_base
make rm_blank_ubuntu_20 # Remove blank_ubuntu_20
make rm_blank_ubuntu_22 # Remove blank_ubuntu_22
make rm_pengine_exploit_base # Remove pengine_exploit_base
make rm_ovs_base # Remove ovs_base
make rm_ryu_base # Remove ryu_base
make rm_elk_base # Remove elk_base
make rm_spark_base # Remove spark_base

make push_kali_base # Push kali_base to DockerHub
make push_ubuntu_20_base # Push ubuntu_20_base to DockerHub
make push_ubuntu_22_base # Push ubuntu_22_base to DockerHub
make push_ubuntu_14_base # Push ubuntu_14_base to DockerHub
make push_ssh_base # Push ssh_base to DockerHub
make push_samba_base # Push samba_base to DockerHub
make push_shellshock_base # Push shellshock_base to DockerHub
make push_shellshock_debian_wheezy_base # Push shellshock_base to DockerHub
make push_sql_injection_base # Push sql_injection_base to DockerHub
make push_debian_10_base # Push debian_10_base to DockerHub
make push_cve_2015_3306_base # Push cve_2015_3306_base to DockerHub
make push_cve_2015_1427_base # Push cve_2015_1427_base to DockerHub
make push_cve_2016_10033_base # Push cve_2016_10033_base to DockerHub
make push_cve_2010_0426_base # Push cve_2010_0426_base to DockerHub
make push_cve_2015_5602_base # Push cve_2010_0426_base to DockerHub
make push_blank_ubuntu_20 # Push blank_ubuntu_20 to DockerHub
make push_blank_ubuntu_22 # Push blank_ubuntu_22 to DockerHub
make push_pengine_exploit_base # Push pengine_exploit_base to DockerHub
make push_ovs_base # Push ovs_base to DockerHub
make push_ryu_base # Push ryu_base to DockerHub
make push_elk_base # Push elk_base to DockerHub
make push_spark_base # Push spark_base to DockerHub

make pull_kali_base # pull kali_base from DockerHub
make pull_ubuntu_20_base # pull ubuntu_20_base from DockerHub
make pull_ubuntu_22_base # pull ubuntu_22 _base from DockerHub
make pull_ubuntu_14_base # pull ubuntu_14_base from DockerHub
make pull_ssh_base # pull ssh_base from DockerHub
make pull_samba_base # pull samba_base from DockerHub
make pull_shellshock_base # pull shellshock_base from DockerHub
make pull_shellshock_debian_wheezy_base # pull shellshock_base from DockerHub
make pull_sql_injection_base # pull sql_injection_base from DockerHub
make pull_debian_10_base # pull debian_10_base from DockerHub
make pull_cve_2015_3306_base # pull cve_2015_3306_base from DockerHub
make pull_cve_2015_1427_base # pull cve_2015_1427_base from DockerHub
make pull_cve_2016_10033_base # pull cve_2016_10033_base from DockerHub
make pull_cve_2010_0426_base # pull cve_2010_0426_base from DockerHub
make pull_cve_2015_5602_base # pull cve_2010_0426_base from DockerHub
make pull_blank_ubuntu_20 # pull blank_ubuntu_20 from DockerHub
make pull_blank_ubuntu_22 # pull blank_ubuntu_22 from DockerHub
make pull_pengine_exploit_base # pull pengine_exploit_base from DockerHub
make pull_ovs_base # pull ovs_base from DockerHub
make pull_ryu_base # pull ryu_base from DockerHub
make pull_elk_base # pull elk_base from DockerHub
make pull_spark_base # pull spark_base from DockerHub

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