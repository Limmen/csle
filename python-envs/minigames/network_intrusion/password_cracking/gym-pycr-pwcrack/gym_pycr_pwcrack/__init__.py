"""
Register OpenAI Envs
"""
from gym.envs.registration import register

# -------- Difficulty Level: Simple, Version 1 ------------
register(
    id='pycr-pwcrack-simple-sim-v1',
    entry_point='gym_pycr_pwcrack.envs:PyCRPwCrackSimpleSim1Env',
    kwargs={'env_config': None}
)