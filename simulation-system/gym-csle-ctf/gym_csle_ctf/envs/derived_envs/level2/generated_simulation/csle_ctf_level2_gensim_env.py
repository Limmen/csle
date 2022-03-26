from csle_common.dao.network.env_mode import EnvMode
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.logic.exploration.random_exploration_policy import RandomExplorationPolicy
from csle_common.dao.network.env_config import CSLEEnvConfig
from gym_csle_ctf.envs.csle_ctf_env import CSLECTFEnv
from gym_csle_ctf.envs_model.config.level_2.csle_ctf_level_2_base import CSLECTFLevel2Base
from gym_csle_ctf.envs_model.config.level_2.csle_ctf_level_2_v1 import CSLECTFLevel2V1
from gym_csle_ctf.envs_model.config.level_2.csle_ctf_level_2_v2 import CSLECTFLevel2V2
from gym_csle_ctf.envs_model.config.level_2.csle_ctf_level_2_v3 import CSLECTFLevel2V3
from gym_csle_ctf.envs_model.config.level_2.csle_ctf_level_2_v4 import CSLECTFLevel2V4


# -------- Version 1 ------------
class CSLECTFLevel2GeneratedSim1Env(CSLECTFEnv):
    """
    Generated Simulation
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = CSLECTFLevel2Base.emulation_config()
            render_config = CSLECTFLevel2Base.render_conf()
            network_conf = CSLECTFLevel2Base.network_conf(generate=True)
            attacker_action_conf = CSLECTFLevel2V1.attacker_actions_conf(num_nodes=CSLECTFLevel2Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel2Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel2Base.hacker_ip())
            defender_action_conf = CSLECTFLevel2V1.defender_actions_conf(
                num_nodes=CSLECTFLevel2Base.num_nodes(), subnet_mask=CSLECTFLevel2Base.subnet_mask())
            env_config = CSLECTFLevel2V1.env_config(network_conf=network_conf,
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

        super(CSLECTFLevel2GeneratedSim1Env, self).__init__(env_config=env_config)


# -------- Version 1, Costs ------------
class CSLECTFLevel2GeneratedSimWithCosts1Env(CSLECTFEnv):
    """
    Generated Simulation.
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = CSLECTFLevel2Base.emulation_config()
            render_config = CSLECTFLevel2Base.render_conf()
            network_conf = CSLECTFLevel2Base.network_conf(generate=True)
            attacker_action_conf = CSLECTFLevel2V1.attacker_actions_conf(num_nodes=CSLECTFLevel2Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel2Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel2Base.hacker_ip())
            defender_action_conf = CSLECTFLevel2V1.defender_actions_conf(
                num_nodes=CSLECTFLevel2Base.num_nodes(), subnet_mask=CSLECTFLevel2Base.subnet_mask())
            env_config = CSLECTFLevel2V1.env_config(network_conf=network_conf,
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

        super(CSLECTFLevel2GeneratedSimWithCosts1Env, self).__init__(env_config=env_config)


# -------- Version 2 ------------
class CSLECTFLevel2GeneratedSim2Env(CSLECTFEnv):
    """
    Generated Simulation.
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = CSLECTFLevel2Base.emulation_config()
            render_config = CSLECTFLevel2Base.render_conf()
            network_conf = CSLECTFLevel2Base.network_conf(generate=True)
            attacker_action_conf = CSLECTFLevel2V2.attacker_actions_conf(num_nodes=CSLECTFLevel2Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel2Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel2Base.hacker_ip())
            defender_action_conf = CSLECTFLevel2V2.defender_actions_conf(
                num_nodes=CSLECTFLevel2Base.num_nodes(), subnet_mask=CSLECTFLevel2Base.subnet_mask())
            env_config = CSLECTFLevel2V2.env_config(network_conf=network_conf,
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

        super(CSLECTFLevel2GeneratedSim2Env, self).__init__(env_config=env_config)


# -------- Version 2, Costs ------------
class CSLECTFLevel2GeneratedSimWithCosts2Env(CSLECTFEnv):
    """
    Generated Simulation.
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = CSLECTFLevel2Base.emulation_config()
            render_config = CSLECTFLevel2Base.render_conf()
            network_conf = CSLECTFLevel2Base.network_conf(generate=True)
            attacker_action_conf = CSLECTFLevel2V2.attacker_actions_conf(num_nodes=CSLECTFLevel2Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel2Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel2Base.hacker_ip())
            defender_action_conf = CSLECTFLevel2V2.defender_actions_conf(
                num_nodes=CSLECTFLevel2Base.num_nodes(), subnet_mask=CSLECTFLevel2Base.subnet_mask())
            env_config = CSLECTFLevel2V2.env_config(network_conf=network_conf,
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

        super(CSLECTFLevel2GeneratedSimWithCosts2Env, self).__init__(env_config=env_config)


# -------- Version 3 ------------
class CSLECTFLevel2GeneratedSim3Env(CSLECTFEnv):
    """
    Generated Simulation.
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = CSLECTFLevel2Base.emulation_config()
            render_config = CSLECTFLevel2Base.render_conf()
            network_conf = CSLECTFLevel2Base.network_conf(generate=True)
            attacker_action_conf = CSLECTFLevel2V3.attacker_actions_conf(num_nodes=CSLECTFLevel2Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel2Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel2Base.hacker_ip())
            defender_action_conf = CSLECTFLevel2V3.defender_actions_conf(
                num_nodes=CSLECTFLevel2Base.num_nodes(), subnet_mask=CSLECTFLevel2Base.subnet_mask())
            env_config = CSLECTFLevel2V3.env_config(network_conf=network_conf,
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

        super(CSLECTFLevel2GeneratedSim3Env, self).__init__(env_config=env_config)


# -------- Version 3, Costs ------------
class CSLECTFLevel2GeneratedSimWithCosts3Env(CSLECTFEnv):
    """
    Generated Simulation.
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = CSLECTFLevel2Base.emulation_config()
            render_config = CSLECTFLevel2Base.render_conf()
            network_conf = CSLECTFLevel2Base.network_conf(generate=True)
            attacker_action_conf = CSLECTFLevel2V3.attacker_actions_conf(num_nodes=CSLECTFLevel2Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel2Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel2Base.hacker_ip())
            defender_action_conf = CSLECTFLevel2V3.defender_actions_conf(
                num_nodes=CSLECTFLevel2Base.num_nodes(), subnet_mask=CSLECTFLevel2Base.subnet_mask())
            env_config = CSLECTFLevel2V3.env_config(network_conf=network_conf,
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

        super(CSLECTFLevel2GeneratedSimWithCosts3Env, self).__init__(env_config=env_config)


# -------- Version 4 ------------
class CSLECTFLevel2GeneratedSim4Env(CSLECTFEnv):
    """
    Generated Simulation.
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = CSLECTFLevel2Base.emulation_config()
            render_config = CSLECTFLevel2Base.render_conf()
            network_conf = CSLECTFLevel2Base.network_conf(generate=True)
            attacker_action_conf = CSLECTFLevel2V4.attacker_actions_conf(num_nodes=CSLECTFLevel2Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel2Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel2Base.hacker_ip())
            defender_action_conf = CSLECTFLevel2V4.defender_actions_conf(
                num_nodes=CSLECTFLevel2Base.num_nodes(), subnet_mask=CSLECTFLevel2Base.subnet_mask())
            env_config = CSLECTFLevel2V4.env_config(network_conf=network_conf,
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

        super(CSLECTFLevel2GeneratedSim4Env, self).__init__(env_config=env_config)


# -------- Version 4 ------------
class CSLECTFLevel2GeneratedSimWithCosts4Env(CSLECTFEnv):
    """
    Generated Simulation.
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = CSLECTFLevel2Base.emulation_config()
            render_config = CSLECTFLevel2Base.render_conf()
            network_conf = CSLECTFLevel2Base.network_conf(generate=True)
            attacker_action_conf = CSLECTFLevel2V4.attacker_actions_conf(num_nodes=CSLECTFLevel2Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel2Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel2Base.hacker_ip())
            defender_action_conf = CSLECTFLevel2V4.defender_actions_conf(
                num_nodes=CSLECTFLevel2Base.num_nodes(), subnet_mask=CSLECTFLevel2Base.subnet_mask())
            env_config = CSLECTFLevel2V4.env_config(network_conf=network_conf,
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

        super(CSLECTFLevel2GeneratedSimWithCosts4Env, self).__init__(env_config=env_config)