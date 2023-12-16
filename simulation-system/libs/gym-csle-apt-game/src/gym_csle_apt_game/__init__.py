"""
Register OpenAI Envs
"""
from . __version__ import __version__
from gymnasium.envs.registration import register

register(
    id='csle-apt-game-v1',
    entry_point='gym_csle_apt_game.envs.apt_game_env:AptGameEnv',
    kwargs={'config': None}
)

register(
    id='csle-apt-game-mdp-attacker-v1',
    entry_point='gym_csle_apt_game.envs.apt_game_mdp_attacker_env:AptGameMdpAttackerEnv',
    kwargs={'config': None}
)

register(
    id='csle-apt-game-pomdp-defender-v1',
    entry_point='gym_csle_apt_game.envs.apt_game_pomdp_defender_env:AptGamePomdpDefenderEnv',
    kwargs={'config': None}
)