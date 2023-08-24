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
pip uninstall csle-common
pip uninstall csle-collector
pip uninstall csle-agents
pip uninstall csle-ryu
pip uninstall csle-rest
pip uninstall csle-system-identification
pip uninstall csle-attacker
cd emulation-system && make rm
cd metastore; make clean
```

<p class="captionFig">
Listing 89: Commands to uninstall CSLE.
</p>