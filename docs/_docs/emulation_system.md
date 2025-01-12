---
title: Emulation System 
permalink: /docs/emulation-system/
---

## Emulation System

The emulation system uses a virtualization layer provided by Docker containers and virtual networks to emulate IT
infrastructures. An emulated IT infrastructure is defined by an *emulation configuration*, which includes the properties
listed in Table 2. The set of configurations supported by the emulation system are stored in the metastore and can be
seen as a *configuration space*, which defines the class of infrastructures that can be emulated (see Fig. 5).

<p align="center">
<img src="./../../img/config_space.png" width="45%">
<p class="captionFig">
Figure 5: The configuration space of the emulation system, 
which defines the class of infrastructures that the emulation system can emulate.
</p>
</p>

| *Configuration property*      | *Description*                                                     |
|-------------------------------|-------------------------------------------------------------------|
| `name`                        | The name of the emulation.                                        |
| `containers_config`           | Configuration of each container (ip, hostname, resources, etc.).  |
| `users_config`                | Configuration of user accounts on each container.                 |
| `flags_config`                | Configuration of flags on each container.                         |
| `vuln_config`                 | Configuration of vulnerabilities on each container.               |
| `topology_config`             | Configuration of the emulation's network topology.                |
| `traffic_config`              | Configuration of traffic generators and client population.        |
| `resources_config`            | Configuration of physical resources (CPU, memory, etc.).          |
| `services_config`             | Configuration of services running on each container.              |
| `descr`                       | Description of the emulation.                                     |
| `static_attacker_sequences`   | Configuration of pre-defined attacker sequences.                  |
| `ovs_config`                  | Configuration of Open vSwitches (virtual OpenFlow switches).      |
| `sdn_controller_config`       | Configuration of SDN controllers.                                 |
| `host_manager_config`         | Configuration of host managers.                                   |
| `snort_ids_manager_config`    | Configuration of Snort IDS managers.                              |
| `ossec_ids_manager_config`    | Configuration of OSSEC IDS managers.                              |
| `docker_stats_manager_config` | Configuration of Docker stats managers.                           |
| `beats_config`                | Configuration of filebeats, packetbeats, etc.                     |
| `elk_config`                  | Configuration of the ELK stack in the management network.         |
| `level`                       | Level of the emulation.                                           |
| `version`                     | Version of the emulation.                                         |
| `execution_id`                | ID of the execution that the emulation belongs to (if any).       |
| `csle_collector_version`      | Version of the `csle-collector` library.                          |
| `csle_ryu_version`            | Verion of the `csle-ryu` library.                                 |

<p class="captionFig">
Table 2: Properties of an emulation configuration.
</p>

Users of CSLE can create new emulation configurations and insert them into the metastore. CSLE also includes a set of
pre-installed configurations
(see Table 3). One of these pre-installed configurations is `csle-level9-070` (as an example), whose topology is shown
in Fig. 6 and whose configuration is listed in Table 4.


| *Emulation configuration* | *Description*                                                                   |
|---------------------------|---------------------------------------------------------------------------------|
| `csle-level1-070`         | Emulation with 7 components, 3 flags, password vulnerabilities, no IDS.         |
| `csle-level2-070`         | Emulation with 13 components, 6 flags, password vulnerabilities, no IDS.        |
| `csle-level3-070`         | Emulation with 34 components, 6 flags, password vulnerabilities, no IDS.        |
| `csle-level4-070`         | Emulation with 7 components, 3 flags, password vulnerabilities, IDS.            |
| `csle-level5-070`         | Emulation with 13 components, 6 flags, password vulnerabilities, IDS.           |
| `csle-level6-070`         | Emulation with 34 components, 6 flags, password vulnerabilities, IDS.           |
| `csle-level7-070`         | Emulation with 7 components, 3 flags, password & RCE vulnerabilities, IDS.      |
| `csle-level8-070`         | Emulation with 13 components, 6 flags, password & RCE vulnerabilities, IDS.     |
| `csle-level9-070`         | Emulation with 34 components, 6 flags, password & RCE vulnerabilities, IDS.     |
| `csle-level10-070`        | Emulation with 16 components, 12 flags, password & RCE vulnerabilities, IDS.    |
| `csle-level11-070`        | Emulation with 36 components, 6 flags, password & RCE vulnerabilities, IDS.     |
| `csle-level12-070`        | Emulation with 7 components, 3 flags, password RCE vulnerabilities, IDS, SDN.   |
| `csle-level13-070`        | Emulation with 64 components, 6 flags, password RCE vulnerabilities, IDS, SDN.  |
| `csle-level14-070`        | Emulation with 17 components, 12 flags, password RCE vulnerabilities, IDS, SDN. |


<p class="captionFig">
Table 3: Pre-installed emulation configurations.
</p>

<p align="center">
<img src="./../../img/example_topology.png" width="30%">
<p class="captionFig">
Figure 6: Topology of the emulation configuration `csle-level9-070`
</p>
</p>

