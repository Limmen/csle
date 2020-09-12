#!/bin/bash

if [[ $EUID -eq 0 ]]; then
    route add -net $1 netmask $2 gw $3 || echo "route already added"
    exit 0
else
    echo "cannot setup routing table without sudo"
fi
