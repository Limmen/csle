#!/bin/bash

route add 172.18.2.7 gw 172.18.2.3 # ftp2 default gw telnet1
route add 172.18.2.101 gw 172.18.2.3 # honeypot2 default gw telnet1
route add 172.18.2.62 gw 172.18.2.3 # telnet3 default gw telnet1
route add 172.18.2.61 gw 172.18.2.3 # telnet2 default gw telnet1
route add 172.18.2.74 gw 172.18.2.3 # ssh3 default gw telnet1

route add 172.18.2.54 gw 172.18.2.2 # ssh2 default gw ssh1

iptables -A OUTPUT -d 172.18.2.10 -j ACCEPT # router
iptables -A OUTPUT -d 172.18.2.1 -j ACCEPT # docker gw
iptables -A OUTPUT -d 172.18.2.2 -j ACCEPT # ssh1
iptables -A OUTPUT -d 172.18.2.3 -j ACCEPT # telnet1
iptables -A OUTPUT -d 172.18.2.21 -j ACCEPT # honeypot1
iptables -A OUTPUT -d 172.18.2.79 -j ACCEPT # ftp1
iptables -A OUTPUT -d 172.18.2.191 -j ACCEPT #kali
iptables -A OUTPUT -d 172.18.2.0/24 -j DROP # default

iptables -A FORWARD -d 172.18.2.0/24 -j DROP # default

iptables -A INPUT -s 172.18.2.0/24 -j ACCEPT # default