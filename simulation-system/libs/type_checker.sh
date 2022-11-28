#!/bin/bash

echo "Running type checker for csle-agents"
cd csle-agents; mypy .; cd ../
echo "Running type checker for csle-attacker"
cd csle-attacker; mypy .; cd ../
echo "Running type checker for csle-collector"
cd csle-collector; mypy .; cd ../
echo "Running type checker for csle-common"
cd csle-common; mypy .; cd ../
echo "Running type checker for csle-defender"
cd csle-defender; mypy .; cd ../
echo "Running type checker for csle-rest-api"
cd csle-rest-api; mypy .; cd ../
echo "Running type checker for csle-ryu"
cd csle-ryu; mypy .; cd ../
echo "Running type checker for csle-system-identification"
cd csle-system-identification; mypy .; cd ../
echo "Running type checker for gym-csle-stopping-game"
cd gym-csle-stopping-game; mypy .; cd ../
