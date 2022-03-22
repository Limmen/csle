from csle_common.dao.network.env_mode import EnvMode
from csle_common.dao.network.emulation_config import EmulationConfig
from gym_csle_ctf.dao.network.env_config import CSLEEnvConfig
from gym_csle_ctf.envs.csle_ctf_env import CSLECTFEnv
from gym_csle_ctf.envs_model.config.level_3.csle_ctf_level_3_base import CSLECTFLevel3Base
from gym_csle_ctf.envs_model.config.level_3.csle_ctf_level_3_v1 import CSLECTFLevel3V1
from gym_csle_ctf.envs_model.config.level_3.csle_ctf_level_3_v2 import CSLECTFLevel3V2
from gym_csle_ctf.envs_model.config.level_3.csle_ctf_level_3_v3 import CSLECTFLevel3V3
from gym_csle_ctf.envs_model.config.level_3.csle_ctf_level_3_v4 import CSLECTFLevel3V4


# -------- Base Version (for testing) ------------
class CSLECTFLevel3EmulationBaseEnv(CSLECTFEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel3Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel3Base.emulation_config()
            network_conf = CSLECTFLevel3Base.network_conf()
            attacker_action_conf = CSLECTFLevel3Base.attacker_all_actions_conf(num_nodes=CSLECTFLevel3Base.num_nodes(),
                                                                      subnet_mask=CSLECTFLevel3Base.subnet_mask(),
                                                                      hacker_ip=CSLECTFLevel3Base.hacker_ip())
            defender_action_conf = CSLECTFLevel3Base.defender_all_actions_conf(
                num_nodes=CSLECTFLevel3Base.num_nodes(), subnet_mask=CSLECTFLevel3Base.subnet_mask())
            env_config = CSLECTFLevel3Base.env_config(network_conf=network_conf,
                                                      attacker_action_conf=attacker_action_conf,
                                                      defender_action_conf=defender_action_conf,
                                                      emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super(CSLECTFLevel3EmulationBaseEnv, self).__init__(env_config=env_config)

# -------- Version 1 ------------

class CSLECTFLevel3Emulation1Env(CSLECTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel3Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel3Base.emulation_config()
            network_conf = CSLECTFLevel3Base.network_conf()
            attacker_action_conf = CSLECTFLevel3V1.attacker_actions_conf(num_nodes=CSLECTFLevel3Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel3Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel3Base.hacker_ip())
            defender_action_conf = CSLECTFLevel3V1.defender_actions_conf(
                num_nodes=CSLECTFLevel3Base.num_nodes(), subnet_mask=CSLECTFLevel3Base.subnet_mask())
            env_config = CSLECTFLevel3V1.env_config(network_conf=network_conf,
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

# -------- Version 1 with costs ------------

class CSLECTFLevel3EmulationWithCosts1Env(CSLECTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel3Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel3Base.emulation_config()
            network_conf = CSLECTFLevel3Base.network_conf()
            attacker_action_conf = CSLECTFLevel3V1.attacker_actions_conf(num_nodes=CSLECTFLevel3Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel3Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel3Base.hacker_ip())
            defender_action_conf = CSLECTFLevel3V1.defender_actions_conf(
                num_nodes=CSLECTFLevel3Base.num_nodes(), subnet_mask=CSLECTFLevel3Base.subnet_mask())
            env_config = CSLECTFLevel3V1.env_config(network_conf=network_conf,
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

class CSLECTFLevel3Emulation2Env(CSLECTFEnv):
    """
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel3Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel3Base.emulation_config()
            network_conf = CSLECTFLevel3Base.network_conf()
            attacker_action_conf = CSLECTFLevel3V2.attacker_actions_conf(num_nodes=CSLECTFLevel3Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel3Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel3Base.hacker_ip())
            defender_action_conf = CSLECTFLevel3V2.defender_actions_conf(
                num_nodes=CSLECTFLevel3Base.num_nodes(), subnet_mask=CSLECTFLevel3Base.subnet_mask())
            env_config = CSLECTFLevel3V2.env_config(network_conf=network_conf,
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


# -------- Version 2 with costs ------------

class CSLECTFLevel3EmulationWithCosts2Env(CSLECTFEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel3Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel3Base.emulation_config()
            network_conf = CSLECTFLevel3Base.network_conf()
            attacker_action_conf = CSLECTFLevel3V2.attacker_actions_conf(num_nodes=CSLECTFLevel3Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel3Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel3Base.hacker_ip())
            defender_action_conf = CSLECTFLevel3V2.defender_actions_conf(
                num_nodes=CSLECTFLevel3Base.num_nodes(), subnet_mask=CSLECTFLevel3Base.subnet_mask())
            env_config = CSLECTFLevel3V2.env_config(network_conf=network_conf,
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

class CSLECTFLevel3Emulation3Env(CSLECTFEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel3Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel3Base.emulation_config()
            network_conf = CSLECTFLevel3Base.network_conf()
            attacker_action_conf = CSLECTFLevel3V3.attacker_actions_conf(num_nodes=CSLECTFLevel3Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel3Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel3Base.hacker_ip())
            defender_action_conf = CSLECTFLevel3V3.defender_actions_conf(
                num_nodes=CSLECTFLevel3Base.num_nodes(), subnet_mask=CSLECTFLevel3Base.subnet_mask())
            env_config = CSLECTFLevel3V3.env_config(network_conf=network_conf,
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

# -------- Version 3 ------------

class CSLECTFLevel3EmulationWithCosts3Env(CSLECTFEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel3Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel3Base.emulation_config()
            network_conf = CSLECTFLevel3Base.network_conf()
            attacker_action_conf = CSLECTFLevel3V3.attacker_actions_conf(num_nodes=CSLECTFLevel3Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel3Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel3Base.hacker_ip())
            defender_action_conf = CSLECTFLevel3V3.defender_actions_conf(
                num_nodes=CSLECTFLevel3Base.num_nodes(), subnet_mask=CSLECTFLevel3Base.subnet_mask())
            env_config = CSLECTFLevel3V3.env_config(network_conf=network_conf,
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

class CSLECTFLevel3Emulation4Env(CSLECTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel3Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel3Base.emulation_config()
            network_conf = CSLECTFLevel3Base.network_conf()
            attacker_action_conf = CSLECTFLevel3V4.attacker_actions_conf(num_nodes=CSLECTFLevel3Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel3Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel3Base.hacker_ip())
            defender_action_conf = CSLECTFLevel3V4.defender_actions_conf(
                num_nodes=CSLECTFLevel3Base.num_nodes(), subnet_mask=CSLECTFLevel3Base.subnet_mask())
            env_config = CSLECTFLevel3V4.env_config(network_conf=network_conf,
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

class CSLECTFLevel3EmulationWithCosts4Env(CSLECTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel3Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel3Base.emulation_config()
            network_conf = CSLECTFLevel3Base.network_conf()
            attacker_action_conf = CSLECTFLevel3V4.attacker_actions_conf(num_nodes=CSLECTFLevel3Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel3Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel3Base.hacker_ip())
            defender_action_conf = CSLECTFLevel3V4.defender_actions_conf(
                num_nodes=CSLECTFLevel3Base.num_nodes(), subnet_mask=CSLECTFLevel3Base.subnet_mask())
            env_config = CSLECTFLevel3V4.env_config(network_conf=network_conf,
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