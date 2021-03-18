from gym_pycr_ctf.dao.network.env_mode import EnvMode
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.cluster_config import ClusterConfig
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.envs.config.level_2.pycr_ctf_level_2_base import PyCrCTFLevel2Base
from gym_pycr_ctf.envs.config.level_2.pycr_ctf_level_2_v1 import PyCrCTFLevel2V1


# -------- Base Version (for testing) ------------
class PyCRCTFLevel2SimBaseEnv(PyCRCTFEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel2Base.render_conf()
            network_conf = PyCrCTFLevel2Base.network_conf()
            action_conf = PyCrCTFLevel2Base.all_actions_conf(num_nodes=PyCrCTFLevel2Base.num_nodes(),
                                                                 subnet_mask=PyCrCTFLevel2Base.subnet_mask(),
                                                                 hacker_ip=PyCrCTFLevel2Base.hacker_ip())
            env_config = PyCrCTFLevel2Base.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=None, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.simulate_detection = True
            env_config.save_trajectories = False
            # env_config.simulate_detection = False
            env_config.env_mode = EnvMode.SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Simulations ------------

# -------- Version 1 ------------
class PyCRCTFLevel2Sim1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel2Base.render_conf()
            network_conf = PyCrCTFLevel2Base.network_conf()
            action_conf = PyCrCTFLevel2V1.actions_conf(num_nodes=PyCrCTFLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel2Base.hacker_ip())
            env_config = PyCrCTFLevel2V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=None, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 1, Costs ------------
class PyCRCTFLevel2SimWithCosts1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel2Base.render_conf()
            network_conf = PyCrCTFLevel2Base.network_conf()
            action_conf = PyCrCTFLevel2V1.actions_conf(num_nodes=PyCrCTFLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel2Base.hacker_ip())
            env_config = PyCrCTFLevel2V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=None, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)