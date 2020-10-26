#!/bin/bash
route add -net 172.18.2.0 netmask 255.255.255.0 gw 172.18.2.10

iptables -A OUTPUT -d 172.18.2.10 -j ACCEPT
iptables -A OUTPUT -d 172.18.2.1 -j ACCEPT
iptables -A OUTPUT -d 172.18.2.2 -j ACCEPT
iptables -A OUTPUT -d 172.18.2.3 -j ACCEPT
iptables -A OUTPUT -d 172.18.2.21 -j ACCEPT
iptables -A OUTPUT -d 172.18.2.79 -j ACCEPT
iptables -A OUTPUT -d 172.18.2.0/24 -j DROP