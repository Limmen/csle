from typing import List
from gym_pycr_ctf.dao.network.env_mode import EnvMode
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.dao.container_config.containers_config import ContainersConfig
from gym_pycr_ctf.dao.container_config.flags_config import FlagsConfig
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.envs_model.config.random.pycr_ctf_random_base import PyCrCTFRandomBase
from gym_pycr_ctf.envs_model.config.random.pycr_ctf_random_v1 import PyCrCTFRandomV1
from gym_pycr_ctf.envs_model.logic.exploration.random_exploration_policy import RandomExplorationPolicy


# -------- Version 1 Generated Sim ------------
class PyCRCTFRandomManyGeneratedSim1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str,
                 containers_configs: List[ContainersConfig], flags_configs: List[FlagsConfig], idx : int,
                 num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = max(list(map(lambda x: len(x.containers), containers_configs)))
        containers_config = containers_configs[idx]
        flags_config = flags_configs[idx]
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = PyCrCTFRandomV1.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                subnet_mask=containers_config.subnet_mask,
                                                                hacker_ip=containers_config.agent_ip)
            defender_action_conf = PyCrCTFRandomV1.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.subnet_mask, )
            env_config = PyCrCTFRandomV1.env_config(containers_config=containers_config,
                                                    flags_config=flags_config,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config,
                                                    num_nodes=num_nodes-1)
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = True
            env_config.attacker_max_exploration_steps = 5000000
            env_config.attacker_max_exploration_trajectories = 10
            env_config.max_episode_length = 60
            env_config.attacker_max_exploration_steps = 5000000
            env_config.attacker_alerts_coefficient = 0
            env_config.attacker_cost_coefficient = 0
            env_config.attacker_base_step_reward = -1
            env_config.use_upper_bound_pi_star_attacker = False
            env_config.detection_alerts_threshold = -1
            env_config.emulate_detection = True
            env_config.detection_prob_factor = 0.05
            env_config.randomize_attacker_starting_state = False
            env_config.idx = idx

            # exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            # env_config.attacker_exploration_policy = exp_policy
            # env_config.domain_randomization = False
            # env_config.simulate_detection = False
            # env_config.attacker_max_exploration_steps = 50000
            # env_config.attacker_max_exploration_trajectories = 500
            # env_config.env_mode = EnvMode.GENERATED_SIMULATION
            # env_config.save_trajectories = False
            # env_config.checkpoint_dir = checkpoint_dir
            # env_config.checkpoint_freq = 1000
            # env_config.max_episode_length = 100
            # env_config.attacker_alerts_coefficient = 0
            # env_config.attacker_cost_coefficient = 0
            # env_config.attacker_base_step_reward = -1
            # env_config.idx = idx
            # env_config.use_upper_bound_pi_star_attacker = False
            # env_config.detection_alerts_threshold = -1
            # env_config.emulate_detection = True
            # # env_config.detection_prob_factor = 0.05
            # env_config.detection_prob_factor = 0.05
            # env_config.randomize_attacker_starting_state = False
        super().__init__(env_config=env_config)
