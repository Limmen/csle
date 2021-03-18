#!/bin/bash

ssh -t agent@172.18.1.191 << EOF
   zip agent_cache.zip ~/*
EOF

scp agent@172.18.1.191:/home/agent/agent_cache.zip .
