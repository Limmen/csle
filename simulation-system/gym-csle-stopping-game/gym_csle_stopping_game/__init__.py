"""
Register OpenAI Envs
"""
import gym
from gym.envs.registration import register

# -------- Difficulty Level: Level1, Mode: Simulation, Version: Base ------------
register(
    id='csle-stopping-game-v1',
    entry_point='gym_csle_stopping_game.envs.stopping_game_env:StoppingGameEnv',
    kwargs={'stopping_game_config': None}
)