| *ID (s)*                  | *OS:Services:Exploitable Vulnerabilities*            |
|---------------------------|------------------------------------------------------|
| N1                        | Ubuntu20:Snort(community ruleset v2.9.17.1),SSH:-    |
| N2                        | Ubuntu20:SSH,HTTP Erl-Pengine,DNS:SSH-pw             |
| N4                        | Ubuntu20:HTTP Flask,Telnet,SSH:Telnet-pw             |
| N10                       | Ubuntu20:FTP,MongoDB,SMTP,Tomcat,TS3,SSH:FTP-pw      |
| N12                       | Deb10.2:TS3,Tomcat,SSH:CVE-2010-0426,SSH-pw          |
| N17                       | Wheezy:Apache2,SNMP,SSH:CVE-2014-6271                |
| N18                       | Deb10.2:IRC,Apache2,SSH:SQL Injection                |
| N22                       | Deb10.2:PROFTPD,SSH,Apache2,SNMP:CVE-2015-3306       |
| N23                       | Deb10.2:Apache2,SMTP,SSH:CVE-2016-10033              |
| N24                       | Deb10.2:SSH:CVE-2015-5602,SSH-pw                      |
| N25                       | Deb10.2: Elasticsearch,Apache2,SSH,SNMP:CVE-2015-1427 |
| N27                       | Deb10.2:Samba,NTP,SSH:CVE-2017-7494                   |
| N3,N11,N5-N9              | Ubuntu20:SSH,SNMP,PostgreSQL,NTP:-                   |
| N13-16,N19-21,N26,N28-31  | Ubuntu20:NTP, IRC, SNMP, SSH, PostgreSQL:-           |

<p class="captionFig">
Table 4: Configuration of the emulation configuration 
`csle-level9-070`, whose topology is shown in Fig. 6.
</p>

An *emulation execution* consists of a set of running containers and virtual networks, 
which are defined by an associated *emulation configuration*.

Creating an execution involves two main tasks of the emulation system. 
The first task is to replicate relevant parts of the physical infrastructure that is emulated, 
such as physical resources, operating systems, network interfaces, and network conditions. 
The second task is to instrument the emulated infrastructure with monitoring and management capabilities. 
Since the emulation execution will be used to evaluate reinforcement learning agents, 
it must be possible to monitor system metrics in real-time and to perform control 
actions prescribed by reinforcement learning agents.

In the following seven sections, we describe how the emulation system 
emulates physical hosts, network links, switches, network conditions, client populations, 
attackers, and defenders, respectively. In the subsequent three sections, 
we describe the monitoring and management capabilities of the emulation system. 
Lastly, we describe the process of creating an emulation execution from an emulation configuration.

### Emulating Physical Hosts

Physical hosts are emulated with Docker containers. 
A container is a lightweight executable package that includes everything needed to emulate the host: 
a runtime system, code, system tools, system libraries, and configurations. 
Multiple containers can run on the same physical host and share the same operating system kernel, 
in which case their resources and processes are isolated using cgroups 
(see Fig. 7).

<p align="center">
<img src="./../../img/virtualization.png" width="35%">
<p class="captionFig">
Figure 7: Software and hardware stack of a physical server that runs CSLE; 
closest to the hardware is the operating system; 
on top of the operating system is the Docker engine, 
which provides the base for running CSLE and virtual containers.
</p>
</p>

The CSLE Docker images are listed in Table 5 and include images for emulating application servers, 
Software-Defined Networking (SDN) controllers, clients, attackers, 
Intrusion Detection and Prevention Systems (IDPSs), and storage systems. 
Detailed configuration of each image is available <a href="https://hub.docker.com/r/kimham/">here</a>.

| *Name*               | *Description*                                   | *OS*          |
|----------------------|-------------------------------------------------|---------------|
| `cve_2010_0426_1`    | An image with the CVE-2010-0426 vulnerability.  | Debian:10.2   |
| `cve_2015_1427_1`    | An image with the CVE-2015-1427 vulnerability.  | Debian:10.2   |
| `cve_2015_3306_1`    | An image with the CVE-2015-3306 vulnerability.  | Debian:10.2   |
| `cve_2015_5602_1`    | An image with the CVE-2015-5602 vulnerability.  | Debian:10.2   |
| `cve_2016_10033_1`   | An image with the CVE-2016-10033 vulnerability. | Debian:10.2   |
| `hacker_kali_1`      | An image with tools for penetration testing.    | Kali          |
| `samba_1`            | An image with the CVE-2017-7494 vulnerability.  | Debian:10.2   |
| `samba_2`            | An image with the CVE-2017-7494 vulnerability.  | Debian:10.2   |
| `shellshock_1`       | An image with the CVE-2014-6271 vulnerability.  | Debian:Wheezy |
| `sql_injection_1`    | An image with SQL-injection vulnerability.      | Debian:10.2   |
| `ftp_1`              | An image with an FTP server.                    | Ubuntu:14     |
| `ftp_2`              | An image with an FTP server.                    | Ubuntu:14     |
| `ssh_1`              | An image with a SSH server.                     | Ubuntu:20     |
| `ssh_2`              | An image with a SSH server.                     | Ubuntu:20     |
| `ssh_3`              | An image with a SSH server.                     | Ubuntu:20     |
| `telnet_1`           | An image with a Telnet server.                  | Ubuntu:20     |
| `telnet_2`           | An image with a Telnet server.                  | Ubuntu:20     |
| `telnet_3`           | An image with a Telnet server.                  | Ubuntu:20     |
| `honeypot_1`         | An image with various honeypot services.        | Ubuntu:20     |
| `honeypot_2`         | An image with various honeypot services.        | Ubuntu:20     |
| `router_1`           | A blank image.                                  | Ubuntu:20     |
| `router_2`           | An image with the Snort IDPS.                   | Ubuntu:20     |
| `client_1`           | A blank image.                                  | Ubuntu:20     |
| `blank_1`            | A blank image.                                  | Ubuntu:20     |
| `pengine_exploit_1`  | An image with the pengine exploit.              | Ubuntu:20     |
| `ovs_1`              | An image with the OVS virtual switch.           | Ubuntu:20     |
| `ryu_1`              | An image with the Ryu SDN controller.           | Ubuntu:20     |
| `elk_1`              | An image with the ELK stack.                    | Ubuntu:20     |
| `kafka_1`            | An image with Kafka.                            | Ubuntu:20     |

