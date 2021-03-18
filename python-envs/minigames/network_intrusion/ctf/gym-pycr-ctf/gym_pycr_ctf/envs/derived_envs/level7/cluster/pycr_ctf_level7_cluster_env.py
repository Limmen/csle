from gym_pycr_ctf.dao.network.env_mode import EnvMode
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.cluster_config import ClusterConfig
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.envs.config.level_7.pycr_ctf_level_7_base import PyCrCTFLevel7Base
from gym_pycr_ctf.envs.config.level_7.pycr_ctf_level_7_v1 import PyCrCTFLevel7V1
from gym_pycr_ctf.envs.config.level_7.pycr_ctf_level_7_v2 import PyCrCTFLevel7V2
from gym_pycr_ctf.envs.config.level_7.pycr_ctf_level_7_v3 import PyCrCTFLevel7V3
from gym_pycr_ctf.envs.config.level_7.pycr_ctf_level_7_v4 import PyCrCTFLevel7V4


# -------- Base Version (for testing) ------------
class PyCRCTFLevel7ClusterBaseEnv(PyCRCTFEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel7Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel7Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel7Base.router_ip()
            network_conf = PyCrCTFLevel7Base.network_conf()
            action_conf = PyCrCTFLevel7Base.all_actions_conf(num_nodes=PyCrCTFLevel7Base.num_nodes(),
                                                                 subnet_mask=PyCrCTFLevel7Base.subnet_mask(),
                                                                 hacker_ip=PyCrCTFLevel7Base.hacker_ip())
            env_config = PyCrCTFLevel7Base.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 1 ------------

class PyCRCTFLevel7Cluster1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel7Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel7Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel7Base.router_ip()
            network_conf = PyCrCTFLevel7Base.network_conf()
            action_conf = PyCrCTFLevel7V1.actions_conf(num_nodes=PyCrCTFLevel7Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel7Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel7Base.hacker_ip())
            env_config = PyCrCTFLevel7V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 1 with costs------------

class PyCRCTFLevel7ClusterWithCosts1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel7Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel7Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel7Base.router_ip()
            network_conf = PyCrCTFLevel7Base.network_conf()
            action_conf = PyCrCTFLevel7V1.actions_conf(num_nodes=PyCrCTFLevel7Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel7Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel7Base.hacker_ip())
            env_config = PyCrCTFLevel7V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 ------------

class PyCRCTFLevel7Cluster2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel7Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel7Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel7Base.router_ip()
            network_conf = PyCrCTFLevel7Base.network_conf()
            action_conf = PyCrCTFLevel7V2.actions_conf(num_nodes=PyCrCTFLevel7Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel7Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel7Base.hacker_ip())
            env_config = PyCrCTFLevel7V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 with costs------------

class PyCRCTFLevel7ClusterWithCosts2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel7Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel7Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel7Base.router_ip()
            network_conf = PyCrCTFLevel7Base.network_conf()
            action_conf = PyCrCTFLevel7V2.actions_conf(num_nodes=PyCrCTFLevel7Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel7Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel7Base.hacker_ip())
            env_config = PyCrCTFLevel7V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 ------------

class PyCRCTFLevel7Cluster3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel7Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel7Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel7Base.router_ip()
            network_conf = PyCrCTFLevel7Base.network_conf()
            action_conf = PyCrCTFLevel7V3.actions_conf(num_nodes=PyCrCTFLevel7Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel7Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel7Base.hacker_ip())
            env_config = PyCrCTFLevel7V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 with costs------------

class PyCRCTFLevel7ClusterWithCosts3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel7Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel7Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel7Base.router_ip()
            network_conf = PyCrCTFLevel7Base.network_conf()
            action_conf = PyCrCTFLevel7V3.actions_conf(num_nodes=PyCrCTFLevel7Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel7Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel7Base.hacker_ip())
            env_config = PyCrCTFLevel7V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 ------------

class PyCRCTFLevel7Cluster4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel7Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel7Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel7Base.router_ip()
            network_conf = PyCrCTFLevel7Base.network_conf()
            action_conf = PyCrCTFLevel7V4.actions_conf(num_nodes=PyCrCTFLevel7Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel7Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel7Base.hacker_ip())
            env_config = PyCrCTFLevel7V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 with costs------------

class PyCRCTFLevel7ClusterWithCosts4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel7Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel7Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel7Base.router_ip()
            network_conf = PyCrCTFLevel7Base.network_conf()
            action_conf = PyCrCTFLevel7V4.actions_conf(num_nodes=PyCrCTFLevel7Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel7Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel7Base.hacker_ip())
            env_config = PyCrCTFLevel7V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)
