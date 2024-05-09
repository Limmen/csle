---
title: Dependency Management
permalink: /docs/dependencies/
---

## Dependency Management

Python dependencies in CSLE are managed with PyPi and JavaScript dependencies are managed with npm.

The Python dependencies are defined in the following files:

- `csle/simulation-system/libs/csle-base/requirements.txt`
- `csle/simulation-system/libs/csle-base/requirements_dev.txt`
- `csle/simulation-system/libs/csle-base/setup.cfg`
- `csle/simulation-system/libs/csle-agents/requirements.txt`
- `csle/simulation-system/libs/csle-agents/requirements_dev.txt`
- `csle/simulation-system/libs/csle-agents/setup.cfg`
- `csle/simulation-system/libs/csle-attacker/requirements.txt`
- `csle/simulation-system/libs/csle-attacker/requirements_dev.txt`
- `csle/simulation-system/libs/csle-attacker/setup.cfg`
- `csle/simulation-system/libs/csle-cli/requirements.txt`
- `csle/simulation-system/libs/csle-cli/requirements_dev.txt`
- `csle/simulation-system/libs/csle-cli/setup.cfg`
- `csle/simulation-system/libs/csle-cluster/requirements.txt`
- `csle/simulation-system/libs/csle-cluster/requirements_dev.txt`
- `csle/simulation-system/libs/csle-cluster/setup.cfg`
- `csle/simulation-system/libs/csle-collector/requirements.txt`
- `csle/simulation-system/libs/csle-collector/requirements_dev.txt`
- `csle/simulation-system/libs/csle-collector/setup.cfg`
- `csle/simulation-system/libs/csle-common/requirements.txt`
- `csle/simulation-system/libs/csle-common/requirements_dev.txt`
- `csle/simulation-system/libs/csle-common/setup.cfg`
- `csle/simulation-system/libs/csle-defender/requirements.txt`
- `csle/simulation-system/libs/csle-defender/requirements_dev.txt`
- `csle/simulation-system/libs/csle-defender/setup.cfg`
- `csle/simulation-system/libs/csle-rest-api/requirements.txt`
- `csle/simulation-system/libs/csle-rest-api/requirements_dev.txt`
- `csle/simulation-system/libs/csle-rest-api/setup.cfg`
- `csle/simulation-system/libs/csle-ryu/requirements.txt`
- `csle/simulation-system/libs/csle-ryu/requirements_dev.txt`
- `csle/simulation-system/libs/csle-ryu/setup.cfg`
- `csle/simulation-system/libs/csle-system-identification/requirements.txt`
- `csle/simulation-system/libs/csle-system-identification/requirements_dev.txt`
- `csle/simulation-system/libs/csle-system-identification/setup.cfg`
- `csle/simulation-system/libs/gym-csle-stopping-game/requirements.txt`
- `csle/simulation-system/libs/gym-csle-stopping-game/requirements_dev.txt`
- `csle/simulation-system/libs/gym-csle-stopping-game/setup.cfg`
- `csle/simulation-system/libs/gym-csle-apt-game/requirements.txt`
- `csle/simulation-system/libs/gym-csle-apt-game/requirements_dev.txt`
- `csle/simulation-system/libs/gym-csle-apt-game/setup.cfg`
- `csle/simulation-system/libs/gym-csle-cyborg/requirements.txt`
- `csle/simulation-system/libs/gym-csle-cyborg/requirements_dev.txt`
- `csle/simulation-system/libs/gym-csle-cyborg/setup.cfg`- 
- `csle/simulation-system/libs/gym-csle-intrusion-response-game/requirements.txt`
- `csle/simulation-system/libs/gym-csle-intrusion-response-game/requirements_dev.txt`
- `csle/simulation-system/libs/gym-csle-intrusion-response-game/setup.cfg`
- `csle/simulation-system/libs/csle-tolerance/requirements.txt`
- `csle/simulation-system/libs/csle-tolerance/requirements_dev.txt`
- `csle/simulation-system/libs/csle-tolerance/setup.cfg`
- `csle/simulation-system/libs/csle-attack-profiler/requirements.txt`
- `csle/simulation-system/libs/csle-attack-profiler/requirements_dev.txt`
- `csle/simulation-system/libs/csle-attack-profiler/setup.cfg`

These files need to be updated whenever a Python dependency is added or removed. 
The dependency structure among the CSLE Python libraries is shown in Fig. 31.

<p align="center">
<img src="./../../img/dependencies.png" width="75%">
<p class="captionFig">
Figure 31: Dependency graph showing the dependencies among the CSLE Python libraries; 
an arrow from X to Y indicates that X depends on Y; dependency arrows are transitive.
</p>
</p>

JavaScript dependencies are defined in the file `csle/management-system/csle-mgmt-webapp/package.json`. 
This file should be updated whenever a JavaScript dependency is added or removed.

