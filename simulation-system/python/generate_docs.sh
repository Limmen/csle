#!/bin/bash

echo "Generating csle-agents API documentation"
cd csle-agents/docs; sphinx-apidoc -f -o source/ ../csle_agents/; make html; cp -r build/html ../../../../docs/_docs/csle-agents; cd ../../
echo "Generating csle-attacker API documentation"
cd csle-attacker/docs; sphinx-apidoc -f -o source/ ../csle_attacker/; make html; cp -r build/html ../../../../docs/_docs/csle-attacker; cd ../../
echo "Generating csle-collector API documentation"
cd csle-collector/docs; sphinx-apidoc -f -o source/ ../csle_collector/; make html; cp -r build/html ../../../../docs/_docs/csle-collector; cd ../../
echo "Generating csle-common API documentation"
cd csle-common/docs; sphinx-apidoc -f -o source/ ../csle_common/; make html; cp -r build/html ../../../../docs/_docs/csle-common; cd ../../
echo "Generating csle-defender API documentation"
cd csle-defender/docs; sphinx-apidoc -f -o source/ ../csle_defender/; make html; cp -r build/html ../../../../docs/_docs/csle-defender; cd ../../
echo "Generating csle-rest-api API documentation"
cd csle-rest-api/docs; sphinx-apidoc -f -o source/ ../csle_rest_api/; make html; cp -r build/html ../../../../docs/_docs/csle-rest-api; cd ../../
echo "Generating csle-ryu API documentation"
cd csle-ryu/docs; sphinx-apidoc -f -o source/ ../csle_ryu/; make html; cp -r build/html ../../../../docs/_docs/csle-ryu; cd ../../
echo "Generating csle-system-identification API documentation"
cd csle-system-identification/docs; sphinx-apidoc -f -o source/ ../csle_system_identification/; make html; cp -r build/html ../../../../docs/_docs/csle-system-identification; cd ../../
echo "Generating gym-csle-stopping-game API documentation"
cd gym-csle-stopping-game/docs; sphinx-apidoc -f -o source/ ../gym_csle_stopping_game/; make html; cp -r build/html ../../../../docs/_docs/gym-csle-stopping-game; cd ../../
