"""
Register OpenAI Envs
"""
from . __version__ import __version__
from gymnasium.envs.registration import register

register(
    id='csle-stopping-game-v1',
    entry_point='gym_csle_stopping_game.envs.stopping_game_env:StoppingGameEnv',
    kwargs={'config': None}
)

register(
    id='csle-stopping-game-mdp-attacker-v1',
    entry_point='gym_csle_stopping_game.envs.stopping_game_mdp_attacker_env:StoppingGameMdpAttackerEnv',
    kwargs={'config': None}
)

register(
    id='csle-stopping-game-pomdp-defender-v1',
    entry_point='gym_csle_stopping_game.envs.stopping_game_pomdp_defender_env:StoppingGamePomdpDefenderEnv',
    kwargs={'config': None}
)