<p class="captionFig">
Table 5: Docker images in CSLE.
</p>

### Emulating Physical Network Links

Network connectivity is emulated by virtual links implemented by Linux bridges. 
Network isolation between emulated hosts and emulated switches on the same physical 
host is achieved through network namespaces, which create logical copies of the 
physical host's network stack.

Each emulation execution has a dedicated virtual subnetwork with the subnet mask:
```bash
executionId.emulationId.0.0/16
```
where `executionID` identifies the execution and `emulationID` identifies the emulation configuration. 
This addressing scheme allows several executions of the same emulation configuration 
to execute concurrently on the same physical servers without overlapping address spaces.

In the case that an emulated network spans multiple physical servers of the management system, 
VXLAN connections are used. These connections tunnel the emulated network traffic over the 
physical network (see Fig. 8). In other words, the physical network that connects the servers of the 
management system provides a substrate network, 
on top of which the emulation system deploys virtual networks.

<p align="center">
<img src="./../../img/docker_network.png" width="75%">
<p class="captionFig">
Figure 8: Architecture diagram of a distributed emulation execution; 
servers of the management system are connected through a physical IP network, 
over which virtual networks are overlayed using VXLAN tunnels.
</p>
</p>

### Emulating Physical Switches

Physical switches are emulated with Docker containers that run Open vSwitch (OVS) version 2.16 (see Fig. 9). 
The emulated switches connect to an SDN controller using the OpenFlow protocol version 1.3 
over a secure TLS tunnel. 
The SDN controller is emulated by a container that resides in the management network 
(the management network is described below). 
(Since the switches are programmed through flow tables, they can act either as 
classical L2 switches or as routers, depending on the flow table configurations.)

<p align="center">
<img src="./../../img/openflow.png" width="50%">
<p class="captionFig">
Figure 9: Physical switches in CSLE are emulated as Open vSwitch (OVS) switches; 
each emulated switch runs the OpenFlow protocol and can be configured via 
a Software-Defined Networking (SDN) controller.
</p>
</p>

### Emulating Network Conditions

Network conditions of virtual links are configured using the NetEm module in the Linux kernel, 
which allows fine-gained configuration of bit rates, packet delays, packet loss probabilities, 
jitter, and packet reordering probabilities (see Fig. 10).

<p align="center">
<img src="./../../img/netem.png" width="35%">
<p class="captionFig">
Figure 10: Method to emulate network conditions with the Netem module in the Linux kernel; 
Netem uses a dedicted queueing discipline in the Linux networking stack and emulates bit rates, 
latencies, packet loss probabilities, packet reordering probabilities, 
and jitter according to a predefined configuration.
</p>
</p>

### Emulating Client Populations

Client populations in CSLE are emulated by processes that run inside Docker 
containers and interact with emulated hosts through various network protocols, 
e.g., HTTP, SSH, and DNS. The clients select functions from the list in 
Table 6 according to some probability distribution.

| *Function* | *Description*                                       |
|------------|-----------------------------------------------------|
| HTTP       | Download web pages and use REST APIs.               |
| SSH        | Connect to emulated components using SSH.           |
| SNMP       | Perform network management operations through SNMP. |
| ICMP       | Ping emulated components.                           |
| IRC        | Communicate with IRC servers.                       |
| PostgreSQL | Communicate with PostgreSQL servers.                |
| FTP        | Download and upload files to FTP servers.           |
| DNS        | Make DNS queries.                                   |
| Telnet     | Connect to emulated components using Telnet.        |

<p class="captionFig">
Table 6: Network functions that emulated clients may invoke.
</p>

Client arrivals are emulated by a Poisson process with exponentially distributed service times (see Fig. 11). 
This process may be stationary or non-stationary, e.g., it may be sine-modulated to 
model periodic load patterns. The duration of a time-step in an emulation is defined 
by its configuration; a typical duration is 30 seconds.

