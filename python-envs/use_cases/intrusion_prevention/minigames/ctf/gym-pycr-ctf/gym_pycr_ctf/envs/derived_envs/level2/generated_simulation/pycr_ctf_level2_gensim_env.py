from pycr_common.dao.network.env_mode import EnvMode
from pycr_common.dao.network.emulation_config import EmulationConfig
from pycr_common.envs_model.logic.exploration.random_exploration_policy import RandomExplorationPolicy
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.envs_model.config.level_2.pycr_ctf_level_2_base import PyCrCTFLevel2Base
from gym_pycr_ctf.envs_model.config.level_2.pycr_ctf_level_2_v1 import PyCrCTFLevel2V1
from gym_pycr_ctf.envs_model.config.level_2.pycr_ctf_level_2_v2 import PyCrCTFLevel2V2
from gym_pycr_ctf.envs_model.config.level_2.pycr_ctf_level_2_v3 import PyCrCTFLevel2V3
from gym_pycr_ctf.envs_model.config.level_2.pycr_ctf_level_2_v4 import PyCrCTFLevel2V4


# -------- Version 1 ------------
class PyCRCTFLevel2GeneratedSim1Env(PyCRCTFEnv):
    """
    Generated Simulation
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = PyCrCTFLevel2Base.emulation_config()
            render_config = PyCrCTFLevel2Base.render_conf()
            network_conf = PyCrCTFLevel2Base.network_conf(generate=True)
            attacker_action_conf = PyCrCTFLevel2V1.attacker_actions_conf(num_nodes=PyCrCTFLevel2Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel2Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel2Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel2V1.defender_actions_conf(
                num_nodes=PyCrCTFLevel2Base.num_nodes(), subnet_mask=PyCrCTFLevel2Base.subnet_mask())
            env_config = PyCrCTFLevel2V1.env_config(network_conf=network_conf,
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

        super(PyCRCTFLevel2GeneratedSim1Env, self).__init__(env_config=env_config)


# -------- Version 1, Costs ------------
class PyCRCTFLevel2GeneratedSimWithCosts1Env(PyCRCTFEnv):
    """
    Generated Simulation.
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = PyCrCTFLevel2Base.emulation_config()
            render_config = PyCrCTFLevel2Base.render_conf()
            network_conf = PyCrCTFLevel2Base.network_conf(generate=True)
            attacker_action_conf = PyCrCTFLevel2V1.attacker_actions_conf(num_nodes=PyCrCTFLevel2Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel2Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel2Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel2V1.defender_actions_conf(
                num_nodes=PyCrCTFLevel2Base.num_nodes(), subnet_mask=PyCrCTFLevel2Base.subnet_mask())
            env_config = PyCrCTFLevel2V1.env_config(network_conf=network_conf,
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

        super(PyCRCTFLevel2GeneratedSimWithCosts1Env, self).__init__(env_config=env_config)


# -------- Version 2 ------------
class PyCRCTFLevel2GeneratedSim2Env(PyCRCTFEnv):
    """
    Generated Simulation.
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = PyCrCTFLevel2Base.emulation_config()
            render_config = PyCrCTFLevel2Base.render_conf()
            network_conf = PyCrCTFLevel2Base.network_conf(generate=True)
            attacker_action_conf = PyCrCTFLevel2V2.attacker_actions_conf(num_nodes=PyCrCTFLevel2Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel2Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel2Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel2V2.defender_actions_conf(
                num_nodes=PyCrCTFLevel2Base.num_nodes(), subnet_mask=PyCrCTFLevel2Base.subnet_mask())
            env_config = PyCrCTFLevel2V2.env_config(network_conf=network_conf,
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

        super(PyCRCTFLevel2GeneratedSim2Env, self).__init__(env_config=env_config)


# -------- Version 2, Costs ------------
class PyCRCTFLevel2GeneratedSimWithCosts2Env(PyCRCTFEnv):
    """
    Generated Simulation.
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = PyCrCTFLevel2Base.emulation_config()
            render_config = PyCrCTFLevel2Base.render_conf()
            network_conf = PyCrCTFLevel2Base.network_conf(generate=True)
            attacker_action_conf = PyCrCTFLevel2V2.attacker_actions_conf(num_nodes=PyCrCTFLevel2Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel2Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel2Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel2V2.defender_actions_conf(
                num_nodes=PyCrCTFLevel2Base.num_nodes(), subnet_mask=PyCrCTFLevel2Base.subnet_mask())
            env_config = PyCrCTFLevel2V2.env_config(network_conf=network_conf,
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

        super(PyCRCTFLevel2GeneratedSimWithCosts2Env, self).__init__(env_config=env_config)


# -------- Version 3 ------------
class PyCRCTFLevel2GeneratedSim3Env(PyCRCTFEnv):
    """
    Generated Simulation.
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = PyCrCTFLevel2Base.emulation_config()
            render_config = PyCrCTFLevel2Base.render_conf()
            network_conf = PyCrCTFLevel2Base.network_conf(generate=True)
            attacker_action_conf = PyCrCTFLevel2V3.attacker_actions_conf(num_nodes=PyCrCTFLevel2Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel2Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel2Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel2V3.defender_actions_conf(
                num_nodes=PyCrCTFLevel2Base.num_nodes(), subnet_mask=PyCrCTFLevel2Base.subnet_mask())
            env_config = PyCrCTFLevel2V3.env_config(network_conf=network_conf,
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

        super(PyCRCTFLevel2GeneratedSim3Env, self).__init__(env_config=env_config)


# -------- Version 3, Costs ------------
class PyCRCTFLevel2GeneratedSimWithCosts3Env(PyCRCTFEnv):
    """
    Generated Simulation.
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = PyCrCTFLevel2Base.emulation_config()
            render_config = PyCrCTFLevel2Base.render_conf()
            network_conf = PyCrCTFLevel2Base.network_conf(generate=True)
            attacker_action_conf = PyCrCTFLevel2V3.attacker_actions_conf(num_nodes=PyCrCTFLevel2Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel2Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel2Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel2V3.defender_actions_conf(
                num_nodes=PyCrCTFLevel2Base.num_nodes(), subnet_mask=PyCrCTFLevel2Base.subnet_mask())
            env_config = PyCrCTFLevel2V3.env_config(network_conf=network_conf,
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

        super(PyCRCTFLevel2GeneratedSimWithCosts3Env, self).__init__(env_config=env_config)


# -------- Version 4 ------------
class PyCRCTFLevel2GeneratedSim4Env(PyCRCTFEnv):
    """
    Generated Simulation.
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = PyCrCTFLevel2Base.emulation_config()
            render_config = PyCrCTFLevel2Base.render_conf()
            network_conf = PyCrCTFLevel2Base.network_conf(generate=True)
            attacker_action_conf = PyCrCTFLevel2V4.attacker_actions_conf(num_nodes=PyCrCTFLevel2Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel2Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel2Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel2V4.defender_actions_conf(
                num_nodes=PyCrCTFLevel2Base.num_nodes(), subnet_mask=PyCrCTFLevel2Base.subnet_mask())
            env_config = PyCrCTFLevel2V4.env_config(network_conf=network_conf,
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

        super(PyCRCTFLevel2GeneratedSim4Env, self).__init__(env_config=env_config)


# -------- Version 4 ------------
class PyCRCTFLevel2GeneratedSimWithCosts4Env(PyCRCTFEnv):
    """
    Generated Simulation.
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = PyCrCTFLevel2Base.emulation_config()
            render_config = PyCrCTFLevel2Base.render_conf()
            network_conf = PyCrCTFLevel2Base.network_conf(generate=True)
            attacker_action_conf = PyCrCTFLevel2V4.attacker_actions_conf(num_nodes=PyCrCTFLevel2Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel2Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel2Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel2V4.defender_actions_conf(
                num_nodes=PyCrCTFLevel2Base.num_nodes(), subnet_mask=PyCrCTFLevel2Base.subnet_mask())
            env_config = PyCrCTFLevel2V4.env_config(network_conf=network_conf,
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

        super(PyCRCTFLevel2GeneratedSimWithCosts4Env, self).__init__(env_config=env_config)