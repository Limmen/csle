from gym_pycr_ctf.dao.network.env_mode import EnvMode
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.envs_model.config.level_9.pycr_ctf_level_9_base import PyCrCTFLevel9Base
from gym_pycr_ctf.envs_model.config.level_9.pycr_ctf_level_9_v1 import PyCrCTFLevel9V1
from gym_pycr_ctf.envs_model.config.level_9.pycr_ctf_level_9_v2 import PyCrCTFLevel9V2
from gym_pycr_ctf.envs_model.config.level_9.pycr_ctf_level_9_v3 import PyCrCTFLevel9V3
from gym_pycr_ctf.envs_model.config.level_9.pycr_ctf_level_9_v4 import PyCrCTFLevel9V4
from gym_pycr_ctf.envs_model.config.level_9.pycr_ctf_level_9_v5 import PyCrCTFLevel9V5
from gym_pycr_ctf.envs_model.logic.exploration.random_exploration_policy import RandomExplorationPolicy
from gym_pycr_ctf.envs_model.logic.exploration.custom_exploration_policy import CustomExplorationPolicy


# -------- Version 1 ------------
class PyCRCTFLevel9GeneratedSim1Env(PyCRCTFEnv):
    """
    Generated Simulation.
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = PyCrCTFLevel9Base.emulation_config()
            render_config = PyCrCTFLevel9Base.render_conf()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel9Base.router_ip()
            network_conf = PyCrCTFLevel9Base.network_conf(generate=True)
            attacker_action_conf = PyCrCTFLevel9V1.attacker_actions_conf(num_nodes=PyCrCTFLevel9Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel9Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel9Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel9V1.defender_actions_conf(num_nodes=PyCrCTFLevel9Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel9Base.subnet_mask())
            env_config = PyCrCTFLevel9V1.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
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
            env_config.detection_alerts_threshold = 10
            env_config.emulate_detection = True
            env_config.detection_prob_factor = 0.05

            env_config.randomize_attacker_starting_state = True
            env_config.randomize_starting_state_policy = CustomExplorationPolicy(
                num_actions=env_config.attacker_action_conf.num_actions,
                strategy=[100,33,104,105,106,1,104,105,106,70,104,105,107,100,165,104,105,106,200,104,105,106,58,104,
                          105,331,105,100,266,104,105,106,100,113,104,105])
            env_config.randomize_state_min_steps = 0
            env_config.randomize_state_max_steps = len(env_config.randomize_starting_state_policy.strategy) - 1
            env_config.randomize_state_steps_list = None
            #env_config.randomize_state_steps_list = [30, 30, 30, 30, 30, 30, 30, 30]
            #env_config.randomize_state_steps_list = [0,0,0,0,0,0,5, 9, 13, 17, 20, 25, 30, 30, 30, 30, 30, 30, 30, 30]

        super().__init__(env_config=env_config)


# -------- Version 1, costs ------------
class PyCRCTFLevel9GeneratedSimWithCosts1Env(PyCRCTFEnv):
    """
    Generated Simulation.
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = PyCrCTFLevel9Base.emulation_config()
            render_config = PyCrCTFLevel9Base.render_conf()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel9Base.router_ip()
            network_conf = PyCrCTFLevel9Base.network_conf(generate=True)
            attacker_action_conf = PyCrCTFLevel9V1.attacker_actions_conf(num_nodes=PyCrCTFLevel9Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel9Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel9Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel9V1.defender_actions_conf(num_nodes=PyCrCTFLevel9Base.num_nodes(),
                                                                         subnet_mask=PyCrCTFLevel9Base.subnet_mask())
            env_config = PyCrCTFLevel9V1.env_config(network_conf=network_conf,
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

class PyCRCTFLevel9GeneratedSim2Env(PyCRCTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel9Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel9Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel9Base.router_ip()
            network_conf = PyCrCTFLevel9Base.network_conf()
            attacker_action_conf = PyCrCTFLevel9V2.attacker_actions_conf(num_nodes=PyCrCTFLevel9Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel9Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel9Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel9V2.defender_actions_conf(num_nodes=PyCrCTFLevel9Base.num_nodes(),
                                                                         subnet_mask=PyCrCTFLevel9Base.subnet_mask())
            env_config = PyCrCTFLevel9V2.env_config(network_conf=network_conf,
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


class PyCRCTFLevel9GeneratedSimWithCosts2Env(PyCRCTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel9Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel9Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel9Base.router_ip()
            network_conf = PyCrCTFLevel9Base.network_conf()
            attacker_action_conf = PyCrCTFLevel9V2.attacker_actions_conf(num_nodes=PyCrCTFLevel9Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel9Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel9Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel9V2.defender_actions_conf(num_nodes=PyCrCTFLevel9Base.num_nodes(),
                                                                         subnet_mask=PyCrCTFLevel9Base.subnet_mask())
            env_config = PyCrCTFLevel9V2.env_config(network_conf=network_conf,
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

class PyCRCTFLevel9GeneratedSim3Env(PyCRCTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel9Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel9Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel9Base.router_ip()
            network_conf = PyCrCTFLevel9Base.network_conf()
            attacker_action_conf = PyCrCTFLevel9V3.attacker_actions_conf(num_nodes=PyCrCTFLevel9Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel9Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel9Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel9V3.defender_actions_conf(num_nodes=PyCrCTFLevel9Base.num_nodes(),
                                                                         subnet_mask=PyCrCTFLevel9Base.subnet_mask())
            env_config = PyCrCTFLevel9V3.env_config(network_conf=network_conf,
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

class PyCRCTFLevel9GeneratedSimWithCosts3Env(PyCRCTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel9Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel9Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel9Base.router_ip()
            network_conf = PyCrCTFLevel9Base.network_conf()
            attacker_action_conf = PyCrCTFLevel9V3.attacker_actions_conf(num_nodes=PyCrCTFLevel9Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel9Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel9Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel9V3.defender_actions_conf(num_nodes=PyCrCTFLevel9Base.num_nodes(),
                                                                         subnet_mask=PyCrCTFLevel9Base.subnet_mask())
            env_config = PyCrCTFLevel9V3.env_config(network_conf=network_conf,
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

class PyCRCTFLevel9GeneratedSim4Env(PyCRCTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel9Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel9Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel9Base.router_ip()
            network_conf = PyCrCTFLevel9Base.network_conf()
            attacker_action_conf = PyCrCTFLevel9V4.attacker_actions_conf(num_nodes=PyCrCTFLevel9Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel9Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel9Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel9V4.defender_actions_conf(num_nodes=PyCrCTFLevel9Base.num_nodes(),
                                                                         subnet_mask=PyCrCTFLevel9Base.subnet_mask())
            env_config = PyCrCTFLevel9V4.env_config(network_conf=network_conf,
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
            env_config.attacker_max_exploration_steps = 500
            env_config.attacker_max_exploration_trajectories = 10
        super().__init__(env_config=env_config)

# -------- Version 4 ------------


class PyCRCTFLevel9GeneratedSimWithCosts4Env(PyCRCTFEnv):
    """
    Generated simulation.
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel9Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel9Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel9Base.router_ip()
            network_conf = PyCrCTFLevel9Base.network_conf()
            attacker_action_conf = PyCrCTFLevel9V4.attacker_actions_conf(num_nodes=PyCrCTFLevel9Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel9Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel9Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel9V4.defender_actions_conf(num_nodes=PyCrCTFLevel9Base.num_nodes(),
                                                                         subnet_mask=PyCrCTFLevel9Base.subnet_mask())
            env_config = PyCrCTFLevel9V4.env_config(network_conf=network_conf,
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

class PyCRCTFLevel9GeneratedSim5Env(PyCRCTFEnv):
    """
    Generated Simulation.

    An extension of V1 but allows the attacker to peform "no-op" actions and is intended for playing with defender agent.
    Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            if emulation_config is None:
                emulation_config = PyCrCTFLevel9Base.emulation_config()
            render_config = PyCrCTFLevel9Base.render_conf()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel9Base.router_ip()
            network_conf = PyCrCTFLevel9Base.network_conf(generate=True)
            attacker_action_conf = PyCrCTFLevel9V5.attacker_actions_conf(num_nodes=PyCrCTFLevel9Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel9Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel9Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel9V5.defender_actions_conf(num_nodes=PyCrCTFLevel9Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel9Base.subnet_mask())
            env_config = PyCrCTFLevel9V5.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            # exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            # env_config.attacker_exploration_policy = exp_policy
            env_config.attacker_exploration_policy = CustomExplorationPolicy(
                num_actions=env_config.attacker_action_conf.num_actions,
                strategy=[372, 100, 372, 33, 372, 104, 372, 105, 372, 106, 372, 1, 372, 104, 372, 372, 372, 105, 372,
                          106, 372, 70, 372, 104, 105, 107, 372, 100, 372, 165, 372, 104, 372, 105, 372, 106, 372,
                          200, 372, 372, 104, 372, 105, 372, 106, 372, 372, 58, 372, 104, 372, 105, 372, 331, 372,
                          105, 100, 266, 372, 104, 105, 106, 100, 372, 113, 104, 372, 105])
            env_config.domain_randomization = False
            env_config.attacker_max_exploration_steps = 500
            env_config.attacker_max_exploration_trajectories = 500
            env_config.max_episode_length = 1000
            env_config.attacker_alerts_coefficient = 0
            env_config.attacker_cost_coefficient = 0
            env_config.attacker_base_step_reward = -1
            env_config.use_upper_bound_pi_star_attacker = False
            env_config.detection_alerts_threshold = 10
            env_config.emulate_detection = False
            env_config.detection_prob_factor = 0.05
            env_config.randomize_attacker_starting_state = False

            env_config.explore_defense_states = True
            env_config.defender_update_state = True
            env_config.attacker_continue_action_sleep = 30
            env_config.defender_sleep_before_state_update = 15

        super().__init__(env_config=env_config)