<p align="center">
<img src="./../../img/client_population.png" width="35%">
<p class="captionFig">
Figure 11: Clients are emulated by processes that invoke network functions of emulated hosts; 
client arrivals and service times are emulated by a Poisson process with exponentially 
distributed service times.
</p>
</p>

### Emulating Attackers

Attackers are emulated by automated programs that select actions from a pre-defined set. 
The actions are selected according to an *attacker strategy*, 
which may depend on system metrics of the emulation. 
(These metrics are collected in real-time by monitoring agents described below.) 
The attacker commands are listed in Table 7.

| *Type*             | *Actions*                                     |
|--------------------|-----------------------------------------------|
| Reconnaissance     | TCP-SYN scan, UDP port scan,                  |
|                    | TCP Null scan, TCP Xmas scan, TCP FIN scan,   |
|                    | ping-scan, TCP connection scan,               |
|                    | TCP-xmas-tree scan, OS-detection scan         |
|                    | "Vulscan" vulnerability scanner               |
|                    | "Vulners" vulnerability scanner               |
|                    | Nikto web scan, masscan                       |
|                    | firewall walk, HTTP-enum scan                 |
|                    | finger scan                                   |
|                    |                                               |
| Brute-force attack | Telnet, SSH, FTP, Cassandra,                  |
|                    | IRC, MongoDB, MySQL, SMTP, Postgres           |
|                    |                                               |
| Exploit            | CVE-2017-7494, CVE-2015-3306,                 |
|                    | CVE-2010-0426, CVE-2015-5602,                 |
|                    | CVE-2014-6271, CVE-2016-10033                 |
|                    | CVE-2015-1427, SQL Injection                  |

<p class="captionFig">
Table 7: Attacker commands.
</p>

### Emulating Defenders

Defender actions are emulated by executing system commands on emulated hosts. 
These commands are invoked through a management API based on gRPC and SSH (the API is detailed below). 
Similar to the attacker actions, 
the defender actions are prescribed by a *defender strategy*, 
which may depend on system metrics collected by monitoring agents (described below). 
The defender actions are listed in Table 8.

| *Index* | *Action*                                                        |
|---------|-----------------------------------------------------------------|
| 1       | Revoke user certificates.                                       |
| 2       | Blacklist IPs.                                                  |
| 3-37    | Drop traffic that generates IDPS alerts of priority $1-34$.     |
| 38      | Block gateway.                                                  |
| 39      | Server migration between different zones of the infrastructure. |
| 40      | Traffic redirect from one server to another.                    |
| 41      | Server isolation.                                               |
| 42      | Deploying new security functions (e.g., firewalls and IDPSs).    |
| 43      | Server shutdown.                                                |

<p class="captionFig">
Table 8: Defender commands.
</p>

### The Management Network

Each emulation execution has a dedicated virtual subnetwork, 
called the *management network*, which spans the following address space:
```bash
executionID.emulationID.253.0/24
```
This network interfaces directly with the management system and also has 
an interface to each emulated component. 
The purpose of this network is to connect management systems to the emulated devices, 
e.g., storage systems, monitoring systems, and SDN controllers (see Fig. 12). 
The reason for using a dedicated management network instead of carrying management traffic on 
the network that carries device-to-device traffic is to avoid interference and 
to simplify control of the execution.

<p align="center">
<img src="./../../img/management_network.png" width="45%">
<p class="captionFig">
Figure 12: The management network; it is a dedicated network used for operation of the emulated infrastructure.
</p>
</p>

### Monitoring Agents

Each emulated device runs a *monitoring agent* that reads local metrics of the device and 
pushes those metrics to a distributed Kafka queue, which is deployed inside 
the management network (see Fig. 13). 
The metrics collected at every time-step are listed in 
Tables 10-13.

The data in the Kafka queue is organized in a set of *topics* (see Table 9), 
each of which stores a sequence of records in a first-in first-out (FIFO) order 
for a pre-determined time window. 
These topics are distributed over a set of partitions, 
each of which is stored at a server in the Kafka cluster.

The topics are consumed by a set of data pipelines implemented with Spark, 
which process the data and write the results to Presto and Elasticsearch for persistent storage and search, 
respectively. These storage systems are then consumed by various downstream applications, 
e.g., dashboards applications and machine learning applications. 
The processed data is also input to reinforcement learning agents, 
which use it to decide on control actions.

<p align="center">
<img src="./../../img/monitoring.png" width="70%">
<p class="captionFig">
Figure 13: The monitoring system of CSLE; monitoring agents running on emulated devices push metric 
data to a distributed Kafka queue; the data in this queue is consumed by data pipelines that 
process the data and write to Presto and Elasticsearch for persistent storage and search, respectively; 
the processed data is used by Reinforcement Learning (RL) agents to decide on control actions, 
and by downstream applications to create dashboards and statistical models.
</p>
</p>

