from gym_pycr_ctf.dao.network.env_mode import EnvMode
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.cluster_config import ClusterConfig
from gym_pycr_ctf.dao.container_config.containers_config import ContainersConfig
from gym_pycr_ctf.dao.container_config.flags_config import FlagsConfig
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.envs.config.random.pycr_ctf_random_base import PyCrCTFRandomBase
from gym_pycr_ctf.envs.config.random.pycr_ctf_random_v1 import PyCrCTFRandomV1
from gym_pycr_ctf.envs.config.random.pycr_ctf_random_v2 import PyCrCTFRandomV2
from gym_pycr_ctf.envs.config.random.pycr_ctf_random_v3 import PyCrCTFRandomV3
from gym_pycr_ctf.envs.config.random.pycr_ctf_random_v4 import PyCrCTFRandomV4


# -------- Base Version (for testing) ------------
class PyCRCTFRandomClusterBaseEnv(PyCRCTFEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrCTFRandomBase.all_actions_conf(num_nodes=num_nodes-1,
                                                                 subnet_mask=containers_config.subnet_mask,
                                                                 hacker_ip=containers_config.agent_ip)
            env_config = PyCrCTFRandomBase.env_config(containers_config=containers_config, flags_config=flags_config,
                                                          action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config,
                                                          num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 1 ------------

class PyCRCTFRandomCluster1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrCTFRandomV1.actions_conf(num_nodes=num_nodes-1,
                                                                 subnet_mask=containers_config.subnet_mask,
                                                                 hacker_ip=containers_config.agent_ip)
            env_config = PyCrCTFRandomV1.env_config(containers_config=containers_config,
                                                          flags_config=flags_config,
                                                          action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config,
                                                          num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 50
        super().__init__(env_config=env_config)


# -------- Version 1 with costs------------

class PyCRCTFRandomClusterWithCosts1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrCTFRandomV1.actions_conf(num_nodes=num_nodes-1,
                                                           subnet_mask=containers_config.subnet_mask,
                                                           hacker_ip=containers_config.agent_ip)
            env_config = PyCrCTFRandomV1.env_config(containers_config=containers_config,
                                                        flags_config=flags_config,
                                                        action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config,
                                                        num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 ------------
class PyCRCTFRandomCluster2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrCTFRandomV2.actions_conf(num_nodes=num_nodes-1,
                                                           subnet_mask=containers_config.subnet_mask,
                                                           hacker_ip=containers_config.agent_ip)
            env_config = PyCrCTFRandomV2.env_config(containers_config=containers_config,
                                                        flags_config=flags_config,
                                                        action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config,
                                                        num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 50
        super().__init__(env_config=env_config)


# -------- Version 2 with costs------------

class PyCRCTFRandomClusterWithCosts2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrCTFRandomV2.actions_conf(num_nodes=num_nodes-1,
                                                           subnet_mask=containers_config.subnet_mask,
                                                           hacker_ip=containers_config.agent_ip)
            env_config = PyCrCTFRandomV2.env_config(containers_config=containers_config,
                                                        flags_config=flags_config,
                                                        action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config,
                                                        num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 50
        super().__init__(env_config=env_config)


# -------- Version 3 ------------
class PyCRCTFRandomCluster3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrCTFRandomV3.actions_conf(num_nodes=num_nodes-1,
                                                           subnet_mask=containers_config.subnet_mask,
                                                           hacker_ip=containers_config.agent_ip)
            env_config = PyCrCTFRandomV3.env_config(containers_config=containers_config,
                                                        flags_config=flags_config,
                                                        action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config,
                                                        num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 50
        super().__init__(env_config=env_config)

# -------- Version 3 with costs------------

class PyCRCTFRandomClusterWithCosts3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrCTFRandomV3.actions_conf(num_nodes=num_nodes-1,
                                                           subnet_mask=containers_config.subnet_mask,
                                                           hacker_ip=containers_config.agent_ip)
            env_config = PyCrCTFRandomV3.env_config(containers_config=containers_config,
                                                        flags_config=flags_config,
                                                        action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config,
                                                        num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 50
        super().__init__(env_config=env_config)


# -------- Version 4 ------------
class PyCRCTFRandomCluster4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrCTFRandomV4.actions_conf(num_nodes= num_nodes-1,
                                                           subnet_mask=containers_config.subnet_mask,
                                                           hacker_ip=containers_config.agent_ip)
            env_config = PyCrCTFRandomV4.env_config(containers_config=containers_config,
                                                        flags_config=flags_config,
                                                        action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config,
                                                        num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 50
        super().__init__(env_config=env_config)


# -------- Version 4 with costs------------
class PyCRCTFRandomClusterWithCosts4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrCTFRandomV4.actions_conf(num_nodes=num_nodes-1,
                                                           subnet_mask=containers_config.subnet_mask,
                                                           hacker_ip=containers_config.agent_ip)
            env_config = PyCrCTFRandomV4.env_config(containers_config=containers_config,
                                                        flags_config=flags_config,
                                                        action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config,
                                                        num_nodes=num_nodes-1)
            env_config.cost_coefficient = 1
            env_config.alerts_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 50
        super().__init__(env_config=env_config)

