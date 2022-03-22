from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.dao.network.env_mode import EnvMode
from gym_csle_ctf.dao.network.env_config import CSLEEnvConfig
from gym_csle_ctf.envs.csle_ctf_env import CSLECTFEnv
from gym_csle_ctf.envs_model.config.level_9.csle_ctf_level_9_base import CSLECTFLevel9Base
from gym_csle_ctf.envs_model.config.level_9.csle_ctf_level_9_v1 import CSLECTFLevel9V1
from gym_csle_ctf.envs_model.config.level_9.csle_ctf_level_9_v2 import CSLECTFLevel9V2
from gym_csle_ctf.envs_model.config.level_9.csle_ctf_level_9_v3 import CSLECTFLevel9V3
from gym_csle_ctf.envs_model.config.level_9.csle_ctf_level_9_v4 import CSLECTFLevel9V4
from gym_csle_ctf.envs_model.config.level_9.csle_ctf_level_9_v5 import CSLECTFLevel9V5
from gym_csle_ctf.envs_model.config.level_9.csle_ctf_level_9_v6 import CSLECTFLevel9V6


# -------- Base Version (for testing) ------------
class CSLECTFLevel9EmulationBaseEnv(CSLECTFEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel9Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel9Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel9Base.router_ip()
            network_conf = CSLECTFLevel9Base.network_conf()
            attacker_action_conf = CSLECTFLevel9Base.attacker_all_actions_conf(num_nodes=CSLECTFLevel9Base.num_nodes(),
                                                                      subnet_mask=CSLECTFLevel9Base.subnet_mask(),
                                                                      hacker_ip=CSLECTFLevel9Base.hacker_ip())
            defender_action_conf = CSLECTFLevel9Base.defender_all_actions_conf(
                num_nodes=CSLECTFLevel9Base.num_nodes(), subnet_mask=CSLECTFLevel9Base.subnet_mask())
            env_config = CSLECTFLevel9Base.env_config(network_conf=network_conf,
                                                      attacker_action_conf=attacker_action_conf,
                                                      defender_action_conf=defender_action_conf,
                                                      emulation_config=emulation_config, render_conf=render_config)
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.simulate_detection = False
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
        super(CSLECTFLevel9EmulationBaseEnv, self).__init__(env_config=env_config)


# -------- Version 1 ------------
class CSLECTFLevel9Emulation1Env(CSLECTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel9Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel9Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel9Base.router_ip()
            network_conf = CSLECTFLevel9Base.network_conf()
            attacker_action_conf = CSLECTFLevel9V1.attacker_actions_conf(num_nodes=CSLECTFLevel9Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel9Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel9Base.hacker_ip())
            defender_action_conf = CSLECTFLevel9V1.defender_actions_conf(
                num_nodes=CSLECTFLevel9Base.num_nodes(), subnet_mask=CSLECTFLevel9Base.subnet_mask())
            env_config = CSLECTFLevel9V1.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.simulate_detection = False
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
            env_config.randomize_attacker_starting_state = False
        super(CSLECTFLevel9Emulation1Env, self).__init__(env_config=env_config)


# -------- Version 1 with costs------------

class CSLECTFLevel9EmulationWithCosts1Env(CSLECTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel9Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel9Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel9Base.router_ip()
            network_conf = CSLECTFLevel9Base.network_conf()
            attacker_action_conf = CSLECTFLevel9V1.attacker_actions_conf(num_nodes=CSLECTFLevel9Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel9Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel9Base.hacker_ip())
            defender_action_conf = CSLECTFLevel9V1.defender_actions_conf(
                num_nodes=CSLECTFLevel9Base.num_nodes(), subnet_mask=CSLECTFLevel9Base.subnet_mask())
            env_config = CSLECTFLevel9V1.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 ------------

class CSLECTFLevel9Emulation2Env(CSLECTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel9Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel9Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel9Base.router_ip()
            network_conf = CSLECTFLevel9Base.network_conf()
            attacker_action_conf = CSLECTFLevel9V2.attacker_actions_conf(num_nodes=CSLECTFLevel9Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel9Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel9Base.hacker_ip())
            defender_action_conf = CSLECTFLevel9V2.defender_actions_conf(
                num_nodes=CSLECTFLevel9Base.num_nodes(), subnet_mask=CSLECTFLevel9Base.subnet_mask())
            env_config = CSLECTFLevel9V2.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 with costs------------

class CSLECTFLevel9EmulationWithCosts2Env(CSLECTFEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel9Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel9Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel9Base.router_ip()
            network_conf = CSLECTFLevel9Base.network_conf()
            attacker_action_conf = CSLECTFLevel9V2.attacker_actions_conf(num_nodes=CSLECTFLevel9Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel9Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel9Base.hacker_ip())
            defender_action_conf = CSLECTFLevel9V2.defender_actions_conf(
                num_nodes=CSLECTFLevel9Base.num_nodes(), subnet_mask=CSLECTFLevel9Base.subnet_mask())
            env_config = CSLECTFLevel9V2.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 ------------

class CSLECTFLevel9Emulation3Env(CSLECTFEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel9Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel9Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel9Base.router_ip()
            network_conf = CSLECTFLevel9Base.network_conf()
            attacker_action_conf = CSLECTFLevel9V3.attacker_actions_conf(num_nodes=CSLECTFLevel9Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel9Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel9Base.hacker_ip())
            defender_action_conf = CSLECTFLevel9V3.defender_actions_conf(
                num_nodes=CSLECTFLevel9Base.num_nodes(), subnet_mask=CSLECTFLevel9Base.subnet_mask())
            env_config = CSLECTFLevel9V3.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 with costs------------

class CSLECTFLevel9EmulationWithCosts3Env(CSLECTFEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel9Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel9Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel9Base.router_ip()
            network_conf = CSLECTFLevel9Base.network_conf()
            attacker_action_conf = CSLECTFLevel9V3.attacker_actions_conf(num_nodes=CSLECTFLevel9Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel9Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel9Base.hacker_ip())
            defender_action_conf = CSLECTFLevel9V3.defender_actions_conf(
                num_nodes=CSLECTFLevel9Base.num_nodes(), subnet_mask=CSLECTFLevel9Base.subnet_mask())
            env_config = CSLECTFLevel9V3.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 ------------

class CSLECTFLevel9Emulation4Env(CSLECTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel9Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel9Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel9Base.router_ip()
            network_conf = CSLECTFLevel9Base.network_conf()
            attacker_action_conf = CSLECTFLevel9V4.attacker_actions_conf(num_nodes=CSLECTFLevel9Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel9Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel9Base.hacker_ip())
            defender_action_conf = CSLECTFLevel9V4.defender_actions_conf(
                num_nodes=CSLECTFLevel9Base.num_nodes(), subnet_mask=CSLECTFLevel9Base.subnet_mask())
            env_config = CSLECTFLevel9V4.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 with costs------------

class CSLECTFLevel9EmulationWithCosts4Env(CSLECTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel9Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel9Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel9Base.router_ip()
            network_conf = CSLECTFLevel9Base.network_conf()
            attacker_action_conf = CSLECTFLevel9V4.attacker_actions_conf(num_nodes=CSLECTFLevel9Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel9Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel9Base.hacker_ip())
            defender_action_conf = CSLECTFLevel9V4.defender_actions_conf(
                num_nodes=CSLECTFLevel9Base.num_nodes(), subnet_mask=CSLECTFLevel9Base.subnet_mask())
            env_config = CSLECTFLevel9V4.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 5 ------------

class CSLECTFLevel9Emulation5Env(CSLECTFEnv):
    """
    An extension of V1 but allows the attacker to peform "no-op" actions and is intended for playing with defender agent.
    Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel9Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel9Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel9Base.router_ip()
            network_conf = CSLECTFLevel9Base.network_conf()
            attacker_action_conf = CSLECTFLevel9V5.attacker_actions_conf(num_nodes=CSLECTFLevel9Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel9Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel9Base.hacker_ip())
            defender_action_conf = CSLECTFLevel9V5.defender_actions_conf(
                num_nodes=CSLECTFLevel9Base.num_nodes(), subnet_mask=CSLECTFLevel9Base.subnet_mask())
            env_config = CSLECTFLevel9V5.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.domain_randomization = False
            env_config.attacker_max_exploration_steps = 500
            env_config.attacker_max_exploration_trajectories = 10
            env_config.max_episode_length = 100
            env_config.attacker_alerts_coefficient = 0
            env_config.attacker_cost_coefficient = 0
            env_config.attacker_base_step_reward = -1
            env_config.use_upper_bound_pi_star_attacker = False
            env_config.detection_alerts_threshold = 10
            env_config.detection_prob_factor = 0.05
            env_config.randomize_attacker_starting_state = False

            env_config.explore_defense_states = True
            env_config.defender_update_state = True
            env_config.attacker_continue_action_sleep = 0.001
            env_config.defender_sleep_before_state_update = 10
            env_config.attacker_illegal_reward_action = -100

            env_config.defender_caught_attacker_reward = 100
            env_config.defender_early_stopping_reward = -100
            env_config.defender_intrusion_reward = -100
            env_config.attacker_early_stopping_reward = -100

            env_config.snort_critical_baseline_threshold = 400
            env_config.emulate_detection = False
            env_config.simulate_detection = False
            env_config.use_attacker_action_stats_to_update_defender_state = True

        super().__init__(env_config=env_config)


# -------- Version 6 ------------

class CSLECTFLevel9Emulation6Env(CSLECTFEnv):
    """
    An extension of V5 which allows the defender to take multiple stop actions
    """

    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir: str):
        if env_config is None:
            render_config = CSLECTFLevel9Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel9Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel9Base.router_ip()
            network_conf = CSLECTFLevel9Base.network_conf()
            attacker_action_conf = CSLECTFLevel9V6.attacker_actions_conf(num_nodes=CSLECTFLevel9Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel9Base.subnet_mask(),
                                                                         hacker_ip=CSLECTFLevel9Base.hacker_ip())
            defender_action_conf = CSLECTFLevel9V6.defender_actions_conf(
                num_nodes=CSLECTFLevel9Base.num_nodes(), subnet_mask=CSLECTFLevel9Base.subnet_mask())
            env_config = CSLECTFLevel9V6.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.domain_randomization = False
            env_config.attacker_max_exploration_steps = 500
            env_config.attacker_max_exploration_trajectories = 10
            env_config.max_episode_length = 100
            env_config.attacker_alerts_coefficient = 0
            env_config.attacker_cost_coefficient = 0
            env_config.attacker_base_step_reward = -1
            env_config.use_upper_bound_pi_star_attacker = False
            env_config.detection_alerts_threshold = 10
            env_config.detection_prob_factor = 0.05
            env_config.randomize_attacker_starting_state = False

            env_config.explore_defense_states = True
            env_config.defender_update_state = True
            env_config.attacker_continue_action_sleep = 0.001
            env_config.defender_sleep_before_state_update = 10
            env_config.attacker_illegal_reward_action = -100

            env_config.defender_caught_attacker_reward = 100
            env_config.defender_early_stopping_reward = -100
            env_config.defender_intrusion_reward = -100
            env_config.attacker_early_stopping_reward = -100

            env_config.snort_critical_baseline_threshold = 400
            env_config.emulate_detection = False
            env_config.simulate_detection = False
            env_config.use_attacker_action_stats_to_update_defender_state = True

        super().__init__(env_config=env_config)