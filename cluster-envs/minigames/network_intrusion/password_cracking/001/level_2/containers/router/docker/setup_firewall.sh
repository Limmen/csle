#!/bin/bash

iptables -A FORWARD -d 172.18.2.1 -j ACCEPT
iptables -A FORWARD -d 172.18.2.2 -j ACCEPT
iptables -A FORWARD -d 172.18.2.3 -j ACCEPT
iptables -A FORWARD -d 172.18.2.21 -j ACCEPT
iptables -A FORWARD -d 172.18.2.79 -j ACCEPT

iptables -A OUTPUT -d 172.18.2.191 -j ACCEPT #kali
iptables -A FORWARD -d 172.18.2.191 -j ACCEPT #kali

iptables --policy INPUT DROP
iptables --policy OUTPUT DROP
iptables --policy FORWARD DROP
