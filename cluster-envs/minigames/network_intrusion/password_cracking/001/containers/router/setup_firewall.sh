#!/bin/bash

if [[ $EUID -eq 0 ]]; then
    route add -net $(SUBNET) netmask $(SUBNET_MASK_2) gw $(IP) || echo "route already added"
    exit 0
else
    echo "cannot setup routing table without sudo"
fi
