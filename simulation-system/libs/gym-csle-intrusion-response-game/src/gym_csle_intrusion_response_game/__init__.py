"""
Register OpenAI Envs
"""
from . __version__ import __version__
from gym.envs.registration import register

register(
    id='csle-intrusion-response-game-pomdp-defender-v1',
    entry_point='gym_csle_intrusion_response_game.envs.intrusion_response_game_local_pomdp_defender:'
                'IntrusionResponseGameLocalPOMDPDefenderEnv',
    kwargs={'config': None}
)