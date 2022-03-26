from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.dao.network.env_mode import EnvMode
from csle_common.dao.network.env_config import CSLEEnvConfig
from gym_csle_ctf.envs.csle_ctf_env import CSLECTFEnv
from gym_csle_ctf.envs_model.config.level_7.csle_ctf_level_7_base import CSLECTFLevel7Base
from gym_csle_ctf.envs_model.config.level_7.csle_ctf_level_7_v1 import CSLECTFLevel7V1
from gym_csle_ctf.envs_model.config.level_7.csle_ctf_level_7_v2 import CSLECTFLevel7V2
from gym_csle_ctf.envs_model.config.level_7.csle_ctf_level_7_v3 import CSLECTFLevel7V3
from gym_csle_ctf.envs_model.config.level_7.csle_ctf_level_7_v4 import CSLECTFLevel7V4


# -------- Base Version (for testing) ------------
class CSLECTFLevel7EmulationBaseEnv(CSLECTFEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel7Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel7Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel7Base.router_ip()
            network_conf = CSLECTFLevel7Base.network_conf()
            attacker_action_conf = CSLECTFLevel7Base.attacker_all_actions_conf(num_nodes=CSLECTFLevel7Base.num_nodes(),
                                                                      subnet_mask=CSLECTFLevel7Base.subnet_mask(),
                                                                      hacker_ip=CSLECTFLevel7Base.hacker_ip())
            defender_action_conf = CSLECTFLevel7Base.defender_all_actions_conf(
                num_nodes=CSLECTFLevel7Base.num_nodes(), subnet_mask=CSLECTFLevel7Base.subnet_mask())
            env_config = CSLECTFLevel7Base.env_config(network_conf=network_conf,
                                                      attacker_action_conf=attacker_action_conf,
                                                      defender_action_conf=defender_action_conf,
                                                      emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super(CSLECTFLevel7EmulationBaseEnv, self).__init__(env_config=env_config)


# -------- Version 1 ------------

class CSLECTFLevel7Emulation1Env(CSLECTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel7Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel7Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel7Base.router_ip()
            network_conf = CSLECTFLevel7Base.network_conf()
            attacker_action_conf = CSLECTFLevel7V1.attacker_actions_conf(num_nodes=CSLECTFLevel7Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel7Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel7Base.hacker_ip())
            defender_action_conf = CSLECTFLevel7V1.defender_actions_conf(
                num_nodes=CSLECTFLevel7Base.num_nodes(), subnet_mask=CSLECTFLevel7Base.subnet_mask())
            env_config = CSLECTFLevel7V1.env_config(network_conf=network_conf,
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

class CSLECTFLevel7EmulationWithCosts1Env(CSLECTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel7Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel7Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel7Base.router_ip()
            network_conf = CSLECTFLevel7Base.network_conf()
            attacker_action_conf = CSLECTFLevel7V1.attacker_actions_conf(num_nodes=CSLECTFLevel7Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel7Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel7Base.hacker_ip())
            defender_action_conf = CSLECTFLevel7V1.defender_actions_conf(
                num_nodes=CSLECTFLevel7Base.num_nodes(), subnet_mask=CSLECTFLevel7Base.subnet_mask())
            env_config = CSLECTFLevel7V1.env_config(network_conf=network_conf,
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

class CSLECTFLevel7Emulation2Env(CSLECTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel7Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel7Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel7Base.router_ip()
            network_conf = CSLECTFLevel7Base.network_conf()
            attacker_action_conf = CSLECTFLevel7V2.attacker_actions_conf(num_nodes=CSLECTFLevel7Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel7Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel7Base.hacker_ip())
            defender_action_conf = CSLECTFLevel7V2.defender_actions_conf(
                num_nodes=CSLECTFLevel7Base.num_nodes(), subnet_mask=CSLECTFLevel7Base.subnet_mask())
            env_config = CSLECTFLevel7V2.env_config(network_conf=network_conf,
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

class CSLECTFLevel7EmulationWithCosts2Env(CSLECTFEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel7Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel7Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel7Base.router_ip()
            network_conf = CSLECTFLevel7Base.network_conf()
            attacker_action_conf = CSLECTFLevel7V2.attacker_actions_conf(num_nodes=CSLECTFLevel7Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel7Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel7Base.hacker_ip())
            defender_action_conf = CSLECTFLevel7V2.defender_actions_conf(
                num_nodes=CSLECTFLevel7Base.num_nodes(), subnet_mask=CSLECTFLevel7Base.subnet_mask())
            env_config = CSLECTFLevel7V2.env_config(network_conf=network_conf,
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

class CSLECTFLevel7Emulation3Env(CSLECTFEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel7Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel7Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel7Base.router_ip()
            network_conf = CSLECTFLevel7Base.network_conf()
            attacker_action_conf = CSLECTFLevel7V3.attacker_actions_conf(num_nodes=CSLECTFLevel7Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel7Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel7Base.hacker_ip())
            defender_action_conf = CSLECTFLevel7V3.defender_actions_conf(
                num_nodes=CSLECTFLevel7Base.num_nodes(), subnet_mask=CSLECTFLevel7Base.subnet_mask())
            env_config = CSLECTFLevel7V3.env_config(network_conf=network_conf,
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

class CSLECTFLevel7EmulationWithCosts3Env(CSLECTFEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel7Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel7Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel7Base.router_ip()
            network_conf = CSLECTFLevel7Base.network_conf()
            attacker_action_conf = CSLECTFLevel7V3.attacker_actions_conf(num_nodes=CSLECTFLevel7Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel7Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel7Base.hacker_ip())
            defender_action_conf = CSLECTFLevel7V3.defender_actions_conf(
                num_nodes=CSLECTFLevel7Base.num_nodes(), subnet_mask=CSLECTFLevel7Base.subnet_mask())
            env_config = CSLECTFLevel7V3.env_config(network_conf=network_conf,
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

class CSLECTFLevel7Emulation4Env(CSLECTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel7Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel7Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel7Base.router_ip()
            network_conf = CSLECTFLevel7Base.network_conf()
            attacker_action_conf = CSLECTFLevel7V4.attacker_actions_conf(num_nodes=CSLECTFLevel7Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel7Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel7Base.hacker_ip())
            defender_action_conf = CSLECTFLevel7V4.defender_actions_conf(
                num_nodes=CSLECTFLevel7Base.num_nodes(), subnet_mask=CSLECTFLevel7Base.subnet_mask())
            env_config = CSLECTFLevel7V4.env_config(network_conf=network_conf,
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

class CSLECTFLevel7EmulationWithCosts4Env(CSLECTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel7Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel7Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel7Base.router_ip()
            network_conf = CSLECTFLevel7Base.network_conf()
            attacker_action_conf = CSLECTFLevel7V4.attacker_actions_conf(num_nodes=CSLECTFLevel7Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel7Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel7Base.hacker_ip())
            defender_action_conf = CSLECTFLevel7V4.defender_actions_conf(
                num_nodes=CSLECTFLevel7Base.num_nodes(), subnet_mask=CSLECTFLevel7Base.subnet_mask())
            env_config = CSLECTFLevel7V4.env_config(network_conf=network_conf,
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
