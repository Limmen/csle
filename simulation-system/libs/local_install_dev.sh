#!/bin/bash

cd csle-base; pip install -r requirements_dev.txt; cd ..
cd csle-collector; pip install -r requirements_dev.txt; cd ..
cd csle-ryu; pip install -r requirements_dev.txt; cd ..
cd csle-common; pip install -r requirements_dev.txt; cd ..
cd csle-cluster; pip install -r requirements_dev.txt; cd ..
cd csle-attacker; pip install -r requirements_dev.txt; cd ..
cd csle-defender; pip install -r requirements_dev.txt; cd ..
cd gym-csle-intrusion-response-game; pip install -r requirements_dev.txt; cd ..
cd csle-system-identification; pip install -r requirements_dev.txt; cd ..
cd gym-csle-stopping-game; pip install -r requirements_dev.txt; cd ..
cd gym-csle-apt-game; pip install -r requirements_dev.txt; cd ..
cd gym-csle-cyborg; pip install -r requirements_dev.txt; cd ..
cd csle-tolerance; pip install -r requirements_dev.txt; cd ..
cd csle-agents; pip install -r requirements_dev.txt; cd ..
cd csle-rest-api; pip install -r requirements_dev.txt; cd ..
cd csle-cli; pip install -r requirements_dev.txt; cd ..
