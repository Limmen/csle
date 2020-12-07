#!/bin/bash

# Agent

ssh -t agent@172.18.3.191 << EOF
   zip agent_cache.zip ~/*
EOF
scp agent@172.18.3.191:/home/agent/agent_cache.zip .

# SSH1
ssh -t pycr_admin@172.18.3.2 << EOF
   zip -r ssh1_cache.zip /home/ '*.xml' '*.txt'
EOF
scp pycr_admin@172.18.3.2:/home/pycr_admin/ssh1_cache.zip .

# SSH2
ssh -t pycr_admin@172.18.3.54 << EOF
   zip -r ssh2_cache.zip /home/ '*.xml' '*.txt'
EOF
scp pycr_admin@172.18.3.54:/home/pycr_admin/ssh2_cache.zip .

# SSH3
ssh -t pycr_admin@172.18.3.74 << EOF
   zip -r ssh3_cache.zip /home/ '*.xml' '*.txt'
EOF
scp pycr_admin@172.18.3.74:/home/pycr_admin/ssh3_cache.zip .

# Telnet1
ssh -t pycr_admin@172.18.3.3 << EOF
   zip -r telnet1_cache.zip /home/ '*.xml' '*.txt'
EOF
scp pycr_admin@172.18.3.3:/home/pycr_admin/telnet1_cache.zip .

# Telnet2
ssh -t pycr_admin@172.18.3.61 << EOF
   zip -r telnet2_cache.zip /home/ '*.xml' '*.txt'
EOF
scp pycr_admin@172.18.3.61:/home/pycr_admin/telnet2_cache.zip .

# Telnet3
ssh -t pycr_admin@172.18.3.62 << EOF
   zip -r telnet3_cache.zip /home/ '*.xml' '*.txt'
EOF
scp pycr_admin@172.18.3.62:/home/pycr_admin/telnet3_cache.zip .



#agent,  pycr@admin-pw_191
