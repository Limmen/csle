# Simulation environments

This folder contains simulation environments.

- *Stopping game* [env](stopping_game): A two-player zero-sum one-sided partially observed stochastic game based on the optimal stopping formulation
- *Stopping MDP from the attacker's perspective* [env](stopping_mdp_attacker): A fully observed optimal stopping problem from the attacker's perspective
- *Stopping POMDP from the defender's perspective* [env](stopping_pomdp_defender): A partially observed optimal stopping problem from the defender's perspective
- *Intrusion recovery POMDP from the defender's perspective* [env](intrusion_recovery_pomdp_defender): A POMDP for intrusion recovery
- *Intrusion response CMDP from the defender's perspective* [env](intrusion_response_cmdp_defender): A CMDP for intrusion response
- *Local intrusion response POMDP from the attacker's perspective* [env](local_intrusion_response_pomdp_attacker): A local intrusion response POMDP from the attacker's perspective
- *Local intrusion response POMDP from the defender's perspective* [env](local_intrusion_response_pomdp_defender): A local intrusion response POMDP from the defender's perspective
- *Workflow intrusion response POMDP from the defender's perspective* [env](workflow_intrusion_response_pomdp_defender): A workflow intrusion response POMDP from the defender's perspective
- *Workflow intrusion response POMDP from the attacker's perspective* [env](workflow_intrusion_response_pomdp_attacker): A workflow intrusion response POMDP from the attacker's perspective
- *APT game* [env](apt_game): A two-player zero-sum one-sided partially observed stochastic APT game
- *APT MDP from the attacker's perspective* [env](apt_mdp_attacker): A fully observed optimal stopping problem from the attacker's perspective
- *APT POMDP from the defender's perspective* [env](apt_pomdp_defender): A partially observed optimal stopping problem from the defender's perspective

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