---
title: Uninstalling CSLE
permalink: /docs/uninstalling/
---

## Uninstalling CSLE

To uninstall CSLE, run the commands:

```bash
csle rm all
csle clean emulations
csle rm emulations
pip uninstall gym-csle-stopping-game
pip uninstall gym-csle-intrusion-response-game
pip uninstall gym-csle-apt-game
pip uninstall gym-csle-cyborg
pip uninstall csle-tolerance
pip uninstall csle-common
pip uninstall csle-attack-profiler
pip uninstall csle-collector
pip uninstall csle-agents
pip uninstall csle-ryu
pip uninstall csle-rest
pip uninstall csle-system-identification
pip uninstall csle-attacker
pip uninstall csle-base
pip uninstall csle-cli
pip uninstall csle-cluster
cd emulation-system && make rm
cd metastore; make clean
```

<p class="captionFig">
Listing 101: Commands to uninstall CSLE.
</p>

Also remove the `CSLE_HOME` environment variable from `.bashrc`.