| *Topic*                                  | *Description*                                                               |
|------------------------------------------|-----------------------------------------------------------------------------|
| `client_population`                      | Statistics of the client population (e.g., number of clients per time.step). |
| `snort_ids_log`                          | Information about Snort IDS alerts per time-step.                           |
| `ossec_ids_log`                          | Information about OSSEC IDS alerts per time-step.                           |
| `host_metrics`                           | Information about system metrics per host.                                  |
| `docker_stats`                           | Resource statistics of docker containers.                                   |
| `docker_host_stats`                      | Resource statistics of host servers.                                        |
| `openflow_flow_stats`                    | Statistics of flows.                                                        |
| `openflow_port_stats`                    | Statistics of ports.                                                        |
| `openflow_flow_agg_stats`                | Aggregate flow statistics.                                                  |
| `avg_openflow_flow_stats_per_switch`     | Aggregate flow statstics per switch.                                        |
| `avg_openflow_port_stats_per_switch`     | Aggregate port statistics per switch.                                       |
| `attacker_actions`                       | Attacker actions in the emulation.                                          |
| `defender_actions`                       | Defender actions in the emulation.                                          |

<p class="captionFig">
Table 9: Kafka topics.
</p>

| *Metric*                            | *Description*                                      |
|-------------------------------------|----------------------------------------------------|
| `num_clients`                       | Number of active clients.                          |
| `clients_arrival_rate`              | Arrival rate of clients.                           |
| `pids`                              | Number of pids per container.                      |
| `cpu_percent`                       | CPU utilization per container.                     |
| `mem_current`                       | The total memory usage per container.              |
| `mem_total`                         | The memory limit per container.                    |
| `mem_percent`                       | The memory utilization per container.              |
| `blk_read`                          | Number of blocks read per container.               |
| `blk_write`                         | Number of blocks written per container.            |
| `net_rx`                            | Number of received network bytes per container.    |
| `net_tx`                            | Number of transmitted network bytes per container. |
| `avg_pids`                          | Average number of pids.                            |
| `avg_cpu_percent`                   | Average CPU utilization.                           |
| `avg_mem_current`                   | Average total memory usage.                        |
| `avg_mem_total`                     | Average memory limit.                              |
| `avg_mem_percent`                   | Average memory utilization.                        |
| `avg_blk_read`                      | Average number of blocks read.                     |
| `avg_blk_write`                     | Average number of blocks written.                  |
| `avg_net_rx`                        | Average number of received network bytes.          |
| `avg_net_tx`                        | Average number of transmitted network bytes.       |
| `num_logged_in_users`               | Number of logged in users per container.           |
| `num_failed_login_attempts`         | Number of failed logins per container.             |
| `num_open_connections`              | Number of open connections per container.          |
| `num_login_events`                  | Number of login events per container.              |
| `num_processes`                     | Number of processes per container.                 |
| `num_users`                         | Number of users per container.                     |
| `avg_num_logged_in_users`           | Average number of logged in users per container.   |
| `avg_num_failed_login_attempts`     | Average number of failed logins per container.     |
| `avg_num_open_connections`          | Average number of open connections per container.  |
| `avg_num_login_events`              | Average number of login events per container.      |
| `avg_num_processes`                 | Average number of processes per container.         |
| `avg_num_users`                     | Average number of users per container.             |

<p class="captionFig">
Table 10: Metrics collected per time-step by the monitoring system (1/4).
</p>

| *Metric*                                | *Description*                                                        |
|-----------------------------------------|----------------------------------------------------------------------|
| `defender_action_id`                    | Defender action ID.                                                  |
| `defender_action_name`                  | Defender action name.                                                |
| `defender_action_cmds`                  | List of defender action commands.                                    |
| `defender_action_type`                  | Defender action type.                                                |
| `defender_action_descr`                 | Defender action description.                                         |
| `defender_action_outcome`               | Defender action outcome.                                             |
| `defender_action_execution_time`        | Defender action execution time.                                      |
| `attacker_action_id`                    | Attacker action ID.                                                  |
| `attacker_action_name`                  | Attacker action name.                                                |
| `attacker_action_cmds`                  | List of attacker action commands.                                    |
| `attacker_action_type`                  | Attacker action type.                                                |
| `attacker_action_descr`                 | Attacker action description.                                         |
| `attacker_action_outcome`               | Attacker action outcome.                                             |
| `attacker_action_execution_time`        | Attacker action execution time.                                      |
| `attacker_action_vulnerability`         | Attacker action vulnerability.                                       |
| `snort_priority_alerts`                 | List of number of Snort alerts of priorities 1-4.                    |
| `snort_class_alerts`                    | List of number of Snort alerts of classes 1-34.                      |
| `snort_total_alerts`                    | Total number of Snort alerts.                                        |
| `snort_alerts_weighted_by_priority`     | Number of Snort alerts weighted by priority.                         |
| `ossec_level_alerts`                    | Number of OSSEC IDS alerts of level 1-16 per container.              |
| `ossec_group_alerts`                    | Number of OSSEC IDS alerts of group 1-12 per container.              |
| `ossec_total_alerts`                    | Total number of OSSEC IDS alerts per container.                      |
| `ossec_alerts_weighted_by_priority`     | Total number of OSSEC IDS alerts weighted by priority per container. |
| `avg_ossec_level_alerts`                | Average number of OSSEC IDS alerts of level 1-16.                    |
| `avg_ossec_group_alerts`                | Average number of OSSEC IDS alerts of group 1-12.                    |
| `avg_ossec_total_alerts`                | Average number of OSSEC IDS alerts.                                  |
| `avg_ossec_alerts_weighted_by_priority` | Average number of OSSEC IDS alerts weighted by priority.             |

