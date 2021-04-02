from gym_pycr_ctf.dao.network.env_mode import EnvMode
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.envs_model.config.level_5.pycr_ctf_level_5_base import PyCrCTFLevel5Base
from gym_pycr_ctf.envs_model.config.level_5.pycr_ctf_level_5_v1 import PyCrCTFLevel5V1
from gym_pycr_ctf.envs_model.config.level_5.pycr_ctf_level_5_v2 import PyCrCTFLevel5V2
from gym_pycr_ctf.envs_model.config.level_5.pycr_ctf_level_5_v3 import PyCrCTFLevel5V3
from gym_pycr_ctf.envs_model.config.level_5.pycr_ctf_level_5_v4 import PyCrCTFLevel5V4


# -------- Base Version (for testing) ------------
class PyCRCTFLevel5EmulationBaseEnv(PyCRCTFEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel5Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel5Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel5Base.router_ip()
            network_conf = PyCrCTFLevel5Base.network_conf()
            attacker_action_conf = PyCrCTFLevel5Base.attacker_all_actions_conf(num_nodes=PyCrCTFLevel5Base.num_nodes(),
                                                                      subnet_mask=PyCrCTFLevel5Base.subnet_mask(),
                                                                      hacker_ip=PyCrCTFLevel5Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel5Base.defender_all_actions_conf(
                num_nodes=PyCrCTFLevel5Base.num_nodes(), subnet_mask=PyCrCTFLevel5Base.subnet_mask())
            env_config = PyCrCTFLevel5Base.env_config(network_conf=network_conf,
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


# -------- Version 1 ------------

class PyCRCTFLevel5Emulation1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel5Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel5Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel5Base.router_ip()
            network_conf = PyCrCTFLevel5Base.network_conf()
            attacker_action_conf = PyCrCTFLevel5V1.attacker_actions_conf(num_nodes=PyCrCTFLevel5Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel5Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel5Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel5V1.defender_actions_conf(
                num_nodes=PyCrCTFLevel5Base.num_nodes(), subnet_mask=PyCrCTFLevel5Base.subnet_mask())
            env_config = PyCrCTFLevel5V1.env_config(network_conf=network_conf,
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


# -------- Version 1 with costs------------

class PyCRCTFLevel5EmulationWithCosts1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel5Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel5Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel5Base.router_ip()
            network_conf = PyCrCTFLevel5Base.network_conf()
            attacker_action_conf = PyCrCTFLevel5V1.attacker_actions_conf(num_nodes=PyCrCTFLevel5Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel5Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel5Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel5V1.defender_actions_conf(
                num_nodes=PyCrCTFLevel5Base.num_nodes(), subnet_mask=PyCrCTFLevel5Base.subnet_mask())
            env_config = PyCrCTFLevel5V1.env_config(network_conf=network_conf,
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

class PyCRCTFLevel5Emulation2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel5Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel5Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel5Base.router_ip()
            network_conf = PyCrCTFLevel5Base.network_conf()
            attacker_action_conf = PyCrCTFLevel5V2.attacker_actions_conf(num_nodes=PyCrCTFLevel5Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel5Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel5Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel5V2.defender_actions_conf(
                num_nodes=PyCrCTFLevel5Base.num_nodes(), subnet_mask=PyCrCTFLevel5Base.subnet_mask())
            env_config = PyCrCTFLevel5V2.env_config(network_conf=network_conf,
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

class PyCRCTFLevel5EmulationWithCosts2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel5Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel5Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel5Base.router_ip()
            network_conf = PyCrCTFLevel5Base.network_conf()
            attacker_action_conf = PyCrCTFLevel5V2.attacker_actions_conf(num_nodes=PyCrCTFLevel5Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel5Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel5Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel5V2.defender_actions_conf(
                num_nodes=PyCrCTFLevel5Base.num_nodes(), subnet_mask=PyCrCTFLevel5Base.subnet_mask())
            env_config = PyCrCTFLevel5V2.env_config(network_conf=network_conf,
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

class PyCRCTFLevel5Emulation3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel5Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel5Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel5Base.router_ip()
            network_conf = PyCrCTFLevel5Base.network_conf()
            attacker_action_conf = PyCrCTFLevel5V3.attacker_actions_conf(num_nodes=PyCrCTFLevel5Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel5Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel5Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel5V3.defender_actions_conf(
                num_nodes=PyCrCTFLevel5Base.num_nodes(), subnet_mask=PyCrCTFLevel5Base.subnet_mask())
            env_config = PyCrCTFLevel5V3.env_config(network_conf=network_conf,
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

class PyCRCTFLevel5EmulationWithCosts3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel5Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel5Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel5Base.router_ip()
            network_conf = PyCrCTFLevel5Base.network_conf()
            attacker_action_conf = PyCrCTFLevel5V3.attacker_actions_conf(num_nodes=PyCrCTFLevel5Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel5Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel5Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel5V3.defender_actions_conf(
                num_nodes=PyCrCTFLevel5Base.num_nodes(), subnet_mask=PyCrCTFLevel5Base.subnet_mask())
            env_config = PyCrCTFLevel5V3.env_config(network_conf=network_conf,
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

class PyCRCTFLevel5Emulation4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel5Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel5Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel5Base.router_ip()
            network_conf = PyCrCTFLevel5Base.network_conf()
            attacker_action_conf = PyCrCTFLevel5V4.attacker_actions_conf(num_nodes=PyCrCTFLevel5Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel5Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel5Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel5V4.defender_actions_conf(
                num_nodes=PyCrCTFLevel5Base.num_nodes(), subnet_mask=PyCrCTFLevel5Base.subnet_mask())
            env_config = PyCrCTFLevel5V4.env_config(network_conf=network_conf,
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

class PyCRCTFLevel5EmulationWithCosts4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel5Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel5Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel5Base.router_ip()
            network_conf = PyCrCTFLevel5Base.network_conf()
            action_conf = PyCrCTFLevel5V4.attacker_actions_conf(num_nodes=PyCrCTFLevel5Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel5Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel5Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel5V4.defender_actions_conf(
                num_nodes=PyCrCTFLevel5Base.num_nodes(), subnet_mask=PyCrCTFLevel5Base.subnet_mask())
            env_config = PyCrCTFLevel5V4.env_config(network_conf=network_conf,
                                                    attacker_action_conf=action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)