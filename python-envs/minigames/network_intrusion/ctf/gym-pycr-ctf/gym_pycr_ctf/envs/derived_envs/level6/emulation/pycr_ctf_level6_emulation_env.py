from gym_pycr_ctf.dao.network.env_mode import EnvMode
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.envs_model.config.level_6.pycr_ctf_level_6_base import PyCrCTFLevel6Base
from gym_pycr_ctf.envs_model.config.level_6.pycr_ctf_level_6_v1 import PyCrCTFLevel6V1
from gym_pycr_ctf.envs_model.config.level_6.pycr_ctf_level_6_v2 import PyCrCTFLevel6V2
from gym_pycr_ctf.envs_model.config.level_6.pycr_ctf_level_6_v3 import PyCrCTFLevel6V3
from gym_pycr_ctf.envs_model.config.level_6.pycr_ctf_level_6_v4 import PyCrCTFLevel6V4

# -------- Base Version (for testing) ------------
class PyCRCTFLevel6EmulationBaseEnv(PyCRCTFEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel6Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel6Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel6Base.router_ip()
            network_conf = PyCrCTFLevel6Base.network_conf()
            attacker_action_conf = PyCrCTFLevel6Base.attacker_all_actions_conf(num_nodes=PyCrCTFLevel6Base.num_nodes(),
                                                                      subnet_mask=PyCrCTFLevel6Base.subnet_mask(),
                                                                      hacker_ip=PyCrCTFLevel6Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel6Base.defender_all_actions_conf(
                num_nodes=PyCrCTFLevel6Base.num_nodes(), subnet_mask=PyCrCTFLevel6Base.subnet_mask())
            env_config = PyCrCTFLevel6Base.env_config(network_conf=network_conf,
                                                      attacker_action_conf=attacker_action_conf,
                                                      defender_action_conf=defender_action_conf,
                                                      emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 1 ------------

class PyCRCTFLevel6Emulation1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel6Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel6Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel6Base.router_ip()
            network_conf = PyCrCTFLevel6Base.network_conf()
            attacker_action_conf = PyCrCTFLevel6V1.attacker_actions_conf(num_nodes=PyCrCTFLevel6Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel6Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel6Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel6V1.defender_actions_conf(
                num_nodes=PyCrCTFLevel6Base.num_nodes(), subnet_mask=PyCrCTFLevel6Base.subnet_mask())
            env_config = PyCrCTFLevel6V1.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.attacker_filter_illegal_actions = False
            env_config.max_episode_length = 100
        super().__init__(env_config=env_config)


# -------- Version 1 with costs------------

class PyCRCTFLevel6EmulationWithCosts1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel6Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel6Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel6Base.router_ip()
            network_conf = PyCrCTFLevel6Base.network_conf()
            attacker_action_conf = PyCrCTFLevel6V1.attacker_actions_conf(num_nodes=PyCrCTFLevel6Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel6Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel6Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel6V1.defender_actions_conf(
                num_nodes=PyCrCTFLevel6Base.num_nodes(), subnet_mask=PyCrCTFLevel6Base.subnet_mask())
            env_config = PyCrCTFLevel6V1.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 ------------

class PyCRCTFLevel6Emulation2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel6Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel6Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel6Base.router_ip()
            network_conf = PyCrCTFLevel6Base.network_conf()
            attacker_action_conf = PyCrCTFLevel6V2.attacker_actions_conf(num_nodes=PyCrCTFLevel6Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel6Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel6Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel6V2.defender_actions_conf(
                num_nodes=PyCrCTFLevel6Base.num_nodes(), subnet_mask=PyCrCTFLevel6Base.subnet_mask())
            env_config = PyCrCTFLevel6V2.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 with costs------------

class PyCRCTFLevel6EmulationWithCosts2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel6Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel6Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel6Base.router_ip()
            network_conf = PyCrCTFLevel6Base.network_conf()
            attacker_action_conf = PyCrCTFLevel6V2.attacker_actions_conf(num_nodes=PyCrCTFLevel6Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel6Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel6Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel6V2.defender_actions_conf(
                num_nodes=PyCrCTFLevel6Base.num_nodes(), subnet_mask=PyCrCTFLevel6Base.subnet_mask())
            env_config = PyCrCTFLevel6V2.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 ------------

class PyCRCTFLevel6Emulation3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel6Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel6Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel6Base.router_ip()
            network_conf = PyCrCTFLevel6Base.network_conf()
            attacker_action_conf = PyCrCTFLevel6V3.attacker_actions_conf(num_nodes=PyCrCTFLevel6Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel6Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel6Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel6V3.defender_actions_conf(
                num_nodes=PyCrCTFLevel6Base.num_nodes(), subnet_mask=PyCrCTFLevel6Base.subnet_mask())
            env_config = PyCrCTFLevel6V3.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 with costs------------

class PyCRCTFLevel6EmulationWithCosts3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel6Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel6Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel6Base.router_ip()
            network_conf = PyCrCTFLevel6Base.network_conf()
            attacker_action_conf = PyCrCTFLevel6V3.attacker_actions_conf(num_nodes=PyCrCTFLevel6Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel6Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel6Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel6V3.defender_actions_conf(
                num_nodes=PyCrCTFLevel6Base.num_nodes(), subnet_mask=PyCrCTFLevel6Base.subnet_mask())
            env_config = PyCrCTFLevel6V3.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 ------------

class PyCRCTFLevel6Emulation4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel6Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel6Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel6Base.router_ip()
            network_conf = PyCrCTFLevel6Base.network_conf()
            attacker_action_conf = PyCrCTFLevel6V4.attacker_actions_conf(num_nodes=PyCrCTFLevel6Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel6Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel6Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel6V4.defender_actions_conf(
                num_nodes=PyCrCTFLevel6Base.num_nodes(), subnet_mask=PyCrCTFLevel6Base.subnet_mask())
            env_config = PyCrCTFLevel6V4.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 with costs------------

class PyCRCTFLevel6EmulationWithCosts4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel6Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel6Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel6Base.router_ip()
            network_conf = PyCrCTFLevel6Base.network_conf()
            attacker_action_conf = PyCrCTFLevel6V4.attacker_actions_conf(num_nodes=PyCrCTFLevel6Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel6Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel6Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel6V4.defender_actions_conf(
                num_nodes=PyCrCTFLevel6Base.num_nodes(), subnet_mask=PyCrCTFLevel6Base.subnet_mask())
            env_config = PyCrCTFLevel6V4.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)