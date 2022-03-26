from csle_common.dao.network.env_mode import EnvMode
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.logic.exploration.random_exploration_policy import RandomExplorationPolicy
from csle_common.dao.network.env_config import CSLEEnvConfig
from gym_csle_ctf.envs.csle_ctf_env import CSLECTFEnv
from gym_csle_ctf.envs_model.config.level_1.csle_ctf_level_1_base import CSLECTFLevel1Base
from gym_csle_ctf.envs_model.config.level_1.csle_ctf_level_1_v1 import CSLECTFLevel1V1
from gym_csle_ctf.envs_model.config.level_1.csle_ctf_level_1_v2 import CSLECTFLevel1V2
from gym_csle_ctf.envs_model.config.level_1.csle_ctf_level_1_v3 import CSLECTFLevel1V3
from gym_csle_ctf.envs_model.config.level_1.csle_ctf_level_1_v4 import CSLECTFLevel1V4


# -------- Version 1 ------------
class CSLECTFLevel1GeneratedSim1Env(CSLECTFEnv):
    """
    Generated Simulation.
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = CSLECTFLevel1Base.emulation_config()
            render_config = CSLECTFLevel1Base.render_conf()
            network_conf = CSLECTFLevel1Base.network_conf(generate=True)
            attacker_action_conf = CSLECTFLevel1V1.attacker_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel1Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel1Base.hacker_ip())
            defender_action_conf = CSLECTFLevel1V1.defender_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel1Base.subnet_mask())
            env_config = CSLECTFLevel1V1.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.defender_update_state = True
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.attacker_max_exploration_steps = 100
            env_config.attacker_max_exploration_trajectories = 10

        super(CSLECTFLevel1GeneratedSim1Env, self).__init__(env_config=env_config)


# -------- Version 1, costs ------------
class CSLECTFLevel1GeneratedSimWithCosts1Env(CSLECTFEnv):
    """
    Generated Simulation.
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = CSLECTFLevel1Base.emulation_config()
            render_config = CSLECTFLevel1Base.render_conf()
            network_conf = CSLECTFLevel1Base.network_conf(generate=True)
            attacker_action_conf = CSLECTFLevel1V1.attacker_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel1Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel1Base.hacker_ip())
            defender_action_conf = CSLECTFLevel1V1.defender_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel1Base.subnet_mask())
            env_config = CSLECTFLevel1V1.env_config(network_conf=network_conf,
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

class CSLECTFLevel1GeneratedSim2Env(CSLECTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel1Base.emulation_config()
            network_conf = CSLECTFLevel1Base.network_conf()
            attacker_action_conf = CSLECTFLevel1V2.attacker_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel1Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel1Base.hacker_ip())
            defender_action_conf = CSLECTFLevel1V2.defender_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel1Base.subnet_mask())
            env_config = CSLECTFLevel1V2.env_config(network_conf=network_conf,
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

class CSLECTFLevel1GeneratedSimWithCosts2Env(CSLECTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel1Base.emulation_config()
            network_conf = CSLECTFLevel1Base.network_conf()
            attacker_action_conf = CSLECTFLevel1V2.attacker_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel1Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel1Base.hacker_ip())
            defender_action_conf = CSLECTFLevel1V2.defender_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel1Base.subnet_mask())
            env_config = CSLECTFLevel1V2.env_config(network_conf=network_conf,
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

class CSLECTFLevel1GeneratedSim3Env(CSLECTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel1Base.emulation_config()
            network_conf = CSLECTFLevel1Base.network_conf()
            attacker_action_conf = CSLECTFLevel1V3.attacker_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel1Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel1Base.hacker_ip())
            defender_action_conf = CSLECTFLevel1V3.defender_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel1Base.subnet_mask())
            env_config = CSLECTFLevel1V3.env_config(network_conf=network_conf,
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

class CSLECTFLevel1GeneratedSimWithCosts3Env(CSLECTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel1Base.emulation_config()
            network_conf = CSLECTFLevel1Base.network_conf()
            attacker_action_conf = CSLECTFLevel1V3.attacker_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel1Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel1Base.hacker_ip())
            defender_action_conf = CSLECTFLevel1V3.defender_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel1Base.subnet_mask())
            env_config = CSLECTFLevel1V3.env_config(network_conf=network_conf,
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

class CSLECTFLevel1GeneratedSim4Env(CSLECTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel1Base.emulation_config()
            network_conf = CSLECTFLevel1Base.network_conf()
            attacker_action_conf = CSLECTFLevel1V4.attacker_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel1Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel1Base.hacker_ip())
            defender_action_conf = CSLECTFLevel1V4.defender_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel1Base.subnet_mask())
            env_config = CSLECTFLevel1V4.env_config(network_conf=network_conf,
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

class CSLECTFLevel1GeneratedSimWithCosts4Env(CSLECTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel1Base.emulation_config()
            network_conf = CSLECTFLevel1Base.network_conf()
            attacker_action_conf = CSLECTFLevel1V4.attacker_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel1Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel1Base.hacker_ip())
            defender_action_conf = CSLECTFLevel1V4.defender_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel1Base.subnet_mask())
            env_config = CSLECTFLevel1V4.env_config(network_conf=network_conf,
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
