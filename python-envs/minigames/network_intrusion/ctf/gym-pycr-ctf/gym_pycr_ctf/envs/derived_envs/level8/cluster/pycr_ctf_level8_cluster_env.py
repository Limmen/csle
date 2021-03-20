from gym_pycr_ctf.dao.network.env_mode import EnvMode
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.cluster_config import ClusterConfig
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.envs.config.level_8.pycr_ctf_level_8_base import PyCrCTFLevel8Base
from gym_pycr_ctf.envs.config.level_8.pycr_ctf_level_8_v1 import PyCrCTFLevel8V1
from gym_pycr_ctf.envs.config.level_8.pycr_ctf_level_8_v2 import PyCrCTFLevel8V2
from gym_pycr_ctf.envs.config.level_8.pycr_ctf_level_8_v3 import PyCrCTFLevel8V3
from gym_pycr_ctf.envs.config.level_8.pycr_ctf_level_8_v4 import PyCrCTFLevel8V4


# -------- Base Version (for testing) ------------
class PyCRCTFLevel8ClusterBaseEnv(PyCRCTFEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel8Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel8Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel8Base.router_ip()
            network_conf = PyCrCTFLevel8Base.network_conf()
            action_conf = PyCrCTFLevel8Base.all_actions_conf(num_nodes=PyCrCTFLevel8Base.num_nodes(),
                                                                 subnet_mask=PyCrCTFLevel8Base.subnet_mask(),
                                                                 hacker_ip=PyCrCTFLevel8Base.hacker_ip())
            env_config = PyCrCTFLevel8Base.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 1 ------------

class PyCRCTFLevel8Cluster1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel8Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel8Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel8Base.router_ip()
            network_conf = PyCrCTFLevel8Base.network_conf()
            action_conf = PyCrCTFLevel8V1.actions_conf(num_nodes=PyCrCTFLevel8Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel8Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel8Base.hacker_ip())
            env_config = PyCrCTFLevel8V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 1 with costs------------

class PyCRCTFLevel8ClusterWithCosts1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel8Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel8Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel8Base.router_ip()
            network_conf = PyCrCTFLevel8Base.network_conf()
            action_conf = PyCrCTFLevel8V1.actions_conf(num_nodes=PyCrCTFLevel8Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel8Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel8Base.hacker_ip())
            env_config = PyCrCTFLevel8V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 ------------

class PyCRCTFLevel8Cluster2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel8Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel8Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel8Base.router_ip()
            network_conf = PyCrCTFLevel8Base.network_conf()
            action_conf = PyCrCTFLevel8V2.actions_conf(num_nodes=PyCrCTFLevel8Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel8Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel8Base.hacker_ip())
            env_config = PyCrCTFLevel8V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 with costs------------

class PyCRCTFLevel8ClusterWithCosts2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel8Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel8Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel8Base.router_ip()
            network_conf = PyCrCTFLevel8Base.network_conf()
            action_conf = PyCrCTFLevel8V2.actions_conf(num_nodes=PyCrCTFLevel8Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel8Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel8Base.hacker_ip())
            env_config = PyCrCTFLevel8V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 ------------

class PyCRCTFLevel8Cluster3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel8Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel8Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel8Base.router_ip()
            network_conf = PyCrCTFLevel8Base.network_conf()
            action_conf = PyCrCTFLevel8V3.actions_conf(num_nodes=PyCrCTFLevel8Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel8Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel8Base.hacker_ip())
            env_config = PyCrCTFLevel8V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 with costs------------

class PyCRCTFLevel8ClusterWithCosts3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel8Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel8Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel8Base.router_ip()
            network_conf = PyCrCTFLevel8Base.network_conf()
            action_conf = PyCrCTFLevel8V3.actions_conf(num_nodes=PyCrCTFLevel8Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel8Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel8Base.hacker_ip())
            env_config = PyCrCTFLevel8V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 ------------

class PyCRCTFLevel8Cluster4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel8Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel8Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel8Base.router_ip()
            network_conf = PyCrCTFLevel8Base.network_conf()
            action_conf = PyCrCTFLevel8V4.actions_conf(num_nodes=PyCrCTFLevel8Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel8Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel8Base.hacker_ip())
            env_config = PyCrCTFLevel8V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 with costs------------

class PyCRCTFLevel8ClusterWithCosts4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel8Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel8Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel8Base.router_ip()
            network_conf = PyCrCTFLevel8Base.network_conf()
            action_conf = PyCrCTFLevel8V4.actions_conf(num_nodes=PyCrCTFLevel8Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel8Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel8Base.hacker_ip())
            env_config = PyCrCTFLevel8V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)
