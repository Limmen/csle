from typing import List
from gym_pycr_ctf.dao.network.env_mode import EnvMode
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.cluster_config import ClusterConfig
from gym_pycr_ctf.dao.container_config.containers_config import ContainersConfig
from gym_pycr_ctf.dao.container_config.flags_config import FlagsConfig
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.envs.config.random.pycr_ctf_random_base import PyCrCTFRandomBase
from gym_pycr_ctf.envs.config.random.pycr_ctf_random_v1 import PyCrCTFRandomV1


# -------- Version 1 Cluster ------------
class PyCRCTFRandomManyCluster1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_configs: List[ContainersConfig], flags_configs: List[FlagsConfig], idx : int,
                 num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = max(list(map(lambda x: len(x.containers), containers_configs)))
        containers_config = containers_configs[idx]
        flags_config = flags_configs[idx]
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
            env_config.idx = idx
            env_config.filter_illegal_actions = True
            env_config.max_episode_length = 200
            env_config.simulate_detection = False
            env_config.domain_randomization = False
            env_config.compute_pi_star = True
            env_config.use_upper_bound_pi_star = True
        super().__init__(env_config=env_config)


# -------- Version 1 With Costs ------------

class PyCRCTFRandomManyClusterWithCosts1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_configs: List[ContainersConfig], flags_configs: List[FlagsConfig], idx : int,
                 num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = max(list(map(lambda x: len(x.containers), containers_configs)))
        containers_config = containers_configs[idx]
        flags_config = flags_configs[idx]
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
            env_config.cost_coefficient = 1
            env_config.alerts_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.idx=idx
            env_config.filter_illegal_actions = True
            env_config.max_episode_length = 200
            env_config.compute_pi_star = False
            env_config.use_upper_bound_pi_star = True
        super().__init__(env_config=env_config)
