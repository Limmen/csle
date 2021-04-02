from gym_pycr_ctf.dao.network.env_mode import EnvMode
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.envs_model.config.level_4.pycr_ctf_level_4_base import PyCrCTFLevel4Base
from gym_pycr_ctf.envs_model.config.level_4.pycr_ctf_level_4_v1 import PyCrCTFLevel4V1
from gym_pycr_ctf.envs_model.config.level_4.pycr_ctf_level_4_v2 import PyCrCTFLevel4V2
from gym_pycr_ctf.envs_model.config.level_4.pycr_ctf_level_4_v3 import PyCrCTFLevel4V3
from gym_pycr_ctf.envs_model.config.level_4.pycr_ctf_level_4_v4 import PyCrCTFLevel4V4
from gym_pycr_ctf.envs_model.config.level_4.pycr_ctf_level_4_v5 import PyCrCTFLevel4V5
from gym_pycr_ctf.envs_model.logic.exploration.random_exploration_policy import RandomExplorationPolicy

# -------- Version 1 ------------
class PyCRCTFLevel4GeneratedSim1Env(PyCRCTFEnv):
    """
    Generated Simulation.
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = PyCrCTFLevel4Base.emulation_config()
            render_config = PyCrCTFLevel4Base.render_conf()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel4Base.router_ip()
            network_conf = PyCrCTFLevel4Base.network_conf(generate=True)
            attacker_action_conf = PyCrCTFLevel4V1.attacker_actions_conf(num_nodes=PyCrCTFLevel4Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel4Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel4Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel4V1.defender_actions_conf(num_nodes=PyCrCTFLevel4Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel4Base.subnet_mask())
            env_config = PyCrCTFLevel4V1.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.attacker_max_exploration_steps = 100
            env_config.attacker_max_exploration_trajectories = 10

        super().__init__(env_config=env_config)


# -------- Version 1, costs ------------
class PyCRCTFLevel4GeneratedSimWithCosts1Env(PyCRCTFEnv):
    """
    Generated Simulation.
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = PyCrCTFLevel4Base.emulation_config()
            render_config = PyCrCTFLevel4Base.render_conf()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel4Base.router_ip()
            network_conf = PyCrCTFLevel4Base.network_conf(generate=True)
            attacker_action_conf = PyCrCTFLevel4V1.attacker_actions_conf(num_nodes=PyCrCTFLevel4Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel4Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel4Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel4V1.defender_actions_conf(num_nodes=PyCrCTFLevel4Base.num_nodes(),
                                                                         subnet_mask=PyCrCTFLevel4Base.subnet_mask())
            env_config = PyCrCTFLevel4V1.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.attacker_max_exploration_steps = 100
            env_config.attacker_max_exploration_trajectories = 10

        super().__init__(env_config=env_config)


# -------- Version 2 ------------

class PyCRCTFLevel4GeneratedSim2Env(PyCRCTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel4Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel4Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel4Base.router_ip()
            network_conf = PyCrCTFLevel4Base.network_conf()
            attacker_action_conf = PyCrCTFLevel4V2.attacker_actions_conf(num_nodes=PyCrCTFLevel4Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel4Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel4Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel4V2.defender_actions_conf(num_nodes=PyCrCTFLevel4Base.num_nodes(),
                                                                         subnet_mask=PyCrCTFLevel4Base.subnet_mask())
            env_config = PyCrCTFLevel4V2.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.attacker_max_exploration_steps = 100
            env_config.attacker_max_exploration_trajectories = 10
        super().__init__(env_config=env_config)

# -------- Version 2, costs ------------

class PyCRCTFLevel4GeneratedSimWithCosts2Env(PyCRCTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel4Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel4Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel4Base.router_ip()
            network_conf = PyCrCTFLevel4Base.network_conf()
            attacker_action_conf = PyCrCTFLevel4V2.attacker_actions_conf(num_nodes=PyCrCTFLevel4Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel4Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel4Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel4V2.defender_actions_conf(num_nodes=PyCrCTFLevel4Base.num_nodes(),
                                                                         subnet_mask=PyCrCTFLevel4Base.subnet_mask())
            env_config = PyCrCTFLevel4V2.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.attacker_max_exploration_steps = 100
            env_config.attacker_max_exploration_trajectories = 10
        super().__init__(env_config=env_config)

# -------- Version 3 ------------

class PyCRCTFLevel4GeneratedSim3Env(PyCRCTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel4Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel4Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel4Base.router_ip()
            network_conf = PyCrCTFLevel4Base.network_conf()
            attacker_action_conf = PyCrCTFLevel4V3.attacker_actions_conf(num_nodes=PyCrCTFLevel4Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel4Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel4Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel4V3.defender_actions_conf(num_nodes=PyCrCTFLevel4Base.num_nodes(),
                                                                         subnet_mask=PyCrCTFLevel4Base.subnet_mask())
            env_config = PyCrCTFLevel4V3.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.attacker_max_exploration_steps = 100
            env_config.attacker_max_exploration_trajectories = 10
        super().__init__(env_config=env_config)

# -------- Version 3, costs ------------

class PyCRCTFLevel4GeneratedSimWithCosts3Env(PyCRCTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel4Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel4Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel4Base.router_ip()
            network_conf = PyCrCTFLevel4Base.network_conf()
            attacker_action_conf = PyCrCTFLevel4V3.attacker_actions_conf(num_nodes=PyCrCTFLevel4Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel4Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel4Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel4V3.defender_actions_conf(num_nodes=PyCrCTFLevel4Base.num_nodes(),
                                                                         subnet_mask=PyCrCTFLevel4Base.subnet_mask())
            env_config = PyCrCTFLevel4V3.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.attacker_max_exploration_steps = 100
            env_config.attacker_max_exploration_trajectories = 10
        super().__init__(env_config=env_config)


# -------- Version 4 ------------

class PyCRCTFLevel4GeneratedSim4Env(PyCRCTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel4Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel4Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel4Base.router_ip()
            network_conf = PyCrCTFLevel4Base.network_conf()
            attacker_action_conf = PyCrCTFLevel4V4.attacker_actions_conf(num_nodes=PyCrCTFLevel4Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel4Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel4Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel4V4.defender_actions_conf(num_nodes=PyCrCTFLevel4Base.num_nodes(),
                                                                         subnet_mask=PyCrCTFLevel4Base.subnet_mask())
            env_config = PyCrCTFLevel4V4.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.attacker_max_exploration_steps = 100
            env_config.attacker_max_exploration_trajectories = 10
        super().__init__(env_config=env_config)

# -------- Version 4 ------------


class PyCRCTFLevel4GeneratedSimWithCosts4Env(PyCRCTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel4Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel4Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel4Base.router_ip()
            network_conf = PyCrCTFLevel4Base.network_conf()
            attacker_action_conf = PyCrCTFLevel4V4.attacker_actions_conf(num_nodes=PyCrCTFLevel4Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel4Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel4Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel4V4.defender_actions_conf(num_nodes=PyCrCTFLevel4Base.num_nodes(),
                                                                         subnet_mask=PyCrCTFLevel4Base.subnet_mask())
            env_config = PyCrCTFLevel4V4.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.attacker_max_exploration_steps = 100
            env_config.attacker_max_exploration_trajectories = 10
        super().__init__(env_config=env_config)


# -------- Version 5 ------------

class PyCRCTFLevel4GeneratedSim5Env(PyCRCTFEnv):
    """
    Generated Simulation.
    An extension to V1 to allow the attacker to take the "continue" action.
    Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = PyCrCTFLevel4Base.emulation_config()
            render_config = PyCrCTFLevel4Base.render_conf()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel4Base.router_ip()
            network_conf = PyCrCTFLevel4Base.network_conf(generate=True)
            attacker_action_conf = PyCrCTFLevel4V5.attacker_actions_conf(num_nodes=PyCrCTFLevel4Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel4Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel4Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel4V5.defender_actions_conf(num_nodes=PyCrCTFLevel4Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel4Base.subnet_mask())
            env_config = PyCrCTFLevel4V5.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.attacker_max_exploration_steps = 100
            env_config.attacker_max_exploration_trajectories = 50
            env_config.explore_defense_states = True
            env_config.defender_update_state = True
            env_config.attacker_continue_action_sleep = 30
            env_config.defender_sleep_before_state_update = 15
        super().__init__(env_config=env_config)
