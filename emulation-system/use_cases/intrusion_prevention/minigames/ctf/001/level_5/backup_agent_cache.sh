#!/bin/bash

# Agent

ssh -t agent@172.18.2.191 << EOF
   zip agent_cache.zip ~/*
EOF
scp agent@172.18.2.191:/home/agent/agent_cache.zip .

# SSH1
ssh -t csle_admin@172.18.2.2 << EOF
   zip -r ssh1_cache.zip /home/ '*.xml' '*.txt'
EOF
scp csle_admin@172.18.2.2:/home/csle_admin/ssh1_cache.zip .

# SSH2
ssh -t csle_admin@172.18.2.54 << EOF
   zip -r ssh2_cache.zip /home/ '*.xml' '*.txt'
EOF
scp csle_admin@172.18.2.54:/home/csle_admin/ssh2_cache.zip .

# SSH3
ssh -t csle_admin@172.18.2.74 << EOF
   zip -r ssh3_cache.zip /home/ '*.xml' '*.txt'
EOF
scp csle_admin@172.18.2.74:/home/csle_admin/ssh3_cache.zip .

# Telnet1
ssh -t csle_admin@172.18.2.3 << EOF
   zip -r telnet1_cache.zip /home/ '*.xml' '*.txt'
EOF
scp csle_admin@172.18.2.3:/home/csle_admin/telnet1_cache.zip .

# Telnet2
ssh -t csle_admin@172.18.2.61 << EOF
   zip -r telnet2_cache.zip /home/ '*.xml' '*.txt'
EOF
scp csle_admin@172.18.2.61:/home/csle_admin/telnet2_cache.zip .

# Telnet3
ssh -t csle_admin@172.18.2.62 << EOF
   zip -r telnet3_cache.zip /home/ '*.xml' '*.txt'
EOF
scp csle_admin@172.18.2.62:/home/csle_admin/telnet3_cache.zip .



#agent,  csle@admin-pw_191
