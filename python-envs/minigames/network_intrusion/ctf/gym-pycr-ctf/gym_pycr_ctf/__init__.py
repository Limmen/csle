"""
Register OpenAI Envs
"""
from gym.envs.registration import register

# -------- Difficulty Level: Level1, Mode: Simulation, Version: Base ------------
register(
    id='pycr-ctf-level-1-sim-base-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1SimBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Version: Base ------------
register(
    id='pycr-ctf-level-1-cluster-base-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1ClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Version: 1 ------------
register(
    id='pycr-ctf-level-1-sim-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1Sim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-1-sim-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1SimWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-ctf-level-1-cluster-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1Cluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, No Cache Version: 1 ------------
register(
    id='pycr-ctf-level-1-cluster-nocache-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1ClusterNoCache1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-1-cluster-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1ClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Version: 1 ------------
register(
    id='pycr-ctf-level-1-generated-sim-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1GeneratedSim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-1-generated-sim-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1GeneratedSimWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Version: 2 ------------
register(
    id='pycr-ctf-level-1-sim-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1Sim2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-1-sim-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1SimWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-ctf-level-1-cluster-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1Cluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-1-cluster-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1ClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Version: 2 ------------
register(
    id='pycr-ctf-level-1-generated-sim-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1GeneratedSim2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-1-generated-sim-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1GeneratedSimWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Version: 3 ------------
register(
    id='pycr-ctf-level-1-sim-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1Sim3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, costs, Version: 3 ------------
register(
    id='pycr-ctf-level-1-sim-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1SimWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Version: 3 ------------
register(
    id='pycr-ctf-level-1-generated-sim-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1GeneratedSim3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-1-generated-sim-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1GeneratedSimWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-ctf-level-1-cluster-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1Cluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-1-cluster-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1ClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Version: 4 ------------
register(
    id='pycr-ctf-level-1-sim-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1Sim4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-1-sim-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1SimWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Version: 4 ------------
register(
    id='pycr-ctf-level-1-generated-sim-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1GeneratedSim4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-1-generated-sim-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1GeneratedSimWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-ctf-level-1-cluster-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1Cluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-ctf-level-1-cluster-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel1ClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Simulation, Version: Base ------------
register(
    id='pycr-ctf-level-2-sim-base-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel2SimBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Version: Base ------------
register(
    id='pycr-ctf-level-2-cluster-base-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel2ClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-ctf-level-2-cluster-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel2Cluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-2-cluster-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel2ClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-ctf-level-2-cluster-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel2Cluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-2-cluster-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel2ClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-ctf-level-2-cluster-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel2Cluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-2-cluster-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel2ClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-ctf-level-2-cluster-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel2Cluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-2-cluster-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel2ClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Version: 1 ------------
register(
    id='pycr-ctf-level-2-generated-sim-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel2GeneratedSim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-2-generated-sim-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel2GeneratedSimWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Simulation, Version: 1 ------------
register(
    id='pycr-ctf-level-2-sim-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel2Sim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Simulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-2-sim-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel2SimWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: Cluster, Version: Base ------------
register(
    id='pycr-ctf-level-3-cluster-base-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel3ClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-ctf-level-3-cluster-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel3Cluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-3-cluster-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel3ClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Version: 2 ------------
register(
    id='pycr-ctf-level-2-generated-sim-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel2GeneratedSim2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-2-generated-sim-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel2GeneratedSimWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-ctf-level-3-cluster-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel3Cluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-3-cluster-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel3ClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Version: 3 ------------
register(
    id='pycr-ctf-level-2-generated-sim-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel2GeneratedSim3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-2-generated-sim-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel2GeneratedSimWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-ctf-level-3-cluster-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel3Cluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-3-cluster-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel3ClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Version: 4 ------------
register(
    id='pycr-ctf-level-2-generated-sim-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel2GeneratedSim4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-2-generated-sim-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel2GeneratedSimWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-ctf-level-3-cluster-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel3Cluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: Cluster, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-3-cluster-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel3ClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

## Level 4

# -------- Difficulty Level: Level4, Mode: Cluster, Version: Base ------------
register(
    id='pycr-ctf-level-4-cluster-base-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel4ClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-ctf-level-4-cluster-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel4Cluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-4-cluster-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel4ClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-ctf-level-4-cluster-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel4Cluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-4-cluster-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel4ClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-ctf-level-4-cluster-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel4Cluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-4-cluster-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel4ClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-ctf-level-4-cluster-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel4Cluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-4-cluster-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel4ClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

## Level 5

# -------- Difficulty Level: Level5, Mode: Cluster, Version: Base ------------
register(
    id='pycr-ctf-level-5-cluster-base-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel5ClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-ctf-level-5-cluster-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel5Cluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-5-cluster-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel5ClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-ctf-level-5-cluster-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel5Cluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-5-cluster-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel5ClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-ctf-level-5-cluster-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel5Cluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-5-cluster-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel5ClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-ctf-level-5-cluster-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel5Cluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-5-cluster-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel5ClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

## Level 6

# -------- Difficulty Level: Level6, Mode: Cluster, Version: Base ------------
register(
    id='pycr-ctf-level-6-cluster-base-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel6ClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-ctf-level-6-cluster-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel6Cluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-6-cluster-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel6ClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-ctf-level-6-cluster-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel6Cluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-6-cluster-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel6ClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-ctf-level-6-cluster-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel6Cluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-6-cluster-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel6ClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-ctf-level-6-cluster-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel6Cluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-6-cluster-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel6ClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

## Random

# -------- Difficulty Level: Random, Mode: Cluster, Version: Base ------------
register(
    id='pycr-ctf-random-cluster-base-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFRandomClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-ctf-random-cluster-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFRandomCluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-ctf-random-cluster-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFRandomClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Version: 1 ------------
register(
    id='pycr-ctf-random-generated-sim-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFRandomGeneratedSim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-random-generated-sim-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFRandomGeneratedSim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-ctf-random-cluster-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFRandomCluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-ctf-random-cluster-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFRandomClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Version: 2 ------------
register(
    id='pycr-ctf-random-generated-sim-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFRandomGeneratedSim2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-random-generated-sim-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFRandomGeneratedSim2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-ctf-random-cluster-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFRandomCluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-ctf-random-cluster-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFRandomClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Version: 3 ------------
register(
    id='pycr-ctf-random-generated-sim-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFRandomGeneratedSim3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Costs, Version: 3 ------------
register(
    id='pycr-ctf-random-generated-sim-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFRandomGeneratedSim3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-ctf-random-cluster-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFRandomCluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Costs, Version: 4 ------------
register(
    id='pycr-ctf-random-cluster-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFRandomClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Version: 4 ------------
register(
    id='pycr-ctf-random-generated-sim-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFRandomGeneratedSim4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-random-generated-sim-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFRandomGeneratedSim4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

## Random Many

# -------- Difficulty Level: Random Many, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-ctf-random-many-cluster-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFRandomManyCluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_configs": None, "flags_configs": None, "idx": None}
)

# -------- Difficulty Level: Random Many, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-ctf-random-many-cluster-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFRandomManyClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_configs": None, "flags_configs": None, "idx": None}
)

# -------- Difficulty Level: Random Many, Mode: Generated Simulation, Version: 1 ------------
register(
    id='pycr-ctf-random-many-generated-sim-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFRandomManyGeneratedSim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_configs": None, "flags_configs": None, "idx": None}
)

# -------- Difficulty Level: MultiSim, Mode: Multi-Simulation, Version: 1 ------------
register(
    id='pycr-ctf-multisim-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFMultiSim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "idx": None, "dr_max_num_nodes": int, "dr_min_num_nodes": int, "dr_max_num_flags": int,
            "dr_min_num_flags": int, "dr_min_num_users": int, "dr_max_num_users": int}
)

## Level 7

# -------- Difficulty Level: Level7, Mode: Cluster, Version: Base ------------
register(
    id='pycr-ctf-level-7-cluster-base-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel7ClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-ctf-level-7-cluster-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel7Cluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-7-cluster-costs-v1',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel7ClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-ctf-level-7-cluster-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel7Cluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-7-cluster-costs-v2',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel7ClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-ctf-level-7-cluster-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel7Cluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-7-cluster-costs-v3',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel7ClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-ctf-level-7-cluster-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel7Cluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-7-cluster-costs-v4',
    entry_point='gym_pycr_ctf.envs.pycr_ctf_env:PyCRCTFLevel7ClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)
