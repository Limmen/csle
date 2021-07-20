# `gym-pycr-ctf`

`gym-pycr-ctf` is a reinforcement learning environment for automating the "first line of defense" against
network intrusions. Specifically the environment focuses on reconnaissance, password vulnerabilities, RCE vulnerabilities, 
intrusion detection, and dictionary attacks. The environment provides a MDP (POMDP) or Markov Game interface for 
OpenAI Gym that can be used to train reinforcement learning agents. 

Moreover, the repository contains code to reproduce baseline results for various reinforcement learning algorithms, including:

- DQN
- REINFORCE with baseline
- PPO
- AC3

## Requirements

- Python 3.5+
- OpenAI Gym
- NumPy
- Pyglet (OpenGL 3D graphics)
- GPU for 3D graphics acceleration (optional)
- Jsonpickle (for configuration files)
- Torch (for baseline algorithms)
- Paramiko (for SSH tunnels)
- Docker (for interacting with the emulations)


## Installation & Tests

```bash
# install from pip
pip install gym-pycr-ctf==1.0.0
# local install from source
$ pip install -e gym-pycr-ctf
# force upgrade deps
$ pip install -e gym-pycr-ctf --upgrade

# git clone and install from source
git clone https://github.com/Limmen/pycr
cd pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf
pip3 install -e .
```

## Usage
The environment can be accessed like any other OpenAI environment with `gym.make`.
Once the environment has been created, the API functions
`step()`, `reset()`, `render()`, and `close()` can be used to train any RL algorithm of
your preference.

```python
import numpy as np
import gym
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig

# Specify configuration to connect to the emulation
emulation_config = EmulationConfig(agent_ip="172.18.9.191", agent_username="agent", agent_pw="agent",
                                   server_connection=False)

# Create gym interface
env_name = "pycr-ctf-level-9-emulation-v1"
env = gym.make(env_name, env_config=None, emulation_config=emulation_config)
num_actions_attacker = env.env_config.attacker_action_conf.num_actions
attacker_actions = np.array(list(range(num_actions_attacker)))
num_actions_defender = env.env_config.defender_action_conf.num_actions
defender_actions = np.array(list(range(num_actions_defender)))

for i in range(10):

    # Sample an action
    legal_attacker_actions = list(filter(lambda x: env.is_attack_action_legal(x, env.env_config, env.env_state), attacker_actions))
    legal_defender_actions = list(filter(lambda x: env.is_defense_action_legal(x, env.env_config, env.env_state), defender_actions))    
    attacker_action = np.random.choice(legal_attacker_actions )
    defender_action = np.random.choice(legal_defender_actions )
    action = (attacker_action, defender_action)
    
    # Step in the environment
    obs, reward, done, info = env.step(action)
    attacker_reward, defender_reward = reward
    attacker_obs, defender_obs = obs
    
    # env.render()

    if done:        
        env.reset()

env.reset()
env.close()
```

## Manual Control
You can run the environment in a mode of "manual control" as well:

```python
import gym
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv, PyCRctfLevel1emulation1Env
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.agents.manual.manual_attacker_agent import ManualAttackerAgent

# Specify configuration for connecting to the emulation
emulation_config = EmulationConfig(agent_ip="172.18.7.191", agent_username="agent", agent_pw="agent",
                                   port_forward_next_port=4600,
                                   server_connection=True, warmup=False, warmup_iterations=500,
                                   server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
                                   server_username="kim", server_ip="172.31.212.92"
                                   )

# Create gym interface
env = gym.make("pycr-ctf-level-7-emulation-v1", env_config=None, emulation_config=emulation_config)

# Manual Control with GUI
ManualAttackerAgent(env=env, env_config=env.env_config)
```

## GUI

<p align="center">
<img src="docs/gui_1.png" width="1200">
</p>

## System Identification and Collection of Traces

<p align="center">
<img src="docs/system_id_1.png" width="1200">
</p>

<p align="center">
<img src="docs/system_id_2.png" width="1200">
</p>

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

Creative Commons

[LICENSE](../../../../../LICENSE.md)

(C) 2021, Kim Hammar