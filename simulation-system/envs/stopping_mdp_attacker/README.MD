# Optimal stopping MDP from the attacker's perspective 

A MDP based on the optimal stopping formulation of intrusion prevention from  
(Hammar and Stadler 2021, https://arxiv.org/abs/2111.00289).

- Attacker actions: Stop, Continue
- Observations: Severe IDS alerts, Warning IDS alerts, Login attempts

## Overview
<p align="center">
<img src="env.png" width="600">
</p>

## Useful commands

```bash
make install # installs the environment in the metastore
make uninstall # uninstalls the environment from the metastore
make clean_config # cleans the materialized config file    
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](../../../../../LICENSE.md)

Creative Commons

(C) 2020-2025, Kim Hammar