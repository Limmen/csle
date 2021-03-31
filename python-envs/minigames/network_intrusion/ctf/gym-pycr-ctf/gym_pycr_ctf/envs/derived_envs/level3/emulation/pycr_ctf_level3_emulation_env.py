from gym_pycr_ctf.dao.network.env_mode import EnvMode
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.envs.config.level_3.pycr_ctf_level_3_base import PyCrCTFLevel3Base
from gym_pycr_ctf.envs.config.level_3.pycr_ctf_level_3_v1 import PyCrCTFLevel3V1
from gym_pycr_ctf.envs.config.level_3.pycr_ctf_level_3_v2 import PyCrCTFLevel3V2
from gym_pycr_ctf.envs.config.level_3.pycr_ctf_level_3_v3 import PyCrCTFLevel3V3
from gym_pycr_ctf.envs.config.level_3.pycr_ctf_level_3_v4 import PyCrCTFLevel3V4


# -------- Base Version (for testing) ------------
class PyCRCTFLevel3EmulationBaseEnv(PyCRCTFEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel3Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel3Base.emulation_config()
            network_conf = PyCrCTFLevel3Base.network_conf()
            action_conf = PyCrCTFLevel3Base.attacker_all_actions_conf(num_nodes=PyCrCTFLevel3Base.num_nodes(),
                                                                      subnet_mask=PyCrCTFLevel3Base.subnet_mask(),
                                                                      hacker_ip=PyCrCTFLevel3Base.hacker_ip())
            env_config = PyCrCTFLevel3Base.env_config(network_conf=network_conf, attacker_action_conf=action_conf,
                                                      emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 1 ------------

class PyCRCTFLevel3Emulation1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel3Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel3Base.emulation_config()
            network_conf = PyCrCTFLevel3Base.network_conf()
            action_conf = PyCrCTFLevel3V1.attacker_actions_conf(num_nodes=PyCrCTFLevel3Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel3Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel3Base.hacker_ip())
            env_config = PyCrCTFLevel3V1.env_config(network_conf=network_conf, attacker_action_conf=action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 1 with costs ------------

class PyCRCTFLevel3EmulationWithCosts1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel3Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel3Base.emulation_config()
            network_conf = PyCrCTFLevel3Base.network_conf()
            action_conf = PyCrCTFLevel3V1.attacker_actions_conf(num_nodes=PyCrCTFLevel3Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel3Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel3Base.hacker_ip())
            env_config = PyCrCTFLevel3V1.env_config(network_conf=network_conf, attacker_action_conf=action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 2 ------------

class PyCRCTFLevel3Emulation2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel3Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel3Base.emulation_config()
            network_conf = PyCrCTFLevel3Base.network_conf()
            action_conf = PyCrCTFLevel3V2.attacker_actions_conf(num_nodes=PyCrCTFLevel3Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel3Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel3Base.hacker_ip())
            env_config = PyCrCTFLevel3V2.env_config(network_conf=network_conf, attacker_action_conf=action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 with costs ------------

class PyCRCTFLevel3EmulationWithCosts2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel3Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel3Base.emulation_config()
            network_conf = PyCrCTFLevel3Base.network_conf()
            action_conf = PyCrCTFLevel3V2.attacker_actions_conf(num_nodes=PyCrCTFLevel3Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel3Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel3Base.hacker_ip())
            env_config = PyCrCTFLevel3V2.env_config(network_conf=network_conf, attacker_action_conf=action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 3 ------------

class PyCRCTFLevel3Emulation3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel3Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel3Base.emulation_config()
            network_conf = PyCrCTFLevel3Base.network_conf()
            action_conf = PyCrCTFLevel3V3.attacker_actions_conf(num_nodes=PyCrCTFLevel3Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel3Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel3Base.hacker_ip())
            env_config = PyCrCTFLevel3V3.env_config(network_conf=network_conf, attacker_action_conf=action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 3 ------------

class PyCRCTFLevel3EmulationWithCosts3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel3Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel3Base.emulation_config()
            network_conf = PyCrCTFLevel3Base.network_conf()
            action_conf = PyCrCTFLevel3V3.attacker_actions_conf(num_nodes=PyCrCTFLevel3Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel3Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel3Base.hacker_ip())
            env_config = PyCrCTFLevel3V3.env_config(network_conf=network_conf, attacker_action_conf=action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 4 ------------

class PyCRCTFLevel3Emulation4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel3Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel3Base.emulation_config()
            network_conf = PyCrCTFLevel3Base.network_conf()
            action_conf = PyCrCTFLevel3V4.attacker_actions_conf(num_nodes=PyCrCTFLevel3Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel3Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel3Base.hacker_ip())
            env_config = PyCrCTFLevel3V4.env_config(network_conf=network_conf, attacker_action_conf=action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 4 with costs------------

class PyCRCTFLevel3EmulationWithCosts4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel3Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel3Base.emulation_config()
            network_conf = PyCrCTFLevel3Base.network_conf()
            action_conf = PyCrCTFLevel3V4.attacker_actions_conf(num_nodes=PyCrCTFLevel3Base.num_nodes(),
                                                                subnet_mask=PyCrCTFLevel3Base.subnet_mask(),
                                                                hacker_ip=PyCrCTFLevel3Base.hacker_ip())
            env_config = PyCrCTFLevel3V4.env_config(network_conf=network_conf, attacker_action_conf=action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)