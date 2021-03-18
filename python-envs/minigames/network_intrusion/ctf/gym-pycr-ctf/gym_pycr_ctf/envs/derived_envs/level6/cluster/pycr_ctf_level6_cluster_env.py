from gym_pycr_ctf.dao.network.env_mode import EnvMode
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.cluster_config import ClusterConfig
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.envs.config.level_6.pycr_ctf_level_6_base import PyCrCTFLevel6Base
from gym_pycr_ctf.envs.config.level_6.pycr_ctf_level_6_v1 import PyCrCTFLevel6V1
from gym_pycr_ctf.envs.config.level_6.pycr_ctf_level_6_v2 import PyCrCTFLevel6V2
from gym_pycr_ctf.envs.config.level_6.pycr_ctf_level_6_v3 import PyCrCTFLevel6V3
from gym_pycr_ctf.envs.config.level_6.pycr_ctf_level_6_v4 import PyCrCTFLevel6V4

# -------- Base Version (for testing) ------------
class PyCRCTFLevel6ClusterBaseEnv(PyCRCTFEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel6Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel6Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel6Base.router_ip()
            network_conf = PyCrCTFLevel6Base.network_conf()
            action_conf = PyCrCTFLevel6Base.all_actions_conf(num_nodes=PyCrCTFLevel6Base.num_nodes(),
                                                                 subnet_mask=PyCrCTFLevel6Base.subnet_mask(),
                                                                 hacker_ip=PyCrCTFLevel6Base.hacker_ip())
            env_config = PyCrCTFLevel6Base.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 1 ------------

class PyCRCTFLevel6Cluster1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel6Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel6Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel6Base.router_ip()
            network_conf = PyCrCTFLevel6Base.network_conf()
            action_conf = PyCrCTFLevel6V1.actions_conf(num_nodes=PyCrCTFLevel6Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel6Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel6Base.hacker_ip())
            env_config = PyCrCTFLevel6V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 100
        super().__init__(env_config=env_config)


# -------- Version 1 with costs------------

class PyCRCTFLevel6ClusterWithCosts1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel6Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel6Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel6Base.router_ip()
            network_conf = PyCrCTFLevel6Base.network_conf()
            action_conf = PyCrCTFLevel6V1.actions_conf(num_nodes=PyCrCTFLevel6Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel6Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel6Base.hacker_ip())
            env_config = PyCrCTFLevel6V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 ------------

class PyCRCTFLevel6Cluster2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel6Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel6Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel6Base.router_ip()
            network_conf = PyCrCTFLevel6Base.network_conf()
            action_conf = PyCrCTFLevel6V2.actions_conf(num_nodes=PyCrCTFLevel6Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel6Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel6Base.hacker_ip())
            env_config = PyCrCTFLevel6V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 with costs------------

class PyCRCTFLevel6ClusterWithCosts2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel6Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel6Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel6Base.router_ip()
            network_conf = PyCrCTFLevel6Base.network_conf()
            action_conf = PyCrCTFLevel6V2.actions_conf(num_nodes=PyCrCTFLevel6Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel6Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel6Base.hacker_ip())
            env_config = PyCrCTFLevel6V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 ------------

class PyCRCTFLevel6Cluster3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel6Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel6Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel6Base.router_ip()
            network_conf = PyCrCTFLevel6Base.network_conf()
            action_conf = PyCrCTFLevel6V3.actions_conf(num_nodes=PyCrCTFLevel6Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel6Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel6Base.hacker_ip())
            env_config = PyCrCTFLevel6V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 with costs------------

class PyCRCTFLevel6ClusterWithCosts3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel6Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel6Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel6Base.router_ip()
            network_conf = PyCrCTFLevel6Base.network_conf()
            action_conf = PyCrCTFLevel6V3.actions_conf(num_nodes=PyCrCTFLevel6Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel6Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel6Base.hacker_ip())
            env_config = PyCrCTFLevel6V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 ------------

class PyCRCTFLevel6Cluster4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel6Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel6Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel6Base.router_ip()
            network_conf = PyCrCTFLevel6Base.network_conf()
            action_conf = PyCrCTFLevel6V4.actions_conf(num_nodes=PyCrCTFLevel6Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel6Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel6Base.hacker_ip())
            env_config = PyCrCTFLevel6V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 with costs------------

class PyCRCTFLevel6ClusterWithCosts4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel6Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel6Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel6Base.router_ip()
            network_conf = PyCrCTFLevel6Base.network_conf()
            action_conf = PyCrCTFLevel6V4.actions_conf(num_nodes=PyCrCTFLevel6Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel6Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel6Base.hacker_ip())
            env_config = PyCrCTFLevel6V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)