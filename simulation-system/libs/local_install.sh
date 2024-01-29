#!/bin/bash

cd csle-base; pip install -e .; cd ..
cd csle-collector; pip install -e .; cd ..
cd csle-ryu; pip install -e .; cd ..
cd csle-common; pip install -e .; cd ..
cd csle-cluster; pip install -e .; cd ..
cd csle-attacker; pip install -e .; cd ..
cd csle-defender; pip install -e .; cd ..
cd gym-csle-intrusion-response-game; pip install -e .; cd ..
cd csle-system-identification; pip install -e .; cd ..
cd gym-csle-stopping-game; pip install -e .; cd ..
cd gym-csle-apt-game; pip install -e .; cd ..
cd gym-csle-cyborg; pip install -e .; cd ..
cd csle-tolerance; pip install -e .; cd ..
cd csle-agents; pip install -e .; cd ..
cd csle-rest-api; pip install -e .; cd ..
cd csle-cli; pip install -e .; cd ..
