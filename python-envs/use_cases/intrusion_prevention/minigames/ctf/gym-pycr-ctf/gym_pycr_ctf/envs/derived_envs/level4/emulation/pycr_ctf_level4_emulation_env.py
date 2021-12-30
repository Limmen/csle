from pycr_common.dao.network.env_mode import EnvMode
from pycr_common.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.dao.network.env_config import PyCREnvConfig
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.envs_model.config.level_4.pycr_ctf_level_4_base import PyCrCTFLevel4Base
from gym_pycr_ctf.envs_model.config.level_4.pycr_ctf_level_4_v1 import PyCrCTFLevel4V1
from gym_pycr_ctf.envs_model.config.level_4.pycr_ctf_level_4_v2 import PyCrCTFLevel4V2
from gym_pycr_ctf.envs_model.config.level_4.pycr_ctf_level_4_v3 import PyCrCTFLevel4V3
from gym_pycr_ctf.envs_model.config.level_4.pycr_ctf_level_4_v4 import PyCrCTFLevel4V4
from gym_pycr_ctf.envs_model.config.level_4.pycr_ctf_level_4_v5 import PyCrCTFLevel4V5


# -------- Base Version (for testing) ------------
class PyCRCTFLevel4EmulationBaseEnv(PyCRCTFEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: PyCREnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel4Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel4Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel4Base.router_ip()
            network_conf = PyCrCTFLevel4Base.network_conf()
            attacker_action_conf = PyCrCTFLevel4Base.attacker_all_actions_conf(num_nodes=PyCrCTFLevel4Base.num_nodes(),
                                                                      subnet_mask=PyCrCTFLevel4Base.subnet_mask(),
                                                                      hacker_ip=PyCrCTFLevel4Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel4Base.defender_all_actions_conf(
                num_nodes=PyCrCTFLevel4Base.num_nodes(), subnet_mask=PyCrCTFLevel4Base.subnet_mask())
            env_config = PyCrCTFLevel4Base.env_config(network_conf=network_conf,
                                                      attacker_action_conf=attacker_action_conf,
                                                      defender_action_conf=defender_action_conf,
                                                      emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super(PyCRCTFLevel4EmulationBaseEnv, self).__init__(env_config=env_config)


# -------- Version 1 ------------
class PyCRCTFLevel4Emulation1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: PyCREnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel4Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel4Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel4Base.router_ip()
            network_conf = PyCrCTFLevel4Base.network_conf()
            attacker_action_conf = PyCrCTFLevel4V1.attacker_actions_conf(num_nodes=PyCrCTFLevel4Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel4Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel4Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel4V1.defender_actions_conf(
                num_nodes=PyCrCTFLevel4Base.num_nodes(), subnet_mask=PyCrCTFLevel4Base.subnet_mask())
            env_config = PyCrCTFLevel4V1.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.defender_update_state = False
        super(PyCRCTFLevel4Emulation1Env, self).__init__(env_config=env_config)


# -------- Version 1 with costs------------

class PyCRCTFLevel4EmulationWithCosts1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: PyCREnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel4Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel4Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel4Base.router_ip()
            network_conf = PyCrCTFLevel4Base.network_conf()
            attacker_action_conf = PyCrCTFLevel4V1.attacker_actions_conf(num_nodes=PyCrCTFLevel4Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel4Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel4Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel4V1.defender_actions_conf(
                num_nodes=PyCrCTFLevel4Base.num_nodes(), subnet_mask=PyCrCTFLevel4Base.subnet_mask())
            env_config = PyCrCTFLevel4V1.env_config(network_conf=network_conf,
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

class PyCRCTFLevel4Emulation2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: PyCREnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
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
            defender_action_conf = PyCrCTFLevel4V2.defender_actions_conf(
                num_nodes=PyCrCTFLevel4Base.num_nodes(), subnet_mask=PyCrCTFLevel4Base.subnet_mask())
            env_config = PyCrCTFLevel4V2.env_config(network_conf=network_conf,
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

class PyCRCTFLevel4EmulationWithCosts2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: PyCREnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
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
            defender_action_conf = PyCrCTFLevel4V2.defender_actions_conf(
                num_nodes=PyCrCTFLevel4Base.num_nodes(), subnet_mask=PyCrCTFLevel4Base.subnet_mask())
            env_config = PyCrCTFLevel4V2.env_config(network_conf=network_conf,
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

class PyCRCTFLevel4Emulation3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: PyCREnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
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
            defender_action_conf = PyCrCTFLevel4V3.defender_actions_conf(
                num_nodes=PyCrCTFLevel4Base.num_nodes(), subnet_mask=PyCrCTFLevel4Base.subnet_mask())
            env_config = PyCrCTFLevel4V3.env_config(network_conf=network_conf,
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

class PyCRCTFLevel4EmulationWithCosts3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: PyCREnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
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
            defender_action_conf = PyCrCTFLevel4V3.defender_actions_conf(
                num_nodes=PyCrCTFLevel4Base.num_nodes(), subnet_mask=PyCrCTFLevel4Base.subnet_mask())
            env_config = PyCrCTFLevel4V3.env_config(network_conf=network_conf,
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

class PyCRCTFLevel4Emulation4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: PyCREnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
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
            defender_action_conf = PyCrCTFLevel4V4.defender_actions_conf(
                num_nodes=PyCrCTFLevel4Base.num_nodes(), subnet_mask=PyCrCTFLevel4Base.subnet_mask())
            env_config = PyCrCTFLevel4V4.env_config(network_conf=network_conf,
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

class PyCRCTFLevel4EmulationWithCosts4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: PyCREnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
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
            defender_action_conf = PyCrCTFLevel4V4.defender_actions_conf(
                num_nodes=PyCrCTFLevel4Base.num_nodes(), subnet_mask=PyCrCTFLevel4Base.subnet_mask())
            env_config = PyCrCTFLevel4V4.env_config(network_conf=network_conf,
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

class PyCRCTFLevel4Emulation5Env(PyCRCTFEnv):
    """
    An extension of V1 but allows the attacker to peform "no-op" actions and is intended for playing with defender agent.
    Does not take action costs into account.
    """
    def __init__(self, env_config: PyCREnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel4Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel4Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel4Base.router_ip()
            network_conf = PyCrCTFLevel4Base.network_conf()
            attacker_action_conf = PyCrCTFLevel4V5.attacker_actions_conf(num_nodes=PyCrCTFLevel4Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel4Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel4Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel4V5.defender_actions_conf(
                num_nodes=PyCrCTFLevel4Base.num_nodes(), subnet_mask=PyCrCTFLevel4Base.subnet_mask())
            env_config = PyCrCTFLevel4V5.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
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
        super().__init__(env_config=env_config)