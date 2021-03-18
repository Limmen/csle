"""
Register OpenAI Envs
"""
from gym.envs.registration import register

# -------- Difficulty Level: Level1, Mode: Simulation, Version: Base ------------
register(
    id='pycr-ctf-level-1-sim-base-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1SimBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Version: Base ------------
register(
    id='pycr-ctf-level-1-cluster-base-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1ClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Version: 1 ------------
register(
    id='pycr-ctf-level-1-sim-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1Sim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-1-sim-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1SimWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-ctf-level-1-cluster-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1Cluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, No Cache Version: 1 ------------
register(
    id='pycr-ctf-level-1-cluster-nocache-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1ClusterNoCache1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-1-cluster-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1ClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Version: 1 ------------
register(
    id='pycr-ctf-level-1-generated-sim-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1GeneratedSim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-1-generated-sim-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1GeneratedSimWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Version: 2 ------------
register(
    id='pycr-ctf-level-1-sim-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1Sim2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-1-sim-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1SimWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-ctf-level-1-cluster-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1Cluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-1-cluster-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1ClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Version: 2 ------------
register(
    id='pycr-ctf-level-1-generated-sim-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1GeneratedSim2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-1-generated-sim-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1GeneratedSimWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Version: 3 ------------
register(
    id='pycr-ctf-level-1-sim-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1Sim3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, costs, Version: 3 ------------
register(
    id='pycr-ctf-level-1-sim-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1SimWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Version: 3 ------------
register(
    id='pycr-ctf-level-1-generated-sim-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1GeneratedSim3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-1-generated-sim-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1GeneratedSimWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-ctf-level-1-cluster-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1Cluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-1-cluster-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1ClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Version: 4 ------------
register(
    id='pycr-ctf-level-1-sim-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1Sim4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-1-sim-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1SimWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Version: 4 ------------
register(
    id='pycr-ctf-level-1-generated-sim-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1GeneratedSim4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-1-generated-sim-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1GeneratedSimWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-ctf-level-1-cluster-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1Cluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-ctf-level-1-cluster-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel1ClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Simulation, Version: Base ------------
register(
    id='pycr-ctf-level-2-sim-base-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel2SimBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Version: Base ------------
register(
    id='pycr-ctf-level-2-cluster-base-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel2ClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-ctf-level-2-cluster-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel2Cluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-2-cluster-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel2ClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-ctf-level-2-cluster-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel2Cluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-2-cluster-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel2ClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-ctf-level-2-cluster-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel2Cluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-2-cluster-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel2ClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-ctf-level-2-cluster-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel2Cluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-2-cluster-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel2ClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Version: 1 ------------
register(
    id='pycr-ctf-level-2-generated-sim-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel2GeneratedSim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-2-generated-sim-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel2GeneratedSimWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Simulation, Version: 1 ------------
register(
    id='pycr-ctf-level-2-sim-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel2Sim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Simulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-2-sim-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel2SimWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: Cluster, Version: Base ------------
register(
    id='pycr-ctf-level-3-cluster-base-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel3ClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-ctf-level-3-cluster-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel3Cluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-3-cluster-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel3ClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Version: 2 ------------
register(
    id='pycr-ctf-level-2-generated-sim-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel2GeneratedSim2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-2-generated-sim-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel2GeneratedSimWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-ctf-level-3-cluster-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel3Cluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-3-cluster-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel3ClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Version: 3 ------------
register(
    id='pycr-ctf-level-2-generated-sim-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel2GeneratedSim3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-2-generated-sim-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel2GeneratedSimWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-ctf-level-3-cluster-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel3Cluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-3-cluster-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel3ClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Version: 4 ------------
register(
    id='pycr-ctf-level-2-generated-sim-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel2GeneratedSim4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-2-generated-sim-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel2GeneratedSimWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-ctf-level-3-cluster-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel3Cluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: Cluster, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-3-cluster-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel3ClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

## Level 4

# -------- Difficulty Level: Level4, Mode: Cluster, Version: Base ------------
register(
    id='pycr-ctf-level-4-cluster-base-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel4ClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-ctf-level-4-cluster-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel4Cluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-4-cluster-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel4ClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-ctf-level-4-cluster-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel4Cluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-4-cluster-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel4ClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-ctf-level-4-cluster-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel4Cluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-4-cluster-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel4ClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-ctf-level-4-cluster-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel4Cluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-4-cluster-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel4ClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

## Level 5

# -------- Difficulty Level: Level5, Mode: Cluster, Version: Base ------------
register(
    id='pycr-ctf-level-5-cluster-base-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel5ClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-ctf-level-5-cluster-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel5Cluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-5-cluster-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel5ClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-ctf-level-5-cluster-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel5Cluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-5-cluster-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel5ClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-ctf-level-5-cluster-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel5Cluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-5-cluster-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel5ClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-ctf-level-5-cluster-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel5Cluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-5-cluster-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel5ClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

## Level 6

# -------- Difficulty Level: Level6, Mode: Cluster, Version: Base ------------
register(
    id='pycr-ctf-level-6-cluster-base-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel6ClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-ctf-level-6-cluster-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel6Cluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-6-cluster-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel6ClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-ctf-level-6-cluster-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel6Cluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-6-cluster-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel6ClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-ctf-level-6-cluster-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel6Cluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-6-cluster-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel6ClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-ctf-level-6-cluster-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel6Cluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-6-cluster-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel6ClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

## Random

# -------- Difficulty Level: Random, Mode: Cluster, Version: Base ------------
register(
    id='pycr-ctf-random-cluster-base-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfRandomClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-ctf-random-cluster-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfRandomCluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-ctf-random-cluster-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfRandomClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Version: 1 ------------
register(
    id='pycr-ctf-random-generated-sim-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfRandomGeneratedSim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-random-generated-sim-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfRandomGeneratedSim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-ctf-random-cluster-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfRandomCluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-ctf-random-cluster-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfRandomClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Version: 2 ------------
register(
    id='pycr-ctf-random-generated-sim-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfRandomGeneratedSim2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-random-generated-sim-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfRandomGeneratedSim2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-ctf-random-cluster-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfRandomCluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-ctf-random-cluster-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfRandomClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Version: 3 ------------
register(
    id='pycr-ctf-random-generated-sim-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfRandomGeneratedSim3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Costs, Version: 3 ------------
register(
    id='pycr-ctf-random-generated-sim-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfRandomGeneratedSim3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-ctf-random-cluster-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfRandomCluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Costs, Version: 4 ------------
register(
    id='pycr-ctf-random-cluster-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfRandomClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Version: 4 ------------
register(
    id='pycr-ctf-random-generated-sim-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfRandomGeneratedSim4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-random-generated-sim-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfRandomGeneratedSim4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

## Random Many

# -------- Difficulty Level: Random Many, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-ctf-random-many-cluster-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfRandomManyCluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_configs": None, "flags_configs": None, "idx": None}
)

# -------- Difficulty Level: Random Many, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-ctf-random-many-cluster-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfRandomManyClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_configs": None, "flags_configs": None, "idx": None}
)

# -------- Difficulty Level: Random Many, Mode: Generated Simulation, Version: 1 ------------
register(
    id='pycr-ctf-random-many-generated-sim-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfRandomManyGeneratedSim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_configs": None, "flags_configs": None, "idx": None}
)

# -------- Difficulty Level: MultiSim, Mode: Multi-Simulation, Version: 1 ------------
register(
    id='pycr-ctf-multisim-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfMultiSim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "idx": None, "dr_max_num_nodes": int, "dr_min_num_nodes": int, "dr_max_num_flags": int,
            "dr_min_num_flags": int, "dr_min_num_users": int, "dr_max_num_users": int}
)

## Level 7

# -------- Difficulty Level: Level7, Mode: Cluster, Version: Base ------------
register(
    id='pycr-ctf-level-7-cluster-base-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel7ClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-ctf-level-7-cluster-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel7Cluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-7-cluster-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel7ClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-ctf-level-7-cluster-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel7Cluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-7-cluster-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel7ClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-ctf-level-7-cluster-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel7Cluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-7-cluster-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel7ClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-ctf-level-7-cluster-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel7Cluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-7-cluster-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRctfLevel7ClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)
