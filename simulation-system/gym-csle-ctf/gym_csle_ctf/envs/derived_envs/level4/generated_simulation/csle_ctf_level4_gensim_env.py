from csle_common.dao.network.env_mode import EnvMode
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.logic.exploration.random_exploration_policy import RandomExplorationPolicy
from csle_common.dao.network.env_config import CSLEEnvConfig
from gym_csle_ctf.envs.csle_ctf_env import CSLECTFEnv
from gym_csle_ctf.envs_model.config.level_4.csle_ctf_level_4_base import CSLECTFLevel4Base
from gym_csle_ctf.envs_model.config.level_4.csle_ctf_level_4_v1 import CSLECTFLevel4V1
from gym_csle_ctf.envs_model.config.level_4.csle_ctf_level_4_v2 import CSLECTFLevel4V2
from gym_csle_ctf.envs_model.config.level_4.csle_ctf_level_4_v3 import CSLECTFLevel4V3
from gym_csle_ctf.envs_model.config.level_4.csle_ctf_level_4_v4 import CSLECTFLevel4V4
from gym_csle_ctf.envs_model.config.level_4.csle_ctf_level_4_v5 import CSLECTFLevel4V5


# -------- Version 1 ------------
class CSLECTFLevel4GeneratedSim1Env(CSLECTFEnv):
    """
    Generated Simulation.
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = CSLECTFLevel4Base.emulation_config()
            render_config = CSLECTFLevel4Base.render_conf()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel4Base.router_ip()
            network_conf = CSLECTFLevel4Base.network_conf(generate=True)
            attacker_action_conf = CSLECTFLevel4V1.attacker_actions_conf(num_nodes=CSLECTFLevel4Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel4Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel4Base.hacker_ip())
            defender_action_conf = CSLECTFLevel4V1.defender_actions_conf(num_nodes=CSLECTFLevel4Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel4Base.subnet_mask())
            env_config = CSLECTFLevel4V1.env_config(network_conf=network_conf,
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

        super(CSLECTFLevel4GeneratedSim1Env, self).__init__(env_config=env_config)


# -------- Version 1, costs ------------
class CSLECTFLevel4GeneratedSimWithCosts1Env(CSLECTFEnv):
    """
    Generated Simulation.
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = CSLECTFLevel4Base.emulation_config()
            render_config = CSLECTFLevel4Base.render_conf()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel4Base.router_ip()
            network_conf = CSLECTFLevel4Base.network_conf(generate=True)
            attacker_action_conf = CSLECTFLevel4V1.attacker_actions_conf(num_nodes=CSLECTFLevel4Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel4Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel4Base.hacker_ip())
            defender_action_conf = CSLECTFLevel4V1.defender_actions_conf(num_nodes=CSLECTFLevel4Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel4Base.subnet_mask())
            env_config = CSLECTFLevel4V1.env_config(network_conf=network_conf,
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

        super(CSLECTFLevel4GeneratedSimWithCosts1Env, self).__init__(env_config=env_config)


# -------- Version 2 ------------
class CSLECTFLevel4GeneratedSim2Env(CSLECTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel4Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel4Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel4Base.router_ip()
            network_conf = CSLECTFLevel4Base.network_conf()
            attacker_action_conf = CSLECTFLevel4V2.attacker_actions_conf(num_nodes=CSLECTFLevel4Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel4Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel4Base.hacker_ip())
            defender_action_conf = CSLECTFLevel4V2.defender_actions_conf(num_nodes=CSLECTFLevel4Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel4Base.subnet_mask())
            env_config = CSLECTFLevel4V2.env_config(network_conf=network_conf,
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
        super(CSLECTFLevel4GeneratedSim2Env, self).__init__(env_config=env_config)


# -------- Version 2, costs ------------
class CSLECTFLevel4GeneratedSimWithCosts2Env(CSLECTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel4Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel4Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel4Base.router_ip()
            network_conf = CSLECTFLevel4Base.network_conf()
            attacker_action_conf = CSLECTFLevel4V2.attacker_actions_conf(num_nodes=CSLECTFLevel4Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel4Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel4Base.hacker_ip())
            defender_action_conf = CSLECTFLevel4V2.defender_actions_conf(num_nodes=CSLECTFLevel4Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel4Base.subnet_mask())
            env_config = CSLECTFLevel4V2.env_config(network_conf=network_conf,
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
        super(CSLECTFLevel4GeneratedSimWithCosts2Env, self).__init__(env_config=env_config)


# -------- Version 3 ------------
class CSLECTFLevel4GeneratedSim3Env(CSLECTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel4Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel4Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel4Base.router_ip()
            network_conf = CSLECTFLevel4Base.network_conf()
            attacker_action_conf = CSLECTFLevel4V3.attacker_actions_conf(num_nodes=CSLECTFLevel4Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel4Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel4Base.hacker_ip())
            defender_action_conf = CSLECTFLevel4V3.defender_actions_conf(num_nodes=CSLECTFLevel4Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel4Base.subnet_mask())
            env_config = CSLECTFLevel4V3.env_config(network_conf=network_conf,
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
        super(CSLECTFLevel4GeneratedSim3Env, self).__init__(env_config=env_config)


# -------- Version 3, costs ------------
class CSLECTFLevel4GeneratedSimWithCosts3Env(CSLECTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel4Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel4Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel4Base.router_ip()
            network_conf = CSLECTFLevel4Base.network_conf()
            attacker_action_conf = CSLECTFLevel4V3.attacker_actions_conf(num_nodes=CSLECTFLevel4Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel4Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel4Base.hacker_ip())
            defender_action_conf = CSLECTFLevel4V3.defender_actions_conf(num_nodes=CSLECTFLevel4Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel4Base.subnet_mask())
            env_config = CSLECTFLevel4V3.env_config(network_conf=network_conf,
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
        super(CSLECTFLevel4GeneratedSimWithCosts3Env, self).__init__(env_config=env_config)


# -------- Version 4 ------------
class CSLECTFLevel4GeneratedSim4Env(CSLECTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel4Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel4Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel4Base.router_ip()
            network_conf = CSLECTFLevel4Base.network_conf()
            attacker_action_conf = CSLECTFLevel4V4.attacker_actions_conf(num_nodes=CSLECTFLevel4Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel4Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel4Base.hacker_ip())
            defender_action_conf = CSLECTFLevel4V4.defender_actions_conf(num_nodes=CSLECTFLevel4Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel4Base.subnet_mask())
            env_config = CSLECTFLevel4V4.env_config(network_conf=network_conf,
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
        super(CSLECTFLevel4GeneratedSim4Env, self).__init__(env_config=env_config)


# -------- Version 4 ------------
class CSLECTFLevel4GeneratedSimWithCosts4Env(CSLECTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel4Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel4Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel4Base.router_ip()
            network_conf = CSLECTFLevel4Base.network_conf()
            attacker_action_conf = CSLECTFLevel4V4.attacker_actions_conf(num_nodes=CSLECTFLevel4Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel4Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel4Base.hacker_ip())
            defender_action_conf = CSLECTFLevel4V4.defender_actions_conf(num_nodes=CSLECTFLevel4Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel4Base.subnet_mask())
            env_config = CSLECTFLevel4V4.env_config(network_conf=network_conf,
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
        super(CSLECTFLevel4GeneratedSimWithCosts4Env, self).__init__(env_config=env_config)


# -------- Version 5 ------------
class CSLECTFLevel4GeneratedSim5Env(CSLECTFEnv):
    """
    Generated Simulation.
    An extension to V1 to allow the attacker to take the "continue" action.
    Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = CSLECTFLevel4Base.emulation_config()
            render_config = CSLECTFLevel4Base.render_conf()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel4Base.router_ip()
            network_conf = CSLECTFLevel4Base.network_conf(generate=True)
            attacker_action_conf = CSLECTFLevel4V5.attacker_actions_conf(num_nodes=CSLECTFLevel4Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel4Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel4Base.hacker_ip())
            defender_action_conf = CSLECTFLevel4V5.defender_actions_conf(num_nodes=CSLECTFLevel4Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel4Base.subnet_mask())
            env_config = CSLECTFLevel4V5.env_config(network_conf=network_conf,
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
            env_config.attacker_max_exploration_steps = 200
            env_config.attacker_max_exploration_trajectories = 50000
            env_config.explore_defense_states = True
            env_config.defender_update_state = True
            env_config.attacker_continue_action_sleep = 0.001
            env_config.defender_sleep_before_state_update = 10
            # env_config.attacker_continue_action_sleep = 0.0001
            # env_config.defender_sleep_before_state_update = 0.0001
            env_config.max_episode_length = 500
            env_config.defender_caught_attacker_reward = 10
            env_config.defender_early_stopping_reward = -1
            env_config.defender_intrusion_reward = -1
            env_config.stop_after_failed_detection = False
        super(CSLECTFLevel4GeneratedSim5Env, self).__init__(env_config=env_config)
