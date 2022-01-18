from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.dao.network.env_mode import EnvMode
from csle_common.dao.container_config.containers_config import ContainersConfig
from csle_common.dao.container_config.flags_config import FlagsConfig
from csle_common.envs_model.logic.exploration.random_exploration_policy import RandomExplorationPolicy
from gym_csle_ctf.dao.network.env_config import csleEnvConfig
from gym_csle_ctf.envs.csle_ctf_env import CSLECTFEnv
from gym_csle_ctf.envs_model.config.random.csle_ctf_random_base import CSLECTFRandomBase
from gym_csle_ctf.envs_model.config.random.csle_ctf_random_v1 import CSLECTFRandomV1
from gym_csle_ctf.envs_model.config.random.csle_ctf_random_v2 import CSLECTFRandomV2
from gym_csle_ctf.envs_model.config.random.csle_ctf_random_v3 import CSLECTFRandomV3
from gym_csle_ctf.envs_model.config.random.csle_ctf_random_v4 import CSLECTFRandomV4


# -------- Version 1 Generated Sim ------------
class CSLECTFRandomGeneratedSim1Env(CSLECTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: csleEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = CSLECTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = CSLECTFRandomV1.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                         subnet_mask=containers_config.internal_subnet_mask,
                                                                         hacker_ip=containers_config.agent_ip)
            defender_action_conf = CSLECTFRandomV1.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.internal_subnet_mask)
            env_config = CSLECTFRandomV1.env_config(containers_config=containers_config,
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
            env_config.domain_randomization = False
            env_config.attacker_max_exploration_steps = 500
            env_config.attacker_max_exploration_trajectories = 10
            env_config.max_episode_length = 100
            env_config.attacker_alerts_coefficient = 0
            env_config.attacker_cost_coefficient = 0
            env_config.attacker_base_step_reward = -1
            env_config.use_upper_bound_pi_star_attacker = False
            env_config.detection_alerts_threshold = -1
            env_config.emulate_detection = True
            env_config.detection_prob_factor = 0.05
            env_config.randomize_attacker_starting_state = False
        super(CSLECTFRandomGeneratedSim1Env, self).__init__(env_config=env_config)


# -------- Version 1 Generated Sim With Costs ------------
class CSLECTFRandomGeneratedSimWithCosts1Env(CSLECTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: csleEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = CSLECTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = CSLECTFRandomV1.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                         subnet_mask=containers_config.internal_subnet_mask,
                                                                         hacker_ip=containers_config.agent_ip)
            defender_action_conf = CSLECTFRandomV1.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.internal_subnet_mask)
            env_config = CSLECTFRandomV1.env_config(containers_config=containers_config,
                                                    flags_config=flags_config,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config,
                                                    num_nodes=num_nodes-1)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.attacker_filter_illegal_actions = False
            env_config.max_episode_length = 100
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.attacker_exploration_filter_illegal = True
        super(CSLECTFRandomGeneratedSimWithCosts1Env, self).__init__(env_config=env_config)


# -------- Version 2 Generated Sim ------------
class CSLECTFRandomGeneratedSim2Env(CSLECTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: csleEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = CSLECTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = CSLECTFRandomV2.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                         subnet_mask=containers_config.internal_subnet_mask,
                                                                         hacker_ip=containers_config.agent_ip)
            defender_action_conf = CSLECTFRandomV2.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.internal_subnet_mask)
            env_config = CSLECTFRandomV2.env_config(containers_config=containers_config,
                                                    flags_config=flags_config,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config,
                                                    num_nodes=num_nodes-1)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.attacker_exploration_filter_illegal = True
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.attacker_filter_illegal_actions = False
            env_config.max_episode_length = 50
        super(CSLECTFRandomGeneratedSim2Env, self).__init__(env_config=env_config)


