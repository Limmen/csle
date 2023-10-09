#!/bin/bash

cd csle-base; pip install -e .
cd csle-collector; pip install -e .
cd csle-ryu; pip install -e .
cd csle-common; pip install -e .
cd csle-cluster; pip install -e .
cd csle-attacker; pip install -e .
cd csle-defender; pip install -e .
cd csle-gym-csle-intrusion-response-game; pip install -e .
cd csle-system-identification; pip install -e .
cd csle-gym-csle-stopping-game; pip install -e .
cd csle-tolerance; pip install -e .
cd csle-agents; pip install -e .
cd csle-rest-api; pip install -e .
cd csle-cli; pip install -e .