<p class="captionFig">
Table 11: Metrics collected per time-step by the monitoring system (2/4).
</p>

| *Metric*                                       | *Description*                                                |
|------------------------------------------------|--------------------------------------------------------------|
| `flow_num_packets`                             | Number of packets per flow.                                  |
| `flow_num_bytes`                               | Number of transceived bytes per flow.                        |
| `flow_duration`                                | Duration per flow.                                           |
| `flow_in_port`                                 | Input port per flow.                                         |
| `flow_out_port`                                | Output port per flow.                                        |
| `flow_dst_mac_address`                         | Destination MAC address per flow.                            |
| `flow_datapath_id`                             | Datapath id per flow.                                        |
| `avg_flow_num_bytes`                           | Average number of transceived bytes per flow.                |
| `avg_flow_duration`                            | Average duration per flow.                                   |
| `of_port_datapath_id`                          | OpenFlow switch port datapath id.                            |
| `of_port_num_received_packets`                 | Number of received packets per OpenFlow port.                |
| `of_port_num_received_bytes`                   | Number of received bytes per OpenFlow port.                  |
| `of_port_num_received_errors`                  | Number of received errors per OpenFlow port.                 |
| `of_port_num_transmitted_packets`              | Number of transmitted packets per OpenFlow port.             |
| `of_port_num_transmitted_bytes`                | Number of transmitted bytes per OpenFlow port.               |
| `of_port_num_transmitted_errors`               | Number of transmitted errors per OpenFlow port.              |
| `of_port_num_received_dropped`                 | Number of received dropped packets per OpenFlow port.        |
| `of_port_num_transmitted_dropped`              | Number of transmitted dropped packets per OpenFlow port.     |
| `of_port_num_received_frame_errors`            | Number of received frame errors per OpenFlow port.           |
| `of_port_num_received_overrun_errors`          | Number of received overrun errors per OpenFlow port.         |
| `of_port_num_received_crc_errors`              | Number of received CRC errors per OpenFlow port.             |
| `of_port_num_collisions`                       | Number of received collisions per OpenFlow port.             |
| `of_port_duration_seconds`                     | Duration uptime per OpenFlow port.                           |
| `avg_of_port_num_received_packets`             | Average OpenFlow port number of received packets.            |
| `avg_of_port_num_received_bytes`               | Average OpenFlow port number of received bytes.              |
| `avg_of_port_num_received_errors`              | Average OpenFlow port number of received errors.             |
| `avg_of_port_num_transmitted_packets`          | Average OpenFlow port number of transmitted packets.         |
| `avg_of_port_num_transmitted_bytes`            | Average OpenFlow port number of transmitted bytes.           |
| `avg_of_port_num_transmitted_errors`           | Average OpenFlow port number of transmitted errors.          |
| `avg_of_port_num_received_dropped`             | Average OpenFlow port number of received dropped packets.    |
| `avg_of_port_num_transmitted_dropped`          | Average OpenFlow port number of transmitted dropped packets. |
| `avg_of_port_num_received_frame_errors`        | Average OpenFlow port number of received frame errors.       |
| `avg_of_port_num_received_overrun_errors`      | Average OpenFlow port number of received overrun errors.     |
| `avg_of_port_num_received_crc_errors`          | Average OpenFlow port number of received CRC errors.         |
| `avg_of_port_num_collisions`                   | Average OpenFlow port number of received collisions.         |
| `avg_of_port_duration_seconds`                 | Average OpenFlow port duration uptime.                       |

<p class="captionFig">
Table 12: Metrics collected per time-step by the monitoring system (3/4).
</p>

