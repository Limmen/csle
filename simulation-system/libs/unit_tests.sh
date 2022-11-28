#!/bin/bash

echo "Running unit tests for csle-agents"
cd csle-agents; pytest; cd ../
echo "Running unit tests for csle-attacker"
cd csle-attacker; pytest; cd ../
echo "Running unit tests for csle-collector"
cd csle-collector; pytest; cd ../
echo "Running unit tests for csle-common"
cd csle-common; pytest; cd ../
echo "Running unit tests for csle-defender"
cd csle-defender; pytest; cd ../
echo "Running unit tests for csle-rest-api"
cd csle-rest-api; pytest; cd ../
echo "Running unit tests for csle-ryu"
cd csle-ryu; pytest; cd ../
echo "Running unit tests for csle-system-identification"
cd csle-system-identification; pytest; cd ../
echo "Running unit tests for gym-csle-stopping-game"
cd gym-csle-stopping-game; pytest; cd ../
