#!/bin/bash

echo "Generating csle-agents API documentation"
cd csle-agents/docs; sphinx-apidoc -f -o source/ ../src/csle_agents/; make html; cp -r build/html/* ../../../../docs/_docs/csle-agents; cd ../../
echo "Generating csle-attacker API documentation"
cd csle-attacker/docs; sphinx-apidoc -f -o source/ ../src/csle_attacker/; make html; cp -r build/html/* ../../../../docs/_docs/csle-attacker; cd ../../
echo "Generating csle-collector API documentation"
cd csle-collector/docs; sphinx-apidoc -f -o source/ ../src/csle_collector/; make html; cp -r build/html/* ../../../../docs/_docs/csle-collector; cd ../../
echo "Generating csle-common API documentation"
cd csle-common/docs; sphinx-apidoc -f -o source/ ../src/csle_common/; make html; cp -r build/html/* ../../../../docs/_docs/csle-common; cd ../../
echo "Generating csle-defender API documentation"
cd csle-defender/docs; sphinx-apidoc -f -o source/ ../src/csle_defender/; make html; cp -r build/html/* ../../../../docs/_docs/csle-defender; cd ../../
echo "Generating csle-rest-api API documentation"
cd csle-rest-api/docs; sphinx-apidoc -f -o source/ ../src/csle_rest_api/; make html; cp -r build/html/* ../../../../docs/_docs/csle-rest-api; cd ../../
echo "Generating csle-ryu API documentation"
cd csle-ryu/docs; sphinx-apidoc -f -o source/ ../src/csle_ryu/; make html; cp -r build/html/* ../../../../docs/_docs/csle-ryu; cd ../../
echo "Generating csle-system-identification API documentation"
cd csle-system-identification/docs; sphinx-apidoc -f -o source/ ../src/csle_system_identification/; make html; cp -r build/html/* ../../../../docs/_docs/csle-system-identification; cd ../../
echo "Generating gym-csle-stopping-game API documentation"
cd gym-csle-stopping-game/docs; sphinx-apidoc -f -o source/ ../src/gym_csle_stopping_game/; make html; cp -r build/html/* ../../../../docs/_docs/gym-csle-stopping-game; cd ../../
echo "Generating csle-cluster API documentation"
cd csle-cluster/docs; sphinx-apidoc -f -o source/ ../src/csle_cluster/; make html; cp -r build/html/* ../../../../docs/_docs/csle-cluster; cd ../../
echo "Generating gym-csle-intrusion-response-game API documentation"
cd gym-csle-intrusion-response-game/docs; sphinx-apidoc -f -o source/ ../src/gym_csle_intrusion_response_game/; make html; cp -r build/html/* ../../../../docs/_docs/gym-csle-intrusion-response-game; cd ../../
echo "Generating csle-tolerance API documentation"
cd csle-tolerance/docs; sphinx-apidoc -f -o source/ ../src/csle_tolerance/; make html; cp -r build/html/* ../../../../docs/_docs/csle-tolerance; cd ../../
echo "Generating gym-csle-apt-game API documentation"
cd gym-csle-apt-game/docs; sphinx-apidoc -f -o source/ ../src/gym_csle_apt_game/; make html; cp -r build/html/* ../../../../docs/_docs/gym-csle-apt-game; cd ../../
echo "Generating gym-csle-cyborg API documentation"
cd gym-csle-cyborg/docs; sphinx-apidoc -f -o source/ ../src/gym_csle_cyborg/; make html; cp -r build/html/* ../../../../docs/_docs/gym-csle-cyborg; cd ../../
echo "Generating csle-attack-profiler API documentation"
cd csle-attack-profiler/docs; sphinx-apidoc -f -o source/ ../src/csle-attack-profiler/; make html; cp -r build/html/* ../../../../docs/_docs/csle-attack-profiler; cd ../../