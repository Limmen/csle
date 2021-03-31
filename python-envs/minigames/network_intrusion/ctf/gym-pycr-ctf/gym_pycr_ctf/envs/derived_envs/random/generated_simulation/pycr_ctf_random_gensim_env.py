from gym_pycr_ctf.dao.network.env_mode import EnvMode
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.dao.container_config.containers_config import ContainersConfig
from gym_pycr_ctf.dao.container_config.flags_config import FlagsConfig
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.envs.config.random.pycr_ctf_random_base import PyCrCTFRandomBase
from gym_pycr_ctf.envs.config.random.pycr_ctf_random_v1 import PyCrCTFRandomV1
from gym_pycr_ctf.envs.config.random.pycr_ctf_random_v2 import PyCrCTFRandomV2
from gym_pycr_ctf.envs.config.random.pycr_ctf_random_v3 import PyCrCTFRandomV3
from gym_pycr_ctf.envs.config.random.pycr_ctf_random_v4 import PyCrCTFRandomV4
from gym_pycr_ctf.envs.logic.exploration.random_exploration_policy import RandomExplorationPolicy

# -------- Version 1 Generated Sim ------------
class PyCRCTFRandomGeneratedSim1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
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
                num_nodes=num_nodes - 1, subnet_mask=containers_config.subnet_mask)
            env_config = PyCrCTFRandomV1.env_config(containers_config=containers_config,
                                                    flags_config=flags_config,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config,
                                                    num_nodes=num_nodes-1)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.attacker_filter_illegal_actions = False
            env_config.max_episode_length = 50
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.attacker_exploration_filter_illegal = True
        super().__init__(env_config=env_config)

# -------- Version 1 Generated Sim With Costs ------------

class PyCRCTFRandomGeneratedSimWithCosts1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
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
                num_nodes=num_nodes - 1, subnet_mask=containers_config.subnet_mask)
            env_config = PyCrCTFRandomV1.env_config(containers_config=containers_config,
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
        super().__init__(env_config=env_config)


# -------- Version 2 Generated Sim ------------
class PyCRCTFRandomGeneratedSim2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = PyCrCTFRandomV2.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                subnet_mask=containers_config.subnet_mask,
                                                                hacker_ip=containers_config.agent_ip)
            defender_action_conf = PyCrCTFRandomV2.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.subnet_mask)
            env_config = PyCrCTFRandomV2.env_config(containers_config=containers_config,
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
        super().__init__(env_config=env_config)

# -------- Version 2 Generated Sim With Costs ------------

class PyCRCTFRandomGeneratedSimWithCosts2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = PyCrCTFRandomV2.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                subnet_mask=containers_config.subnet_mask,
                                                                hacker_ip=containers_config.agent_ip)
            defender_action_conf = PyCrCTFRandomV2.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.subnet_mask)
            env_config = PyCrCTFRandomV2.env_config(containers_config=containers_config,
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
        super().__init__(env_config=env_config)


# -------- Version 3, Generated Simulation ------------
class PyCRCTFRandomGeneratedSim3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = PyCrCTFRandomV3.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                subnet_mask=containers_config.subnet_mask,
                                                                hacker_ip=containers_config.agent_ip)
            defender_action_conf = PyCrCTFRandomV3.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.subnet_mask)
            env_config = PyCrCTFRandomV3.env_config(containers_config=containers_config,
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
        super().__init__(env_config=env_config)

# -------- Version 3, Generated Simulation With Costs ------------
class PyCRCTFRandomGeneratedSimWithCosts3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = PyCrCTFRandomV3.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                subnet_mask=containers_config.subnet_mask,
                                                                hacker_ip=containers_config.agent_ip)
            defender_action_conf = PyCrCTFRandomV3.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.subnet_mask)
            env_config = PyCrCTFRandomV3.env_config(containers_config=containers_config,
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
        super().__init__(env_config=env_config)


# -------- Version 4, Generated Simulation ------------
class PyCRCTFRandomGeneratedSim4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """

    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir: str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes: int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = PyCrCTFRandomV4.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                subnet_mask=containers_config.subnet_mask,
                                                                hacker_ip=containers_config.agent_ip)
            defender_action_conf = PyCrCTFRandomV4.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.subnet_mask)
            env_config = PyCrCTFRandomV4.env_config(containers_config=containers_config,
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
        super().__init__(env_config=env_config)

# -------- Version 4, Generated Simulation, With Costs------------
class PyCRCTFRandomGeneratedSimWithCosts4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """

    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir: str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes: int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = PyCrCTFRandomV4.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                subnet_mask=containers_config.subnet_mask,
                                                                hacker_ip=containers_config.agent_ip)
            defender_action_conf = PyCrCTFRandomV4.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.subnet_mask)
            env_config = PyCrCTFRandomV4.env_config(containers_config=containers_config,
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
        super().__init__(env_config=env_config)
