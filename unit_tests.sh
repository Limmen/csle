#!/bin/bash

echo "Running Python unit tests for csle-agents"
cd simulation-system/libs/csle-agents; pytest; cd ../../../
echo "Running Python unit tests for csle-attacker"
cd simulation-system/libs/csle-attacker; pytest; cd ../../../
echo "Running Python unit tests for csle-collector"
cd simulation-system/libs/csle-collector; pytest; cd ../../../
echo "Running Python unit tests for csle-common"
cd simulation-system/libs/csle-common; pytest; cd ../../../
echo "Running Python unit tests for csle-defender"
cd simulation-system/libs/csle-defender; pytest; cd ../../../
echo "Running Python unit tests for csle-rest-api"
cd simulation-system/libs/csle-rest-api; pytest; cd ../../../
echo "Running Python unit tests for csle-ryu"
cd simulation-system/libs/csle-ryu; pytest; cd ../../../
echo "Running Python unit tests for csle-system-identification"
cd simulation-system/libs/csle-system-identification; pytest; cd ../../../
echo "Running Python unit tests for gym-csle-stopping-game"
cd simulation-system/libs/gym-csle-stopping-game; pytest; cd ../../../
echo "Running Python unit tests for csle-cluster"
cd simulation-system/libs/csle-cluster; pytest; cd ../../../
echo "Running Python unit tests for gym-csle-intrusion-response-game"
cd simulation-system/libs/gym-csle-intrusion-response-game; pytest; cd ../../../
echo "Running Python unit tests for csle-tolerance"
cd simulation-system/libs/csle-tolerance; pytest; cd ../../../
echo "Running Python unit tests for gym-csle-apt-game"
cd simulation-system/libs/gym-csle-apt-game; pytest; cd ../../../
echo "Running Python unit tests for gym-csle-cyborg"
cd simulation-system/libs/gym-csle-cyborg; pytest; cd ../../../
echo "Running Python unit tests for csle-attack-profiler"
cd simulation-system/libs/csle-attack-profiler; pytest; cd ../../../
echo "Running Python unit tests for CSLE emulation environments"
cd emulation-system/envs/050/level_1; pytest; cd ../../../../
cd emulation-system/envs/050/level_2; pytest; cd ../../../../
cd emulation-system/envs/050/level_3; pytest; cd ../../../../
cd emulation-system/envs/050/level_4; pytest; cd ../../../../
cd emulation-system/envs/050/level_5; pytest; cd ../../../../
cd emulation-system/envs/050/level_6; pytest; cd ../../../../
cd emulation-system/envs/050/level_7; pytest; cd ../../../../
cd emulation-system/envs/050/level_8; pytest; cd ../../../../
cd emulation-system/envs/050/level_9; pytest; cd ../../../../
cd emulation-system/envs/050/level_10; pytest; cd ../../../../
cd emulation-system/envs/050/level_11; pytest; cd ../../../../
cd emulation-system/envs/050/level_12; pytest; cd ../../../../
cd emulation-system/envs/050/level_13; pytest; cd ../../../../
cd emulation-system/envs/050/level_14; pytest; cd ../../../../
echo "Running Python unit tests for CSLE simulation environments"
cd simulation-system/envs/apt_game; pytest; cd ../../../
cd simulation-system/envs/apt_mdp_attacker; pytest; cd ../../../
cd simulation-system/envs/apt_pomdp_defender; pytest; cd ../../../
cd simulation-system/envs/cyborg; pytest; cd ../../../
cd simulation-system/envs/intrusion_recovery_pomdp_defender; pytest; cd ../../../
cd simulation-system/envs/intrusion_response_cmdp_defender; pytest; cd ../../../
cd simulation-system/envs/local_intrusion_response_pomdp_attacker; pytest; cd ../../../
cd simulation-system/envs/local_intrusion_response_pomdp_defender; pytest; cd ../../../
cd simulation-system/envs/stopping_game; pytest; cd ../../../
cd simulation-system/envs/stopping_mdp_attacker; pytest; cd ../../../
cd simulation-system/envs/stopping_pomdp_defender; pytest; cd ../../../
cd simulation-system/envs/workflow_intrusion_response_pomdp_attacker; pytest; cd ../../../
cd simulation-system/envs/workflow_intrusion_response_pomdp_defender; pytest; cd ../../../
echo "Running JavaScript unit tests for csle-mgmt-webapp"
cd management-system/csle-mgmt-webapp; npm test -- --watchAll=false; cd ../../
