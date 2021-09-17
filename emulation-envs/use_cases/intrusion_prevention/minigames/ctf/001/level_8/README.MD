# Capture the Flag - Level 8

A virtual environment with a set of nodes that run common networked services such as SSH, FTP, Telnet, IRC, Kafka, 
Cassandra, etc. Some of the services are vulnerable to different network attacks such as the SambaCry exploit, Shellshock, CVE-2015-1427, CVE-2015-3306, CVE-2016-100033_1,and SQL injection. 
Moreover, some nodes are vulnerable to privilege escalation attacks (e.g. CVE-2010-0426 and CVE-2015-5602) which can be used by the attacker to extend his privileges after compromising the host.    
The task of an attacker agent is to identify the vulnerabilities and exploit them and discover hidden flags
on the nodes. Conversely, the task of the defender is to harden the defense of the nodes and to detect the 
attacker. 

- Number of nodes: 27
- IDS: Yes (Snort)
- Traffic generation: Yes
- Number of flags: 22
- Vulnerabilities: SambaCry, Shellshock, CVE-2015-1427, CVE-2015-3306, CVE-2016-100033_1,and SQL injection., as well as SSH, FTP, Telnet servers that can be compromised using dictionary attacks

## Architecture

<p align="center">
<img src="env.png" width="600">
</p>

## Useful commands

```bash
make rm-image # Delete all built images
make build # Build all docker images
make clean # Stop all running containers
make run # Run all containers
make router # Run router container
make telnet # Run telnet container
make ssh_1 # Run 1st ssh container
make ssh_2 # Run 2nd ssh container
make ssh_3 # Run 3st ssh container
make ssh_4 # Run 4th ssh container
make honeypot_1 # Run 1st honeypot container
make honeypot_2 # Run 2nd honeypot container
make cve_2010_0426_1_1 # Run 1st container with the CVE-2010-0426 vulnerability
make cve_2010_0426_1_2 # Run 2nd container with the CVE-2010-0426 vulnerability
make cve_2015_1427_1_1 # Run 1st container with the CVE-2015-1427 vulnerability
make cve_2015_1427_1_2 # Run 2nd container with the CVE-2015-1427 vulnerability
make cve_2015_3306_1_1 # Run 1st container with the CVE-2015-3306 vulnerability
make cve_2015_3306_1_2 # Run 2nd container with the CVE-2015-3306 vulnerability
make cve_2015_5602_1_1 # Run 1st container with the CVE-2015-5602 vulnerability
make cve_2015_5602_1_2 # Run 2nd container with the CVE-2015-5602 vulnerability
make cve_2016_10033_1_1 # Run 1st container with the CVE-2016-10033 vulnerability
make cve_2016_10033_1_2 # Run 2nd container with the CVE-2016-10033 vulnerability
make samba1_1 # Run 1st container with th SambaCry vulnerability
make samba1_2 # Run 2nd container with th SambaCry vulnerability
make shellshock1_1 # Run 1st container with the Shellshock vulnerability
make shellshock1_2 # Run 2nd container with the Shellshock vulnerability
make sql_injection1_1 # Run 1st container with a SQL Injection vulnerability
make sql_injection1_2 # Run 2nd container with a SQL Injection vulnerability 
make net # Create Docker sub-network
make rm-net # Remove Docker sub-network
make traffic # create traffic generators and start them on each node
make stop_traffic # stop traffic_generators that are running on each node
python run.py --build # build all containers with custom config
python run.py --run # run all containers with custom config
docker container ls --all # list all running containers
docker image ls --all # list all images
docker system prune # remove unused images and containers
docker container prune # remove stopped containers
sudo useradd -rm -d /home/pycr_admin -s /bin/bash -g root -G sudo -p "$(openssl passwd -1 'pycr@admin-pw_191')" pycr_admin   
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](../../../../../../../LICENSE.md)

Creative Commons

(C) 2021, Kim Hammar