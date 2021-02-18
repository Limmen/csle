"""
Register OpenAI Envs
"""
from gym.envs.registration import register

# -------- Difficulty Level: Level1, Mode: Simulation, Version: Base ------------
register(
    id='pycr-pwcrack-level-1-sim-base-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1SimBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Version: Base ------------
register(
    id='pycr-pwcrack-level-1-cluster-base-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1ClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Version: 1 ------------
register(
    id='pycr-pwcrack-level-1-sim-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1Sim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Costs, Version: 1 ------------
register(
    id='pycr-pwcrack-level-1-sim-costs-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1SimWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-pwcrack-level-1-cluster-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1Cluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, No Cache Version: 1 ------------
register(
    id='pycr-pwcrack-level-1-cluster-nocache-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1ClusterNoCache1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-pwcrack-level-1-cluster-costs-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1ClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Version: 1 ------------
register(
    id='pycr-pwcrack-level-1-generated-sim-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1GeneratedSim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Costs, Version: 1 ------------
register(
    id='pycr-pwcrack-level-1-generated-sim-costs-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1GeneratedSimWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Version: 2 ------------
register(
    id='pycr-pwcrack-level-1-sim-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1Sim2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Costs, Version: 2 ------------
register(
    id='pycr-pwcrack-level-1-sim-costs-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1SimWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-pwcrack-level-1-cluster-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1Cluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-pwcrack-level-1-cluster-costs-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1ClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Version: 2 ------------
register(
    id='pycr-pwcrack-level-1-generated-sim-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1GeneratedSim2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Costs, Version: 2 ------------
register(
    id='pycr-pwcrack-level-1-generated-sim-costs-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1GeneratedSimWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Version: 3 ------------
register(
    id='pycr-pwcrack-level-1-sim-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1Sim3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, costs, Version: 3 ------------
register(
    id='pycr-pwcrack-level-1-sim-costs-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1SimWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Version: 3 ------------
register(
    id='pycr-pwcrack-level-1-generated-sim-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1GeneratedSim3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Costs, Version: 3 ------------
register(
    id='pycr-pwcrack-level-1-generated-sim-costs-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1GeneratedSimWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-pwcrack-level-1-cluster-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1Cluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-pwcrack-level-1-cluster-costs-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1ClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Version: 4 ------------
register(
    id='pycr-pwcrack-level-1-sim-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1Sim4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Costs, Version: 4 ------------
register(
    id='pycr-pwcrack-level-1-sim-costs-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1SimWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Version: 4 ------------
register(
    id='pycr-pwcrack-level-1-generated-sim-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1GeneratedSim4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Costs, Version: 4 ------------
register(
    id='pycr-pwcrack-level-1-generated-sim-costs-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1GeneratedSimWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-pwcrack-level-1-cluster-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1Cluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-pwcrack-level-1-cluster-costs-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel1ClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Simulation, Version: Base ------------
register(
    id='pycr-pwcrack-level-2-sim-base-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel2SimBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Version: Base ------------
register(
    id='pycr-pwcrack-level-2-cluster-base-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel2ClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-pwcrack-level-2-cluster-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel2Cluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-pwcrack-level-2-cluster-costs-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel2ClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-pwcrack-level-2-cluster-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel2Cluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-pwcrack-level-2-cluster-costs-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel2ClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-pwcrack-level-2-cluster-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel2Cluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-pwcrack-level-2-cluster-costs-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel2ClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-pwcrack-level-2-cluster-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel2Cluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Costs, Version: 4 ------------
register(
    id='pycr-pwcrack-level-2-cluster-costs-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel2ClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Version: 1 ------------
register(
    id='pycr-pwcrack-level-2-generated-sim-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel2GeneratedSim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Costs, Version: 1 ------------
register(
    id='pycr-pwcrack-level-2-generated-sim-costs-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel2GeneratedSimWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Simulation, Version: 1 ------------
register(
    id='pycr-pwcrack-level-2-sim-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel2Sim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Simulation, Costs, Version: 1 ------------
register(
    id='pycr-pwcrack-level-2-sim-costs-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel2SimWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: Cluster, Version: Base ------------
register(
    id='pycr-pwcrack-level-3-cluster-base-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel3ClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-pwcrack-level-3-cluster-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel3Cluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-pwcrack-level-3-cluster-costs-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel3ClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Version: 2 ------------
register(
    id='pycr-pwcrack-level-2-generated-sim-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel2GeneratedSim2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Costs, Version: 2 ------------
register(
    id='pycr-pwcrack-level-2-generated-sim-costs-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel2GeneratedSimWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-pwcrack-level-3-cluster-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel3Cluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-pwcrack-level-3-cluster-costs-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel3ClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Version: 3 ------------
register(
    id='pycr-pwcrack-level-2-generated-sim-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel2GeneratedSim3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Costs, Version: 3 ------------
register(
    id='pycr-pwcrack-level-2-generated-sim-costs-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel2GeneratedSimWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-pwcrack-level-3-cluster-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel3Cluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-pwcrack-level-3-cluster-costs-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel3ClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Version: 4 ------------
register(
    id='pycr-pwcrack-level-2-generated-sim-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel2GeneratedSim4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Costs, Version: 4 ------------
register(
    id='pycr-pwcrack-level-2-generated-sim-costs-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel2GeneratedSimWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-pwcrack-level-3-cluster-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel3Cluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: Cluster, Costs, Version: 4 ------------
register(
    id='pycr-pwcrack-level-3-cluster-costs-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel3ClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

## Level 4

# -------- Difficulty Level: Level4, Mode: Cluster, Version: Base ------------
register(
    id='pycr-pwcrack-level-4-cluster-base-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel4ClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-pwcrack-level-4-cluster-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel4Cluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-pwcrack-level-4-cluster-costs-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel4ClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-pwcrack-level-4-cluster-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel4Cluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-pwcrack-level-4-cluster-costs-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel4ClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-pwcrack-level-4-cluster-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel4Cluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-pwcrack-level-4-cluster-costs-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel4ClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-pwcrack-level-4-cluster-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel4Cluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Cluster, Costs, Version: 4 ------------
register(
    id='pycr-pwcrack-level-4-cluster-costs-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel4ClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

## Level 5

# -------- Difficulty Level: Level5, Mode: Cluster, Version: Base ------------
register(
    id='pycr-pwcrack-level-5-cluster-base-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel5ClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-pwcrack-level-5-cluster-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel5Cluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-pwcrack-level-5-cluster-costs-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel5ClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-pwcrack-level-5-cluster-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel5Cluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-pwcrack-level-5-cluster-costs-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel5ClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-pwcrack-level-5-cluster-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel5Cluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-pwcrack-level-5-cluster-costs-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel5ClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-pwcrack-level-5-cluster-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel5Cluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: Cluster, Costs, Version: 4 ------------
register(
    id='pycr-pwcrack-level-5-cluster-costs-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel5ClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

## Level 6

# -------- Difficulty Level: Level6, Mode: Cluster, Version: Base ------------
register(
    id='pycr-pwcrack-level-6-cluster-base-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel6ClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-pwcrack-level-6-cluster-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel6Cluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-pwcrack-level-6-cluster-costs-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel6ClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-pwcrack-level-6-cluster-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel6Cluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-pwcrack-level-6-cluster-costs-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel6ClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-pwcrack-level-6-cluster-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel6Cluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-pwcrack-level-6-cluster-costs-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel6ClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-pwcrack-level-6-cluster-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel6Cluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: Cluster, Costs, Version: 4 ------------
register(
    id='pycr-pwcrack-level-6-cluster-costs-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel6ClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

## Random

# -------- Difficulty Level: Random, Mode: Cluster, Version: Base ------------
register(
    id='pycr-pwcrack-random-cluster-base-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackRandomClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-pwcrack-random-cluster-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackRandomCluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-pwcrack-random-cluster-costs-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackRandomClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Version: 1 ------------
register(
    id='pycr-pwcrack-random-generated-sim-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackRandomGeneratedSim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Costs, Version: 1 ------------
register(
    id='pycr-pwcrack-random-generated-sim-costs-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackRandomGeneratedSim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-pwcrack-random-cluster-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackRandomCluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-pwcrack-random-cluster-costs-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackRandomClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Version: 2 ------------
register(
    id='pycr-pwcrack-random-generated-sim-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackRandomGeneratedSim2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Costs, Version: 2 ------------
register(
    id='pycr-pwcrack-random-generated-sim-costs-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackRandomGeneratedSim2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-pwcrack-random-cluster-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackRandomCluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-pwcrack-random-cluster-costs-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackRandomClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Version: 3 ------------
register(
    id='pycr-pwcrack-random-generated-sim-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackRandomGeneratedSim3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Costs, Version: 3 ------------
register(
    id='pycr-pwcrack-random-generated-sim-costs-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackRandomGeneratedSim3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-pwcrack-random-cluster-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackRandomCluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Cluster, Costs, Version: 4 ------------
register(
    id='pycr-pwcrack-random-cluster-costs-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackRandomClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Version: 4 ------------
register(
    id='pycr-pwcrack-random-generated-sim-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackRandomGeneratedSim4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Costs, Version: 4 ------------
register(
    id='pycr-pwcrack-random-generated-sim-costs-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackRandomGeneratedSim4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

## Random Many

# -------- Difficulty Level: Random Many, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-pwcrack-random-many-cluster-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackRandomManyCluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_configs": None, "flags_configs": None, "idx": None}
)

# -------- Difficulty Level: Random Many, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-pwcrack-random-many-cluster-costs-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackRandomManyClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_configs": None, "flags_configs": None, "idx": None}
)

# -------- Difficulty Level: Random Many, Mode: Generated Simulation, Version: 1 ------------
register(
    id='pycr-pwcrack-random-many-generated-sim-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackRandomManyGeneratedSim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "containers_configs": None, "flags_configs": None, "idx": None}
)

# -------- Difficulty Level: MultiSim, Mode: Multi-Simulation, Version: 1 ------------
register(
    id='pycr-pwcrack-multisim-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackMultiSim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None,
            "idx": None, "dr_max_num_nodes": int, "dr_min_num_nodes": int, "dr_max_num_flags": int,
            "dr_min_num_flags": int, "dr_min_num_users": int, "dr_max_num_users": int}
)

## Level 7

# -------- Difficulty Level: Level7, Mode: Cluster, Version: Base ------------
register(
    id='pycr-pwcrack-level-7-cluster-base-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel7ClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-pwcrack-level-7-cluster-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel7Cluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Costs, Version: 1 ------------
register(
    id='pycr-pwcrack-level-7-cluster-costs-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel7ClusterWithCosts1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-pwcrack-level-7-cluster-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel7Cluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Costs, Version: 2 ------------
register(
    id='pycr-pwcrack-level-7-cluster-costs-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel7ClusterWithCosts2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-pwcrack-level-7-cluster-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel7Cluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Costs, Version: 3 ------------
register(
    id='pycr-pwcrack-level-7-cluster-costs-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel7ClusterWithCosts3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-pwcrack-level-7-cluster-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel7Cluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: Cluster, Costs, Version: 4 ------------
register(
    id='pycr-pwcrack-level-7-cluster-costs-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackLevel7ClusterWithCosts4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)
