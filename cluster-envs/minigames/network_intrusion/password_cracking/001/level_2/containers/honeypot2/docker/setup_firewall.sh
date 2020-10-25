#!/bin/bash
iptables -A OUTPUT -d 172.18.2.10 -j ACCEPT
iptables -A OUTPUT -d 172.18.2.1 -j ACCEPT
iptables -A OUTPUT -d 172.18.2.2 -j ACCEPT
iptables -A OUTPUT -d 172.18.2.3 -j ACCEPT
iptables -A OUTPUT -d 172.18.2.21 -j ACCEPT
iptables -A OUTPUT -d 172.18.2.79 -j ACCEPT
iptables -A OUTPUT -d 172.18.2.54 -j ACCEPT # ssh2
iptables -A OUTPUT -d 172.18.2.61 -j ACCEPT # telnet 2
iptables -A OUTPUT -d 172.18.2.62 -j ACCEPT # telnet 3
iptables -A OUTPUT -d 172.18.2.191 -j ACCEPT #kali
iptables -A OUTPUT -d 172.18.2.0/24 -j DROP