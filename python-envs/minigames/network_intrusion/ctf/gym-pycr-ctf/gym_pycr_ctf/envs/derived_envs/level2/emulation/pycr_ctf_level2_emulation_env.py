from gym_pycr_ctf.dao.network.env_mode import EnvMode
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.envs.config.level_2.pycr_ctf_level_2_base import PyCrCTFLevel2Base
from gym_pycr_ctf.envs.config.level_2.pycr_ctf_level_2_v1 import PyCrCTFLevel2V1
from gym_pycr_ctf.envs.config.level_2.pycr_ctf_level_2_v2 import PyCrCTFLevel2V2
from gym_pycr_ctf.envs.config.level_2.pycr_ctf_level_2_v3 import PyCrCTFLevel2V3
from gym_pycr_ctf.envs.config.level_2.pycr_ctf_level_2_v4 import PyCrCTFLevel2V4


# -------- Base Version (for testing) ------------
class PyCRCTFLevel2EmulationBaseEnv(PyCRCTFEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel2Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel2Base.emulation_config()
            network_conf = PyCrCTFLevel2Base.network_conf()
            action_conf = PyCrCTFLevel2Base.all_actions_conf(num_nodes=PyCrCTFLevel2Base.num_nodes(),
                                                                 subnet_mask=PyCrCTFLevel2Base.subnet_mask(),
                                                                 hacker_ip=PyCrCTFLevel2Base.hacker_ip())
            env_config = PyCrCTFLevel2Base.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          emulation_config=emulation_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 1 ------------

class PyCRCTFLevel2Emulation1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel2Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel2Base.emulation_config()
            network_conf = PyCrCTFLevel2Base.network_conf()
            action_conf = PyCrCTFLevel2V1.actions_conf(num_nodes=PyCrCTFLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel2Base.hacker_ip())
            env_config = PyCrCTFLevel2V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        emulation_config=emulation_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 1 with costs ------------

class PyCRCTFLevel2EmulationWithCosts1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel2Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel2Base.emulation_config()
            network_conf = PyCrCTFLevel2Base.network_conf()
            action_conf = PyCrCTFLevel2V1.actions_conf(num_nodes=PyCrCTFLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel2Base.hacker_ip())
            env_config = PyCrCTFLevel2V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        emulation_config=emulation_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 2 ------------

class PyCRCTFLevel2Emulation2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel2Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel2Base.emulation_config()
            network_conf = PyCrCTFLevel2Base.network_conf()
            action_conf = PyCrCTFLevel2V2.actions_conf(num_nodes=PyCrCTFLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel2Base.hacker_ip())
            env_config = PyCrCTFLevel2V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        emulation_config=emulation_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 with costs ------------

class PyCRCTFLevel2EmulationWithCosts2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel2Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel2Base.emulation_config()
            network_conf = PyCrCTFLevel2Base.network_conf()
            action_conf = PyCrCTFLevel2V2.actions_conf(num_nodes=PyCrCTFLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel2Base.hacker_ip())
            env_config = PyCrCTFLevel2V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        emulation_config=emulation_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 ------------

class PyCRCTFLevel2Emulation3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel2Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel2Base.emulation_config()
            network_conf = PyCrCTFLevel2Base.network_conf()
            action_conf = PyCrCTFLevel2V3.actions_conf(num_nodes=PyCrCTFLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel2Base.hacker_ip())
            env_config = PyCrCTFLevel2V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        emulation_config=emulation_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 with costs ------------

class PyCRCTFLevel2EmulationWithCosts3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel2Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel2Base.emulation_config()
            network_conf = PyCrCTFLevel2Base.network_conf()
            action_conf = PyCrCTFLevel2V3.actions_conf(num_nodes=PyCrCTFLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel2Base.hacker_ip())
            env_config = PyCrCTFLevel2V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        emulation_config=emulation_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 4 ------------

class PyCRCTFLevel2Emulation4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel2Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel2Base.emulation_config()
            network_conf = PyCrCTFLevel2Base.network_conf()
            action_conf = PyCrCTFLevel2V4.actions_conf(num_nodes=PyCrCTFLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel2Base.hacker_ip())
            env_config = PyCrCTFLevel2V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        emulation_config=emulation_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 4 with costs ------------

class PyCRCTFLevel2EmulationWithCosts4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel2Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel2Base.emulation_config()
            network_conf = PyCrCTFLevel2Base.network_conf()
            action_conf = PyCrCTFLevel2V4.actions_conf(num_nodes=PyCrCTFLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel2Base.hacker_ip())
            env_config = PyCrCTFLevel2V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        emulation_config=emulation_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.emulation
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)