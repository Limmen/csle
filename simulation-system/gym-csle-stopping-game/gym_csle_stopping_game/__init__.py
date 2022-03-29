"""
Register OpenAI Envs
"""
import gym
from gym.envs.registration import register

register(
    id='csle-stopping-game-v1',
    entry_point='gym_csle_stopping_game.envs.stopping_game_env:StoppingGameEnv',
    kwargs={'config': None}
)

register(
    id='csle-stopping-game-attacker-mdp-v1',
    entry_point='gym_csle_stopping_game.envs.stopping_game_mdp_attacker_env:StoppingGameMdpAttackerEnv',
    kwargs={'config': None}
)