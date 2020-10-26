#!/bin/bash

route add -net 172.18.2.0 netmask 255.255.255.0 gw 172.18.2.2 # ssh1 default gw

iptables -A OUTPUT -d 172.18.2.10 -j ACCEPT # router
iptables -A OUTPUT -d 172.18.2.1 -j ACCEPT # docker gw
iptables -A OUTPUT -d 172.18.2.2 -j ACCEPT # ssh1
iptables -A OUTPUT -d 172.18.2.3 -j ACCEPT # telnet1
iptables -A OUTPUT -d 172.18.2.21 -j ACCEPT # honeypot1
iptables -A OUTPUT -d 172.18.2.79 -j ACCEPT # ftp1
iptables -A OUTPUT -d 172.18.2.54 -j ACCEPT # ssh2
iptables -A OUTPUT -d 172.18.2.191 -j ACCEPT # kali
iptables -A OUTPUT -d 172.18.2.0/24 -j DROP # default

iptables -A FORWARD -d 172.18.2.0/24 -j DROP # default

iptables -A INPUT -s 172.18.2.2 -j ACCEPT # ssh2
iptables -A INPUT -s 172.18.2.0/24 -j DROP # default


# flush iptables -F