# -------- Version 2 Generated Sim With Costs ------------
class CSLECTFRandomGeneratedSimWithCosts2Env(CSLECTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: csleEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = CSLECTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = CSLECTFRandomV2.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                         subnet_mask=containers_config.internal_subnet_mask,
                                                                         hacker_ip=containers_config.agent_ip)
            defender_action_conf = CSLECTFRandomV2.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.internal_subnet_mask)
            env_config = CSLECTFRandomV2.env_config(containers_config=containers_config,
                                                    flags_config=flags_config,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config,
                                                    num_nodes=num_nodes-1)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_filter_illegal = True
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.attacker_filter_illegal_actions = False
            env_config.max_episode_length = 50
        super(CSLECTFRandomGeneratedSimWithCosts2Env, self).__init__(env_config=env_config)


# -------- Version 3, Generated Simulation ------------
class CSLECTFRandomGeneratedSim3Env(CSLECTFEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: csleEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = CSLECTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = CSLECTFRandomV3.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                         subnet_mask=containers_config.internal_subnet_mask,
                                                                         hacker_ip=containers_config.agent_ip)
            defender_action_conf = CSLECTFRandomV3.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.internal_subnet_mask)
            env_config = CSLECTFRandomV3.env_config(containers_config=containers_config,
                                                    flags_config=flags_config,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config,
                                                    num_nodes=num_nodes-1)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_filter_illegal = True
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.attacker_filter_illegal_actions = False
            env_config.max_episode_length = 50
        super(CSLECTFRandomGeneratedSim3Env, self).__init__(env_config=env_config)


# -------- Version 3, Generated Simulation With Costs ------------
class CSLECTFRandomGeneratedSimWithCosts3Env(CSLECTFEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: csleEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = CSLECTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = CSLECTFRandomV3.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                         subnet_mask=containers_config.internal_subnet_mask,
                                                                         hacker_ip=containers_config.agent_ip)
            defender_action_conf = CSLECTFRandomV3.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.internal_subnet_mask)
            env_config = CSLECTFRandomV3.env_config(containers_config=containers_config,
                                                    flags_config=flags_config,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config,
                                                    num_nodes=num_nodes-1)
            env_config.attacker_cost_coefficient = 1
            env_config.attacker_alerts_coefficient = 1
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_filter_illegal = True
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.attacker_filter_illegal_actions = False
            env_config.max_episode_length = 50
        super(CSLECTFRandomGeneratedSimWithCosts3Env, self).__init__(env_config=env_config)


# -------- Version 4, Generated Simulation ------------
class CSLECTFRandomGeneratedSim4Env(CSLECTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """

    def __init__(self, env_config: csleEnvConfig, emulation_config: EmulationConfig, checkpoint_dir: str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes: int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = CSLECTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = CSLECTFRandomV4.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                         subnet_mask=containers_config.internal_subnet_mask,
                                                                         hacker_ip=containers_config.agent_ip)
            defender_action_conf = CSLECTFRandomV4.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.internal_subnet_mask)
            env_config = CSLECTFRandomV4.env_config(containers_config=containers_config,
                                                    flags_config=flags_config,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config,
                                                    num_nodes=num_nodes - 1)
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.attacker_exploration_filter_illegal = True
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.attacker_filter_illegal_actions = False
            env_config.max_episode_length = 50
        super(CSLECTFRandomGeneratedSim4Env, self).__init__(env_config=env_config)


# -------- Version 4, Generated Simulation, With Costs------------
class CSLECTFRandomGeneratedSimWithCosts4Env(CSLECTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """

    def __init__(self, env_config: csleEnvConfig, emulation_config: EmulationConfig, checkpoint_dir: str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes: int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = CSLECTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = CSLECTFRandomV4.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                         subnet_mask=containers_config.internal_subnet_mask,
                                                                         hacker_ip=containers_config.agent_ip)
            defender_action_conf = CSLECTFRandomV4.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.internal_subnet_mask)
            env_config = CSLECTFRandomV4.env_config(containers_config=containers_config,
                                                    flags_config=flags_config,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config,
                                                    num_nodes=num_nodes - 1)
            env_config.attacker_cost_coefficient = 1
            env_config.attacker_alerts_coefficient = 1
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_filter_illegal = True
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.attacker_filter_illegal_actions = False
            env_config.max_episode_length = 50
            env_config.compute_pi_star_attacker = False
            env_config.use_upper_bound_pi_star_attacker = True
        super(CSLECTFRandomGeneratedSimWithCosts4Env, self).__init__(env_config=env_config)
