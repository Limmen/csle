#!/bin/bash

echo "Running type checker for csle-agents"
cd simulation-system/libs/csle-agents; mypy src tests; cd ../../../
echo "Running type checker for csle-attacker"
cd simulation-system/libs/csle-attacker; mypy src tests; cd ../../../
echo "Running type checker for csle-collector"
cd simulation-system/libs/csle-collector; mypy src tests; cd ../../../
echo "Running type checker for csle-common"
cd simulation-system/libs/csle-common; mypy src tests; cd ../../../
echo "Running type checker for csle-defender"
cd simulation-system/libs/csle-defender; mypy src tests; cd ../../../
echo "Running type checker for csle-rest-api"
cd simulation-system/libs/csle-rest-api; mypy src tests; cd ../../../
echo "Running type checker for csle-ryu"
cd simulation-system/libs/csle-ryu; mypy src tests; cd ../../../
echo "Running type checker for csle-system-identification"
cd simulation-system/libs/csle-system-identification; mypy src tests; cd ../../../
echo "Running type checker for gym-csle-stopping-game"
cd simulation-system/libs/gym-csle-stopping-game; mypy src tests; cd ../../../
echo "Running type checker for gym-csle-intrusion-response-game"
cd simulation-system/libs/gym-csle-intrusion-response-game; mypy src tests; cd ../../../
echo "Running type checker for csle-base"
cd simulation-system/libs/csle-base; mypy src tests; cd ../../../
echo "Running type checker for csle-cli"
cd simulation-system/libs/csle-cli; mypy src tests; cd ../../../