| *Metric*                                         | *Description*                                                       |
|--------------------------------------------------|---------------------------------------------------------------------|
| `switch_flow_num_packets`                        | Number of packets per flow per switch.                              |
| `switch_flow_num_bytes`                          | Number of transceived bytes per flow per switch.                    |
| `switch_flow_duration`                           | Duration per flow per switch.                                       |
| `switch_flow_in_port`                            | Input port per flow per switch.                                     |
| `switch_flow_out_port`                           | Output port per flow per switch.                                    |
| `switch_flow_dst_mac_address`                    | Destination MAC address per flow per switch.                        |
| `switch_flow_datapath_id`                        | Datapath id per flow per switch.                                    |
| `switch_avg_flow_num_bytes`                      | Average number of transceived bytes per flow per switch.            |
| `switch_avg_flow_duration`                       | Average duration per flow per switch.                               |
| `switch_of_port_datapath_id`                     | OpenFlow switch port datapath id.                                   |
| `switch_of_port_num_received_packets`            | Number of received packets per OpenFlow port per switch.            |
| `switch_of_port_num_received_bytes`              | Number of received bytes per OpenFlow port per switch.              |
| `switch_of_port_num_received_errors`             | Number of received errors per OpenFlow port per switch.             |
| `switch_of_port_num_transmitted_packets`         | Number of transmitted packets per OpenFlow port per switch.         |
| `switch_of_port_num_transmitted_bytes`           | Number of transmitted bytes per OpenFlow port per switch.           |
| `switch_of_port_num_transmitted_errors`          | Number of transmitted errors per OpenFlow port per switch.          |
| `switch_of_port_num_received_dropped`            | Number of received dropped packets per OpenFlow port per switch.    |
| `switch_of_port_num_transmitted_dropped`         | Number of transmitted dropped packets per OpenFlow port per switch. |
| `switch_of_port_num_received_frame_errors`       | Number of received frame errors per OpenFlow port per switch.       |
| `switch_of_port_num_received_overrun_errors`     | Number of received overrun errors per OpenFlow port per switch.     |
| `switch_of_port_num_received_crc_errors`         | Number of received CRC errors per OpenFlow port per switch.         |
| `switch_of_port_num_collisions`                  | Number of received collisions per OpenFlow port per switch.         |
| `switch_of_port_duration_seconds`                | Duration uptime per OpenFlow port per switch.                       |
| `switch_avg_of_port_num_received_packets`        | Average OpenFlow port number of received packets.                   |
| `switch_avg_of_port_num_received_bytes`          | Average OpenFlow port number of received bytes.                     |
| `switch_avg_of_port_num_received_errors`         | Average OpenFlow port number of received errors.                    |
| `switch_avg_of_port_num_transmitted_packets`     | Average OpenFlow port number of transmitted packets.                |
| `switch_avg_of_port_num_transmitted_bytes`       | Average OpenFlow port number of transmitted bytes.                  |
| `switch_avg_of_port_num_transmitted_errors`      | Average OpenFlow port number of transmitted errors.                 |
| `switch_avg_of_port_num_received_dropped`        | Average OpenFlow port number of received dropped packets.           |
| `switch_avg_of_port_num_transmitted_dropped`     | Average OpenFlow port number of transmitted dropped packets.        |
| `switch_avg_of_port_num_received_frame_errors`   | Average OpenFlow port number of received frame errors.              |
| `switch_avg_of_port_num_received_overrun_errors` | Average OpenFlow port number of received overrun errors.            |
| `switch_avg_of_port_num_received_crc_errors`     | Average OpenFlow port number of received CRC errors.                |
| `switch_avg_of_port_num_collisions`              | Average OpenFlow port number of received collisions.                |
| `switch_avg_of_port_duration_seconds`            | Average OpenFlow port duration uptime.                              |

<p class="captionFig">
Table 13: Metrics collected per time-step by the monitoring system (4/4).
</p>

### Management Agents

In addition to the monitoring agent, each emulated device runs a *management agent*, 
which is connected to the management network and exposes a gRPC API 
for management actions (see Fig. 14). 
This API is invoked by the management system to perform management operations on behalf of 
CSLE users and reinforcement learning agents, e.g., restarting services, rotating log files, 
or updating firewall configurations. 
The management functions available in the API are listed in 
Tables 14-16.

<p align="center">
<img src="./../../img/management_actions.png" width="45%">
<p class="captionFig">
Figure 14: The management setup in CSLE; each emulated device runs a management 
agent which is connected to the management network and exposes a gRPC API for management actions, 
which is invoked by the management system on behalf of CSLE users and reinforcement learning agents.
</p>
</p>

| *Remote procedure call*         | *Description*                                              |
|---------------------------------|------------------------------------------------------------|
| `getClients()`                  | Gets the number of clients.                                |
| `stopClients()`                 | Stops the client population.                               |
| `startClients()`                | Starts the client population.                              |
| `startProducer()`               | Starts the Kafka producer thread of the client population. |
| `stopProducer()`                | Stops the Kafka producer thread of the client population.  |
| `getDockerStatsMonitorStatus()` | Gets the status of the Docker statsmanager.                |
| `stopDockerStatsMonitor()`      | Stops the Docker statsmanager.                             |
| `startDockerStatsMonitor()`     | Starts the Docker statsmanager.                            |
| `getElkStatus()`                | Gets the status of the ELK stack.                          |
| `stopElk()`                     | Stops the ELK stack.                                       |
| `startElk()`                    | Starts the ELK stack.                                      |
| `stopElastic()`                 | Stops Elasticsearch.                                       |
| `startElastic()`                | Starts Elasticsearch.                                      |
| `stopLogstash()`                | Stops Logstash.                                            |
| `startLogstash()`               | Starts Logstash.                                           |
| `stopKibana()`                  | Stops Kibana.                                              |
| `startKibana()`                 | Starts Kibana.                                             |
| `stopHostMonitor()`             | Stops the host monitor of a particular host.               |
| `startHostMonitor()`            | Starts the host monitor of a particular host.              |
| `getHostStatus()`               | Gets the status of a host.                                 |
| `getHostMetric()`               | Gets a list of metrics of a given host.                    |
| `stopFilebeat()`                | Stops filebeat on a given host.                            |
| `startFilebeat()`               | Starts filebeat on a given host.                           |
| `configFilebeat()`              | Configures filebeat on a given host.                       |
| `stopPacketbeat()`              | Stops packetbeat on a given host.                          |
| `updateFirewall()`              | Updates the firewall configuration on a given host.        |
| `createUserAccount()`           | Creates a user account on a given host.                    |
| `revokeUserCertificates()`      | Revokes user certificates on a given host.                 |

