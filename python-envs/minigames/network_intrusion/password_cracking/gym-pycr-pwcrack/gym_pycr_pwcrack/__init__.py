"""
Register OpenAI Envs
"""
from gym.envs.registration import register

# -------- Version 1 ------------
register(
    id='cgc-bta-v1',
    entry_point='gym_pycr_pwcrack.envs:TODO',
    kwargs={'config': None}
)