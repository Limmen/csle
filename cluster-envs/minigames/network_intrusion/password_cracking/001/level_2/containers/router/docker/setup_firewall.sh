#!/bin/bash

iptables -A FORWARD -d 172.18.2.1 -j ACCEPT # docker gw
iptables -A FORWARD -d 172.18.2.2 -j ACCEPT # ssh1
iptables -A FORWARD -d 172.18.2.3 -j ACCEPT # telnet1
iptables -A FORWARD -d 172.18.2.21 -j ACCEPT # honeypot1
iptables -A FORWARD -d 172.18.2.79 -j ACCEPT # ftp1

iptables -A OUTPUT -d 172.18.2.191 -j ACCEPT #kali
iptables -A FORWARD -d 172.18.2.191 -j ACCEPT #kali

iptables --policy INPUT DROP # default
iptables --policy OUTPUT DROP # default
iptables --policy FORWARD DROP # default
