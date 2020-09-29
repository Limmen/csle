"""
Register OpenAI Envs
"""
from gym.envs.registration import register

# -------- Difficulty Level: Simple, Mode: Simulation, Version: 1 ------------
register(
    id='pycr-pwcrack-simple-sim-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackSimpleSim1Env',
    kwargs={'env_config': None, 'cluster_config': None}
)

# -------- Difficulty Level: Simple, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-pwcrack-simple-cluster-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackSimpleCluster1Env',
    kwargs={'env_config': None, 'cluster_config': None}
)