#!/bin/bash

# Agent

ssh -t agent@172.18.3.191 << EOF
   zip agent_cache.zip ~/*
EOF
scp agent@172.18.3.191:/home/agent/agent_cache.zip .

# ssh_1
ssh -t csle_admin@172.18.3.2 << EOF
   zip -r ssh_1_cache.zip /home/ '*.xml' '*.txt'
EOF
scp csle_admin@172.18.3.2:/home/csle_admin/ssh_1_cache.zip .

# ssh_2
ssh -t csle_admin@172.18.3.54 << EOF
   zip -r ssh_2_cache.zip /home/ '*.xml' '*.txt'
EOF
scp csle_admin@172.18.3.54:/home/csle_admin/ssh_2_cache.zip .

# ssh_3
ssh -t csle_admin@172.18.3.74 << EOF
   zip -r ssh_3_cache.zip /home/ '*.xml' '*.txt'
EOF
scp csle_admin@172.18.3.74:/home/csle_admin/ssh_3_cache.zip .

# telnet_1
ssh -t csle_admin@172.18.3.3 << EOF
   zip -r telnet_1_cache.zip /home/ '*.xml' '*.txt'
EOF
scp csle_admin@172.18.3.3:/home/csle_admin/telnet_1_cache.zip .

# telnet_2
ssh -t csle_admin@172.18.3.61 << EOF
   zip -r telnet_2_cache.zip /home/ '*.xml' '*.txt'
EOF
scp csle_admin@172.18.3.61:/home/csle_admin/telnet_2_cache.zip .

# telnet_3
ssh -t csle_admin@172.18.3.62 << EOF
   zip -r telnet_3_cache.zip /home/ '*.xml' '*.txt'
EOF
scp csle_admin@172.18.3.62:/home/csle_admin/telnet_3_cache.zip .



#agent,  csle@admin-pw_191
