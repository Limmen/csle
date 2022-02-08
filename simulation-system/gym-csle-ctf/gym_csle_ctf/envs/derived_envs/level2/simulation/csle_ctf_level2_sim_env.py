from csle_common.dao.network.env_mode import EnvMode
from csle_common.dao.network.emulation_config import EmulationConfig
from gym_csle_ctf.dao.network.env_config import csleEnvConfig
from gym_csle_ctf.envs.csle_ctf_env import CSLECTFEnv
from gym_csle_ctf.envs_model.config.level_2.csle_ctf_level_2_base import CSLECTFLevel2Base
from gym_csle_ctf.envs_model.config.level_2.csle_ctf_level_2_v1 import CSLECTFLevel2V1


# -------- Base Version (for testing) ------------
class CSLECTFLevel2SimBaseEnv(CSLECTFEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: csleEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel2Base.render_conf()
            network_conf = CSLECTFLevel2Base.network_conf()
            attacker_action_conf = CSLECTFLevel2Base.attacker_all_actions_conf(num_nodes=CSLECTFLevel2Base.num_nodes(),
                                                                      subnet_mask=CSLECTFLevel2Base.subnet_mask(),
                                                                      hacker_ip=CSLECTFLevel2Base.hacker_ip())
            defender_action_conf = CSLECTFLevel2Base.defender_all_actions_conf(
                num_nodes=CSLECTFLevel2Base.num_nodes(), subnet_mask=CSLECTFLevel2Base.subnet_mask())
            env_config = CSLECTFLevel2Base.env_config(network_conf=network_conf,
                                                      attacker_action_conf=attacker_action_conf,
                                                      defender_action_conf=defender_action_conf,
                                                      emulation_config=None, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.simulate_detection = True
            env_config.save_trajectories = False
            # env_config.simulate_detection = False
            env_config.env_mode = EnvMode.SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super(CSLECTFLevel2SimBaseEnv, self).__init__(env_config=env_config)

# -------- Simulations ------------


# -------- Version 1 ------------
class CSLECTFLevel2Sim1Env(CSLECTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: csleEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel2Base.render_conf()
            network_conf = CSLECTFLevel2Base.network_conf()
            attacker_action_conf = CSLECTFLevel2V1.attacker_actions_conf(num_nodes=CSLECTFLevel2Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel2Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel2Base.hacker_ip())
            defender_action_conf = CSLECTFLevel2V1.defender_actions_conf(
                num_nodes=CSLECTFLevel2Base.num_nodes(), subnet_mask=CSLECTFLevel2Base.subnet_mask())
            env_config = CSLECTFLevel2V1.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=None, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super(CSLECTFLevel2Sim1Env, self).__init__(env_config=env_config)

# -------- Version 1, Costs ------------
class CSLECTFLevel2SimWithCosts1Env(CSLECTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: csleEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel2Base.render_conf()
            network_conf = CSLECTFLevel2Base.network_conf()
            attacker_action_conf = CSLECTFLevel2V1.attacker_actions_conf(num_nodes=CSLECTFLevel2Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel2Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel2Base.hacker_ip())
            defender_action_conf = CSLECTFLevel2V1.defender_actions_conf(
                num_nodes=CSLECTFLevel2Base.num_nodes(), subnet_mask=CSLECTFLevel2Base.subnet_mask())
            env_config = CSLECTFLevel2V1.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=None, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)