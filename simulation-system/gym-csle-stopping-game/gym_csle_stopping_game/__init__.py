"""
Register OpenAI Envs
"""
import gym
from gym.envs.registration import register

# -------- Difficulty Level: Level1, Mode: Simulation, Version: Base ------------
register(
    id='csle-ctf-level-1-sim-base-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.simulation.csle_ctf_level1_sim_env:CSLECTFLevel1SimBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)