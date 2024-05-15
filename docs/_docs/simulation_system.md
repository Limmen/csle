---
title: Simulation System 
permalink: /docs/simulation-system/
---

## Simulation System

The simulation system uses the data collected from the emulation system to instantiate simulations, which are used to
find effective defender strategies through reinforcement learning and other optimization techniques (see Fig. 16). It consists of
simulation configurations and Python libraries that implement numerical algorithms for computing defender strategies,
for simulating Markov decision processes, and for system identification.

<p align="center">
<img src="./../../img/simulation_system.png" width="75%">
<p class="captionFig">
Figure 16: Overview of the simulation system; it uses data collected from emulated 
IT infrastructures to instantiate simulations of Markov decision processes (MDPs) 
and to optimize defender strategies through reinforcement learning and other optimization methods.
</p>
</p>

### Simulation Environments

The simulation environments are listed in Table 17. Similar to an emulation execution, which is defined by an emulation
configuration, a simulation is defined by a *simulation configuration*, which includes the set of properties listed in
Table 18. Each simulation environment is implemented in Python and the configuration files are stored in the metastore.
Simulations are typically based either on Markov decision processes or game-theoretic models.

| Name                                       | Description                                                           |
|--------------------------------------------|-----------------------------------------------------------------------|
| Optimal stopping game                      | Zero-sum one-sided partially observed stochastic game.                |
| Optimal stopping MDP                       | MDP based on an optimal stopping formulation.                         |
| Optimal stopping POMDP                     | POMDP based on an optimal stopping formulation.                       |
| Local intrusion response game              | Zero-sum partially observed stochastic game with public observations. |
| Local intrusion response POMDP attacker    | POMDP for the attacker in the local intrusion response game.          |
| Local intrusion response POMDP defender    | POMDP for the defender in the local intrusion response game.          |
| Workflow intrusion response game           | Zero-sum partially observed stochastic game with public observations. |
| Workflow intrusion response POMDP attacker | POMDP for the attacker in the workflow intrusion response game.       |
| Workflow intrusion response POMDP defender | POMDP for the defender in the workflow intrusion response game.       |
| APT stopping game                          | Zero-sum one-sided partially observed stochastic APT game.            |
| APT stopping MDP                           | MDP based on an optimal stopping formulation of APT.                  |
| APT stopping POMDP                         | POMDP based on an optimal stopping formulation of APT.                |
| Intrusion recovery POMDP                   | POMDP formulation of intrusion recovery                               |
| Intrusion response CMDP                    | CMDP formulation of intrusion response and replication factor control |

<p class="captionFig">
Table 17: Simulation environments.
</p>

| *Configuration property*               | *Description*                                                            |
|----------------------------------------|--------------------------------------------------------------------------|
| `name`                                 | Name of the simulation environment.                                      |
| `gym_env_name`                         | Name of the OpenAI gym environment.                                      |
| `descr`                                | Description of the simulation environment.                               |
| `simulation_env_input_config`          | Input configuration to the simulation.                                   |
| `players_config`                       | Players configuration of the simulation.                                 |
| `state_space_config`                   | State space configuration of the simulation.                             |
| `joint_action_space_config`            | Joint action space configuration of the simulation.                      |
| `joint_observation_space_config`       | Joint observation space config of the simulation.                        |
| `time_step_type`                       | Time-step type of the simulation                                         |
| `reward_function_config`               | Reward function configuration of the of the simulation.                  |
| `transition_operator_config`           | Transition operator configuration of the simulation.                     |
| `observation_function_config`          | Observation function configuration of the simulation.                    |
| `emulation_statistic_id`               | Id of the emulation statistic.                                           |
| `initial_state_distribution_config`    | Initial state distribution configuration of the simulation.              |
| `version`                              | Version of the simulation environment.                                   |
| `env_parameters_config`                | Parameters that are not part of the state but that the poliy depends on. |
| `plot_transition_probabilities`        | Boolean parameter whether to plot transition probabilities or not.       |
| `plot_observation_function`            | Boolean parameter whether to plot the observation function or not.       |
| `plot_reward_function`                 | Boolean parameter whether to plot the reward function or not.            |

<p class="captionFig">
Table 18: Properties of a simulation environment configuration.
</p>

### Numerical Algorithms

The numerical algorithms for strategy optimization and system identification are 
listed in Table 19. These algorithms are implemented in Python and are based on 
PyTorch, NumPy, PuLP, CvxPy, Openspiel, Stable-Baselines3, emukit, and cma. 
A code example of running the Q-learning algorithm is shown below:

```python
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.q_learning.q_learning_agent import QLearningAgent
import csle_agents.constants.constants as agents_constants
# Select simulation configuration
simulation_env_config = MetastoreFacade.get_simulation_by_name(
"csle-stopping-mdp-attacker-002")
# Setup experiment with hyperparameters
experiment_config = ExperimentConfig(output_dir="..", title="Q-learning test", random_seeds=[..], agent_type=AgentType.Q_LEARNING, hparams={..`, player_type=PlayerType.ATTACKER, player_idx=1)
agent = QLearningAgent(simulation_env_config=simulation_env_config, experiment_config=experiment_config, save_to_metastore=True)
# Run the algorithm
experiment_execution = agent.train()
# Save the results and the learned policies
MetastoreFacade.save_experiment_execution(experiment_execution)
for policy in experiment_execution.result.policies.values():
    MetastoreFacade.save_tabular_policy(tabular_policy=policy)
```

<p class="captionFig">
Listing 2: Example of strategy optimization through the Q-learning algorithm in CSLE.
</p>

| *Name*                                                           | *Algorithm type*          |
|------------------------------------------------------------------|---------------------------|
| Bayesian optimization                                            | Black-box optimization    |
| Cross-entropy method                                             | Black-box optimization    |
| Simulated annealing                                              | Black-box optimization    |
| Nelder-Mead                                                      | Black-box optimization    |
| Particle swarm                                                   | Black-box optimization    |
| CMA-ES                                                           | Evolutionary computation  |
| Differential evolution                                           | Evolutionary computation  |
| Deep Q-network (DQN)                                             | Reinforcement learning    |
| Fictitious Self-Play                                             | Computational game theory |
| Heuristic Search Value Iteration (HSVI)                          | Dynamic programming       |
| Heuristic Search Value Iteration (HSVI) for one-sided game POSGs | Computational game theory |
| Kiefer Wolfowitz                                                 | Stochastic approximation  |
| Linear programming                                               | Computational game theory |
| Policy iteration                                                 | Dynamic programming       |
| Value iteration                                                  | Dynamic programming       |
| Proximal Policy Optimization (PPO)                               | Reinforcement learning    |
| Q-learning                                                       | Reinforcement learning    |
| Random search                                                    | Black-box optimization    |
| REINFORCE                                                        | Reinforcement learning    |
| SARSA                                                            | Reinforcement learning    |
| Shapley iteration                                                | Computational game theory |
| Sondik's value iteration                                         | Dynamic programming       |
| T-FP                                                             | Reinforcement learning    |
| T-SPSA                                                           | Reinforcement learning    |
| Expectation maximization                                         | System identification     |
| POMCP                                                            | POMDP planning            |
| Phasic Policy Gradient (PPG)                                     | Reinforcement learning    |

<p class="captionFig">
Table 19: Numerical algorithms.
</p>