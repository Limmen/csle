# Simulation environments

This folder contains simulation environments.

- Version: **001** [./001](001):
  - *Stopping game* [level_1](001/stopping_game): A two-player zero-sum one-sided partially observed stochastic game based on the optimal stopping formulation
  - *Stopping MDP from the attacker's perspective* [level_1](001/stopping_mdp_attacker): A fully observed optimal stopping problem from the attacker's perspective
  - *Stopping POMDP from the defender's perspective* [level_1](001/stopping_pomdp_defender): A partially observed optimal stopping problem from the defender's perspective

## Useful commands:

- Install all emulations:
  ```bash
  make install
   ```

- Uninstall all emulations:
  ```bash
  make uninstall
   ```

- Clean the configuration of all simulations:
  ```bash
  make clean_config
   ```