<p class="captionFig">
Table 14: Remote procedure calls (RPCs) in the gRPC API exposed by management agents (1/3).
</p>

| *Remote procedure call*   | *Description*                                      |
|---------------------------|----------------------------------------------------|
| `startPacketbeat()`       | Starts packetbeat on a given host.                 |
| `configPacketbeat()`      | Configures packetbeat on a given host.             |
| `stopMetricbeat()`        | Stops metricbeat on a given host.                  |
| `startMetricbeat()`       | Starts metricbeat on a given host.                 |
| `configMetricbeat()`      | Configures metricbeat on a given host.             |
| `stopHeartbeat()`         | Stops heartbeat on a given host.                   |
| `startHeartbeat()`        | Starts heartbeat on a given host.                  |
| `configHeartbeat()`       | Configures heartbeat on a given host.              |
| `getKafkaStatus()`        | Gets the status of the Kafka cluster.              |
| `stopKafka()`             | Stops the Kafka cluster.                           |
| `startKafka()`            | Starts the Kafka cluster.                          |
| `createTopic()`           | Creates a topic in Kafka.                          |
| `deleteTopic()`           | Deletes a topic in Kafka.                          |
| `getOSSECIdsAlerts()`     | Gets the list of OSSEC IDS alerts of a given host. |
| `stopOSSECIdsMonitor()`   | Stops the OSSEC IDS monitor of a given host.       |
| `startOSSECIdsMonito()`   | Starts the OSSEC IDS monitor of a given host.      |
| `stopOSSECIds()`          | Stops the OSSEC IDS on a given host.               |
| `startOSSECIds()`         | Starts the OSSEC IDS on a given host.              |

<p class="captionFig">
Table 15: Remote procedure calls (RPCs) in the gRPC API exposed by management agents (2/3).
</p>

| *Remote procedure call*        | *Description*                                             |
|--------------------------------|-----------------------------------------------------------|
| `getOSSECIdsMonitorStatus()`   | Gets the status of the OSSEC IDS monitor of a given host. |
| `getRyuStatus()`               | Gets the status of the Ryu SDN manager.                   |
| `stopRyu()`                    | Stops the Ryu SDN manager.                                |
| `startRyu()`                   | Starts the Ryu SDN manager.                               |
| `stopRyuMonitor()`             | Stops the Ryu monitor.                                    |
| `startRyuMonitor()`            | Starts the Ryu monitor.                                   |
| `getSnortIdsAlerts()`          | Gets the list of Snort IDS alerts.                        |
| `stopSnortIdsMonitor()`        | Stops the Snort IDS monitor.                              |
| `startSnortIdsMonitor()`       | Starts the Snort IDS monitor.                             |
| `getSnortIdsMonitorStatus()`   | Gets the status of the Snort IDS monitor.                 |
| `stopSnortIds()`               | Stops the Snort IDS.                                      |
| `startSnortIds()`              | Starts the Snort IDS.                                     |
| `getTrafficStatus()`           | Gets the status of the traffic generator of a given host. |
| `stopTraffic()`                | Stops the traffic generator on a given host.              |
| `startTraffic()`               | Starts the traffic generator on a given host.             |
| `updateSnortConfig()`          | Updates the Snort configuration on a given host.          |
| `updateOssecConfig()`          | Updates the OSSEC IDS configuration on a given host.      |
| `updateRyuConfig()`            | Updates the Ryu configuration on a given host.            |

<p class="captionFig">
Table 16: Remote procedure calls (RPCs) in the gRPC API exposed by management agents (3/3).
</p>

### Starting an Emulation Execution

An emulation execution corresponds to a set of running Docker containers and virtual networks. 
Starting an execution takes around 10-15 minutes. 
To start an execution, the emulation system first reads the emulation configuration 
from the metastore and starts the containers that are described in the configuration. 
Once the containers have started, the emulation system applies the emulation configuration. 
This step involves executing a sequence of Remote Procedure Calls (RPCs) 
through the gRPC API described above, 
e.g., RPCs to create user accounts, to start services, and to configure services 
(see Fig. 15).

<p align="center">
<img src="./../../img/sequence_diagram.png" width="80%">
<p class="captionFig">
Figure 15: Sequence diagram of the emulation system's procedure to start an emulation execution.
</p>
</p>
