#!/bin/bash

route add 172.18.2.54 gw 172.18.2.2 # route ssh2 to default gw ssh1
route add 172.18.2.7 gw 172.18.2.74 # route ftp2 to default gw ssh3
route add 172.18.2.62 gw 172.18.2.74 # route telnet3 to default gw ssh3
route add 172.18.2.101 gw 172.18.2.74 # route honeypot2 to default gw ssh3

iptables -A OUTPUT -d 172.18.2.10 -j ACCEPT # router
iptables -A OUTPUT -d 172.18.2.1 -j ACCEPT # docker gw
iptables -A OUTPUT -d 172.18.2.2 -j ACCEPT # ssh1
iptables -A OUTPUT -d 172.18.2.3 -j ACCEPT #telnet1
iptables -A OUTPUT -d 172.18.2.21 -j ACCEPT # honeypot1
iptables -A OUTPUT -d 172.18.2.79 -j ACCEPT # ftp1
iptables -A OUTPUT -d 172.18.2.74 -j ACCEPT # ssh 3
iptables -A OUTPUT -d 172.18.2.61 -j ACCEPT # telnet 2
iptables -A OUTPUT -d 172.18.2.191 -j ACCEPT #kali
iptables -A OUTPUT -d 172.18.2.0/24 -j DROP # default

iptables -A FORWARD -d 172.18.2.7 -j DROP # ftp2
iptables -A FORWARD -d 172.18.2.62 -j DROP # telnet3
iptables -A FORWARD -d 172.18.2.74 -j DROP # ssh3
iptables -A FORWARD -d 172.18.2.101 -j DROP # honeypot2
iptables -A FORWARD -d 172.18.2.61 -j DROP # telnet2
iptables -A FORWARD -s 172.18.2.61 -d 172.18.2.74 -j ACCEPT # telnet2 to ssh3
iptables -A FORWARD -s 172.18.2.74 -d 172.18.2.61 -j ACCEPT # ssh3 to telnet2
iptables -A FORWARD -d 172.18.2.0/24 -j ACCEPT # default

iptables -A INPUT -s 172.18.2.0/24 -j ACCEPT # default
