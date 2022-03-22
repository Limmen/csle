from csle_common.dao.network.env_mode import EnvMode
from csle_common.dao.network.emulation_config import EmulationConfig
from gym_csle_ctf.dao.network.env_config import CSLEEnvConfig
from gym_csle_ctf.envs.csle_ctf_env import CSLECTFEnv
from gym_csle_ctf.envs_model.config.level_1.csle_ctf_level_1_base import CSLECTFLevel1Base
from gym_csle_ctf.envs_model.config.level_1.csle_ctf_level_1_v1 import CSLECTFLevel1V1
from gym_csle_ctf.envs_model.config.level_1.csle_ctf_level_1_v2 import CSLECTFLevel1V2
from gym_csle_ctf.envs_model.config.level_1.csle_ctf_level_1_v3 import CSLECTFLevel1V3
from gym_csle_ctf.envs_model.config.level_1.csle_ctf_level_1_v4 import CSLECTFLevel1V4
from gym_csle_ctf.envs_model.config.level_1.csle_ctf_level_1_nocache_v1 import CSLECTFLevel1NoCacheV1

# -------- Base Version ------------

class CSLECTFLevel1EmulationBaseEnv(CSLECTFEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel1Base.emulation_config()
            network_conf = CSLECTFLevel1Base.network_conf()
            attacker_action_conf = CSLECTFLevel1Base.attacker_all_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                 subnet_mask=CSLECTFLevel1Base.subnet_mask(),
                                                                 hacker_ip=CSLECTFLevel1Base.hacker_ip())
            defender_action_conf = CSLECTFLevel1Base.defender_actions_conf(
                num_nodes=CSLECTFLevel1Base.num_nodes(), subnet_mask=CSLECTFLevel1Base.subnet_mask())
            env_config = CSLECTFLevel1Base.env_config(network_conf=network_conf, attacker_action_conf=attacker_action_conf,
                                                      defender_action_conf=defender_action_conf,
                                                      emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super(CSLECTFLevel1EmulationBaseEnv, self).__init__(env_config=env_config)

# -------- Version 1 ------------

class CSLECTFLevel1Emulation1Env(CSLECTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel1Base.emulation_config()
            network_conf = CSLECTFLevel1Base.network_conf()
            attacker_action_conf = CSLECTFLevel1V1.attacker_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel1Base.subnet_mask(),
                                                                         hacker_ip=CSLECTFLevel1Base.hacker_ip())
            defender_action_conf = CSLECTFLevel1V1.defender_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                               subnet_mask=CSLECTFLevel1Base.subnet_mask())
            env_config = CSLECTFLevel1V1.env_config(network_conf=network_conf, attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 1 No Cache ------------

class CSLECTFLevel1EmulationNoCache1Env(CSLECTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    No cache
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel1Base.emulation_config()
            network_conf = CSLECTFLevel1Base.network_conf()
            attacker_action_conf = CSLECTFLevel1NoCacheV1.attacker_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                       subnet_mask=CSLECTFLevel1Base.subnet_mask(),
                                                                       hacker_ip=CSLECTFLevel1Base.hacker_ip())
            defender_action_conf = CSLECTFLevel1NoCacheV1.defender_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                               subnet_mask=CSLECTFLevel1Base.subnet_mask())
            env_config = CSLECTFLevel1NoCacheV1.env_config(network_conf=network_conf,
                                                           attacker_action_conf=attacker_action_conf,
                                                           defender_action_conf=defender_action_conf,
                                                           emulation_config=emulation_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 1 With costs ------------

class CSLECTFLevel1EmulationWithCosts1Env(CSLECTFEnv):
    """
    Uses a minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel1Base.emulation_config()
            network_conf = CSLECTFLevel1Base.network_conf()
            attacker_action_conf = CSLECTFLevel1V1.attacker_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel1Base.subnet_mask(),
                                                                         hacker_ip=CSLECTFLevel1Base.hacker_ip())
            defender_action_conf = CSLECTFLevel1V1.defender_actions_conf(
                num_nodes=CSLECTFLevel1Base.num_nodes(), subnet_mask=CSLECTFLevel1Base.subnet_mask())
            env_config = CSLECTFLevel1V1.env_config(network_conf=network_conf,
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

class CSLECTFLevel1Emulation2Env(CSLECTFEnv):
    """
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel1Base.emulation_config()
            network_conf = CSLECTFLevel1Base.network_conf()
            attacker_action_conf = CSLECTFLevel1V2.attacker_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel1Base.subnet_mask(),
                                                                         hacker_ip=CSLECTFLevel1Base.hacker_ip())
            defender_action_conf = CSLECTFLevel1V2.defender_actions_conf(
                num_nodes=CSLECTFLevel1Base.num_nodes(), subnet_mask=CSLECTFLevel1Base.subnet_mask())
            env_config = CSLECTFLevel1V2.env_config(network_conf=network_conf,
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


# -------- Version 2 with Costs ------------

class CSLECTFLevel1EmulationWithCosts2Env(CSLECTFEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel1Base.emulation_config()
            network_conf = CSLECTFLevel1Base.network_conf()
            attacker_action_conf = CSLECTFLevel1V2.attacker_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel1Base.subnet_mask(),
                                                                         hacker_ip=CSLECTFLevel1Base.hacker_ip()),
            defender_action_conf = CSLECTFLevel1V2.defender_actions_conf(
                num_nodes=CSLECTFLevel1Base.num_nodes(), subnet_mask=CSLECTFLevel1Base.subnet_mask())
            env_config = CSLECTFLevel1V2.env_config(network_conf=network_conf,
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

class CSLECTFLevel1Emulation3Env(CSLECTFEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel1Base.emulation_config()
            network_conf = CSLECTFLevel1Base.network_conf()
            attacker_action_conf = CSLECTFLevel1V3.attacker_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel1Base.subnet_mask(),
                                                                         hacker_ip=CSLECTFLevel1Base.hacker_ip())
            defender_action_conf = CSLECTFLevel1V3.defender_actions_conf(
                num_nodes=CSLECTFLevel1Base.num_nodes(), subnet_mask=CSLECTFLevel1Base.subnet_mask())
            env_config = CSLECTFLevel1V3.env_config(network_conf=network_conf,
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


# -------- Version 3 with Costs ------------

class CSLECTFLevel1EmulationWithCosts3Env(CSLECTFEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel1Base.emulation_config()
            network_conf = CSLECTFLevel1Base.network_conf()
            attacker_action_conf = CSLECTFLevel1V3.attacker_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel1Base.subnet_mask(),
                                                                         hacker_ip=CSLECTFLevel1Base.hacker_ip())
            defender_action_conf = CSLECTFLevel1V3.defender_actions_conf(
                num_nodes=CSLECTFLevel1Base.num_nodes(), subnet_mask=CSLECTFLevel1Base.subnet_mask())
            env_config = CSLECTFLevel1V3.env_config(network_conf=network_conf,
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

class CSLECTFLevel1Emulation4Env(CSLECTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel1Base.emulation_config()
            network_conf = CSLECTFLevel1Base.network_conf()
            attacker_action_conf = CSLECTFLevel1V4.attacker_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel1Base.subnet_mask(),
                                                                         hacker_ip=CSLECTFLevel1Base.hacker_ip())
            defender_action_conf = CSLECTFLevel1V4.defender_actions_conf(
                num_nodes=CSLECTFLevel1Base.num_nodes(), subnet_mask=CSLECTFLevel1Base.subnet_mask())
            env_config = CSLECTFLevel1V4.env_config(network_conf=network_conf,
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


# -------- Version 4 with costs ------------

class CSLECTFLevel1EmulationWithCosts4Env(CSLECTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel1Base.emulation_config()
            network_conf = CSLECTFLevel1Base.network_conf()
            attacker_action_conf = CSLECTFLevel1V4.attacker_actions_conf(num_nodes=CSLECTFLevel1Base.num_nodes(),
                                                                         subnet_mask=CSLECTFLevel1Base.subnet_mask(),
                                                                         hacker_ip=CSLECTFLevel1Base.hacker_ip())
            defender_action_conf = CSLECTFLevel1V4.defender_actions_conf(
                num_nodes=CSLECTFLevel1Base.num_nodes(), subnet_mask=CSLECTFLevel1Base.subnet_mask())
            env_config = CSLECTFLevel1V4.env_config(network_conf=network_conf,
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