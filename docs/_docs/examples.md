---
title: Examples
permalink: /docs/examples/
---

## Examples

Examples of CSLE usages can be found  
<a href="https://github.com/Limmen/csle/examples">here</a>.
The folder in the above link includes examples of the four main
usages of CSLE: (1) data collection; (2) system identification;
(3) strategy training; and (4), strategy evaluation.

### Data Collection

A common usage of CSLE is to run emulated cyber attacks against an emulated IT infrastructure and
record the resulting traces of system metrics and logs.
To do this with CSLE, you have to a) choose a running emulation execution; b)
define the sequence of attacker actions; c) define the sequence of defender actions;
and d), start the attacker and defender sequences.
A code example of performing these steps using the CSLE APIs is given below.

```python
# Imports
import csle_common.constants.constants as constants
from ..emulation_attacker_action import EmulationAttackerAction
from ..emulation_defender_action import EmulationDefenderAction
from ..emulation_attacker_stopping_actions import EmulationAttackerStoppingActions
from ..emulation_defender_stopping_actions import EmulationDefenderStoppingActions
from ..emulation_env_config import EmulationEnvConfig
from ..metastore_facade import MetastoreFacade
from ..container_controller import ContainerController
from csle_system_identification.emulator import Emulator
# Select emulation execution
execution = get_emulation_execution(ip_first_octet=.., emulation_name=..)
emulation_env_config = executions.emulation_env_config

attacker_sequence = [..] # Define attacker sequence
defender_sequence = [..] # Define defender sequence

# Starting the attacker and defender
Emulator.run_action_sequences(
     emulation_env_config=emulation_env_config,
     attacker_sequence=attacker_sequence,
     defender_sequence=defender_sequence)

# Extract recorded traces and statistics
statistics = MetastoreFacade.list_emulation_statistics()
traces = MetastoreFacade.list_emulation_traces()
```

<p class="captionFig">
Listing 116: Example of collecting attack and system traces with CSLE.
</p>

### System Identification
A key step in CSLE's reinforcement learning method is *system identification* (see Fig. 1).
In this step, data collected from emulated IT infrastructures are used to
identify system parameters and models.
A code example of system identification with CSLE is given below.

```python
# Imports
import csle_common.constants.constants as constants
from csle_common.dao.system_identification.system_identification_config import SystemIdentificationConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.system_identification.system_model_type import SystemModelType
from csle_common.dao.training.hparam import HParam
from csle_system_identification.expectation_maximization.expectation_maximization_algorithm import ExpectationMaximizationAlgorithm
import csle_system_identification.constants.constants as sid_consts

# Select emulation config
emulation_env_config = MetastoreFacade.get_emulation_by_name("csle-level9-070")

# Extract statistics from the metastore
emulation_statistic = MetastoreFacade.get_emulation_statistic(id=1)
system_identifcation_config = SystemIdentificationConfig( 
    output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR`em_level9_test",
    title="Expectation-Maximization level 9 test",
    model_type=SystemModelType.GAUSSIAN_MIXTURE,
    log_every=1,
    hparams={..`)
algorithm = ExpectationMaximizationAlgorithm(
    emulation_env_config=emulation_env_config,
    emulation_statistics=emulation_statistic,
    system_identification_config=system_identifcation_config)

# Run the algorithm
system_model = algorithm.fit()

# Save system model in metastore
MetastoreFacade.save_gaussian_mixture_system_model(
gaussian_mixture_system_model=system_model) 
```

<p class="captionFig">
Listing 117: Example of system identification through expectation maximization with CSLE.
</p>

### Strategy Training
CSLE includes several numerical algorithms for optimizing defender strategies, e
.g. reinforcement learning algorithms, dynamic programming algorithms,
game-theoretic algorithms, and general optimization algorithms.
A code example of learning security strategies through
the Proximal Policy Optimization (PPO) reinforcement learning algorithm is given below.

```python
# Imports
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.ppo.ppo_agent import PPOAgent
import csle_agents.constants.constants as agents_constants

# Select emulation configuration
emulation_env_config = MetastoreFacade.get_emulation_by_name("..")

# Select simulation environment
simulation_env_config = MetastoreFacade.get_simulation_by_name("..")

# Setup experiment with hyperparameters
experiment_config = ExperimentConfig(output_dir="..", 
                                     title="PPO test", 
                                     random_seeds=[399,9141], 
                                     agent_type=AgentType.PPO, 
                                     log_every=1, hparams={`, 
                                     player_type=PlayerType.DEFENDER, player_idx=0)
agent = PPOAgent(emulation_env_config=emulation_env_config, 
                 simulation_env_config=simulation_env_config, 
                 experiment_config=experiment_config)

# Run the algorithm
experiment_execution = agent.train()

# Save the results and the learned policies
MetastoreFacade.save_experiment_execution(experiment_execution)
for policy in experiment_execution.result.policies.values():
    MetastoreFacade.save_ppo_policy(ppo_policy=policy)
```

<p class="captionFig">
Listing 118: Example of strategy optimization through the Proximal Policy Optimization (PPO) reinforcement learning algorithm in CSLE.
</p>

### Strategy Evaluation

CSLE can be used to evaluate learned security strategies in emulated infrastructures running
on the emulation system (see Fig. 1).
Below is a code example of strategy evaluation with CSLE.

```python
# Imports
import gymnasium as gym
import csle_common.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy
from gym_csle_stopping_game.envs.stopping_game_pomdp_defender_env import StoppingGamePomdpDefenderEnv
from csle_system_identification.environment_evaluations.stopping_game_emulation_eval import StoppingGameEmulationEval
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.training.agent_type import AgentType

# Select emulation to be used as evaluation environment
emulation_env_config = MetastoreFacade.get_emulation_by_name("..")

# Select simulation environment
simulation_env_config = MetastoreFacade.get_simulation_by_name("..")
config = simulation_env_config.simulation_env_input_config
env = gym.make(simulation_env_config.gym_env_name, config=config)

# Define security policy to evaluate
tspsa_policy = MultiThresholdStoppingPolicy(..)

# Perform the evaluation
StoppingGameEmulationEval.emulation_evaluation(
    env=env, n_episodes=10, intrusion_seq=[], 
    defender_policy=tspsa_policy, 
    emulation_env_config=emulation_env_config, 
    simulation_env_config=simulation_env_config)
```

<p class="captionFig">
Listing 119: Example of evaluating learned security strategies in the emulation system of CSLE.
</p>

