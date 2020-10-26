#!/bin/bash

route add 172.18.2.2 gw 172.18.2.74 # ssh3 gw for ssh1
route add 172.18.2.21 gw 172.18.2.74 # ssh3 gw for honeypot1
route add 172.18.2.54 gw 172.18.2.74 # ssh3 gw for ssh2
route add 172.18.2.79 gw 172.18.2.74 # ssh3 gw for ftp1
route add 172.18.2.10 gw 172.18.2.74 # ssh3 gw for router
route add 172.18.2.191 gw 172.18.2.74 # ssh3 gw for kali
route add 172.18.2.61 gw 172.18.2.74 # ssh3 gw for telnet2
route add 172.18.2.101 gw 172.18.2.74 # ssh3 gw for honeypot2

iptables -A OUTPUT -d 172.18.2.10 -j ACCEPT #router1
iptables -A OUTPUT -d 172.18.2.1 -j ACCEPT # docker gw
iptables -A OUTPUT -d 172.18.2.2 -j ACCEPT #ssh1
iptables -A OUTPUT -d 172.18.2.3 -j ACCEPT # telnet1
iptables -A OUTPUT -d 172.18.2.21 -j ACCEPT # honeypot1
iptables -A OUTPUT -d 172.18.2.79 -j ACCEPT # ftp1
iptables -A OUTPUT -d 172.18.2.74 -j ACCEPT # ssh3
iptables -A OUTPUT -d 172.18.2.61 -j ACCEPT # telnet 2
iptables -A OUTPUT -d 172.18.2.101 -j ACCEPT # honeypot 2
iptables -A OUTPUT -d 172.18.2.7 -j ACCEPT # ftp 2
iptables -A OUTPUT -d 172.18.2.191 -j ACCEPT #kali
iptables -A OUTPUT -d 172.18.2.0/24 -j DROP # default

iptables -A FORWARD -d 172.18.2.7 -j DROP # ftp2
iptables -A FORWARD -d 172.18.2.0/24 -j ACCEPT # default

iptables -A INPUT -s 172.18.2.74 -j ACCEPT # ssh3
iptables -A INPUT -s 172.18.2.7 -j ACCEPT # ftp2
iptables -A INPUT -s 172.18.2.101 -j ACCEPT # honeypot2
iptables -A INPUT -s 172.18.2.0/24 -j DROP # default