from pycr_common.dao.network.env_mode import EnvMode
from pycr_common.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.envs_model.config.level_10.pycr_ctf_level_10_base import PyCrCTFLevel10Base
from gym_pycr_ctf.envs_model.config.level_10.pycr_ctf_level_10_v1 import PyCrCTFLevel10V1
from gym_pycr_ctf.envs_model.config.level_10.pycr_ctf_level_10_v2 import PyCrCTFLevel10V2
from gym_pycr_ctf.envs_model.config.level_10.pycr_ctf_level_10_v3 import PyCrCTFLevel10V3
from gym_pycr_ctf.envs_model.config.level_10.pycr_ctf_level_10_v4 import PyCrCTFLevel10V4


# -------- Base Version (for testing) ------------
class PyCRCTFLevel10EmulationBaseEnv(PyCRCTFEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel10Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel10Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel10Base.router_ip()
            network_conf = PyCrCTFLevel10Base.network_conf()
            attacker_action_conf = PyCrCTFLevel10Base.attacker_all_actions_conf(num_nodes=PyCrCTFLevel10Base.num_nodes(),
                                                                      subnet_mask=PyCrCTFLevel10Base.subnet_mask(),
                                                                      hacker_ip=PyCrCTFLevel10Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel10Base.defender_all_actions_conf(
                num_nodes=PyCrCTFLevel10Base.num_nodes(), subnet_mask=PyCrCTFLevel10Base.subnet_mask())
            env_config = PyCrCTFLevel10Base.env_config(network_conf=network_conf,
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
class PyCRCTFLevel10Emulation1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel10Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel10Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel10Base.router_ip()
            network_conf = PyCrCTFLevel10Base.network_conf()
            attacker_action_conf = PyCrCTFLevel10V1.attacker_actions_conf(num_nodes=PyCrCTFLevel10Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel10Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel10Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel10V1.defender_actions_conf(
                num_nodes=PyCrCTFLevel10Base.num_nodes(), subnet_mask=PyCrCTFLevel10Base.subnet_mask())
            env_config = PyCrCTFLevel10V1.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super(PyCRCTFLevel10Emulation1Env, self).__init__(env_config=env_config)


# -------- Version 1 with costs------------
class PyCRCTFLevel10EmulationWithCosts1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel10Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel10Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel10Base.router_ip()
            network_conf = PyCrCTFLevel10Base.network_conf()
            attacker_action_conf = PyCrCTFLevel10V1.attacker_actions_conf(num_nodes=PyCrCTFLevel10Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel10Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel10Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel10V1.defender_actions_conf(
                num_nodes=PyCrCTFLevel10Base.num_nodes(), subnet_mask=PyCrCTFLevel10Base.subnet_mask())
            env_config = PyCrCTFLevel10V1.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super(PyCRCTFLevel10EmulationWithCosts1Env, self).__init__(env_config=env_config)


# -------- Version 2 ------------
class PyCRCTFLevel10Emulation2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel10Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel10Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel10Base.router_ip()
            network_conf = PyCrCTFLevel10Base.network_conf()
            attacker_action_conf = PyCrCTFLevel10V2.attacker_actions_conf(num_nodes=PyCrCTFLevel10Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel10Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel10Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel10V2.defender_actions_conf(
                num_nodes=PyCrCTFLevel10Base.num_nodes(), subnet_mask=PyCrCTFLevel10Base.subnet_mask())
            env_config = PyCrCTFLevel10V2.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super(PyCRCTFLevel10Emulation2Env, self).__init__(env_config=env_config)


# -------- Version 2 with costs------------
class PyCRCTFLevel10EmulationWithCosts2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel10Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel10Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel10Base.router_ip()
            network_conf = PyCrCTFLevel10Base.network_conf()
            attacker_action_conf = PyCrCTFLevel10V2.attacker_actions_conf(num_nodes=PyCrCTFLevel10Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel10Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel10Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel10V2.defender_actions_conf(
                num_nodes=PyCrCTFLevel10Base.num_nodes(), subnet_mask=PyCrCTFLevel10Base.subnet_mask())
            env_config = PyCrCTFLevel10V2.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super(PyCRCTFLevel10EmulationWithCosts2Env, self).__init__(env_config=env_config)


# -------- Version 3 ------------
class PyCRCTFLevel10Emulation3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel10Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel10Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel10Base.router_ip()
            network_conf = PyCrCTFLevel10Base.network_conf()
            attacker_action_conf = PyCrCTFLevel10V3.attacker_actions_conf(num_nodes=PyCrCTFLevel10Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel10Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel10Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel10V3.defender_actions_conf(
                num_nodes=PyCrCTFLevel10Base.num_nodes(), subnet_mask=PyCrCTFLevel10Base.subnet_mask())
            env_config = PyCrCTFLevel10V3.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super(PyCRCTFLevel10Emulation3Env, self).__init__(env_config=env_config)


# -------- Version 3 with costs------------
class PyCRCTFLevel10EmulationWithCosts3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel10Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel10Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel10Base.router_ip()
            network_conf = PyCrCTFLevel10Base.network_conf()
            attacker_action_conf = PyCrCTFLevel10V3.attacker_actions_conf(num_nodes=PyCrCTFLevel10Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel10Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel10Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel10V3.defender_actions_conf(
                num_nodes=PyCrCTFLevel10Base.num_nodes(), subnet_mask=PyCrCTFLevel10Base.subnet_mask())
            env_config = PyCrCTFLevel10V3.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super(PyCRCTFLevel10EmulationWithCosts3Env, self).__init__(env_config=env_config)


# -------- Version 4 ------------
class PyCRCTFLevel10Emulation4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel10Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel10Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel10Base.router_ip()
            network_conf = PyCrCTFLevel10Base.network_conf()
            attacker_action_conf = PyCrCTFLevel10V4.attacker_actions_conf(num_nodes=PyCrCTFLevel10Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel10Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel10Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel10V4.defender_actions_conf(
                num_nodes=PyCrCTFLevel10Base.num_nodes(), subnet_mask=PyCrCTFLevel10Base.subnet_mask())
            env_config = PyCrCTFLevel10V4.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super(PyCRCTFLevel10Emulation4Env, self).__init__(env_config=env_config)


# -------- Version 4 with costs------------
class PyCRCTFLevel10EmulationWithCosts4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel10Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel10Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = PyCrCTFLevel10Base.router_ip()
            network_conf = PyCrCTFLevel10Base.network_conf()
            attacker_action_conf = PyCrCTFLevel10V4.attacker_actions_conf(num_nodes=PyCrCTFLevel10Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel10Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel10Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel10V4.defender_actions_conf(
                num_nodes=PyCrCTFLevel10Base.num_nodes(), subnet_mask=PyCrCTFLevel10Base.subnet_mask())
            env_config = PyCrCTFLevel10V4.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super(PyCRCTFLevel10EmulationWithCosts4Env, self).__init__(env_config=env_config)
