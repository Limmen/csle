"""
Register OpenAI Envs
"""
import gym
from gym.envs.registration import register

# -------- Difficulty Level: Level1, Mode: Simulation, Version: Base ------------
register(
    id='pycr-ctf-level-1-sim-base-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env:PyCRCTFLevel1SimBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: emulation, Version: Base ------------
register(
    id='pycr-ctf-level-1-emulation-base-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.emulation.pycr_ctf_level1_emulation_env:PyCRCTFLevel1EmulationBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Version: 1 ------------
register(
    id='pycr-ctf-level-1-sim-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env:PyCRCTFLevel1Sim1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-1-sim-costs-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env:PyCRCTFLevel1SimWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: emulation, Version: 1 ------------
register(
    id='pycr-ctf-level-1-emulation-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.emulation.pycr_ctf_level1_emulation_env:PyCRCTFLevel1Emulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: emulation, No Cache Version: 1 ------------
register(
    id='pycr-ctf-level-1-emulation-nocache-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.emulation.pycr_ctf_level1_emulation_env:PyCRCTFLevel1EmulationNoCache1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: emulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-1-emulation-costs-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.emulation.pycr_ctf_level1_emulation_env:PyCRCTFLevel1EmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Version: 1 ------------
register(
    id='pycr-ctf-level-1-generated-sim-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.generated_simulation.pycr_ctf_level1_gensim_env:PyCRCTFLevel1GeneratedSim1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-1-generated-sim-costs-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.generated_simulation.pycr_ctf_level1_gensim_env:PyCRCTFLevel1GeneratedSimWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Version: 2 ------------
register(
    id='pycr-ctf-level-1-sim-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env:PyCRCTFLevel1Sim2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-1-sim-costs-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env:PyCRCTFLevel1SimWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: emulation, Version: 2 ------------
register(
    id='pycr-ctf-level-1-emulation-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.emulation.pycr_ctf_level1_emulation_env:PyCRCTFLevel1Emulation2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: emulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-1-emulation-costs-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.emulation.pycr_ctf_level1_emulation_env:PyCRCTFLevel1EmulationWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Version: 2 ------------
register(
    id='pycr-ctf-level-1-generated-sim-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.generated_simulation.pycr_ctf_level1_gensim_env:PyCRCTFLevel1GeneratedSim2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-1-generated-sim-costs-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.generated_simulation.pycr_ctf_level1_gensim_env:PyCRCTFLevel1GeneratedSimWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Version: 3 ------------
register(
    id='pycr-ctf-level-1-sim-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env:PyCRCTFLevel1Sim3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, costs, Version: 3 ------------
register(
    id='pycr-ctf-level-1-sim-costs-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env:PyCRCTFLevel1SimWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Version: 3 ------------
register(
    id='pycr-ctf-level-1-generated-sim-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.generated_simulation.pycr_ctf_level1_gensim_env:PyCRCTFLevel1GeneratedSim3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-1-generated-sim-costs-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.generated_simulation.pycr_ctf_level1_gensim_env:PyCRCTFLevel1GeneratedSimWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: emulation, Version: 3 ------------
register(
    id='pycr-ctf-level-1-emulation-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.emulation.pycr_ctf_level1_emulation_env:PyCRCTFLevel1Emulation3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: emulation, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-1-emulation-costs-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.emulation.pycr_ctf_level1_emulation_env:PyCRCTFLevel1EmulationWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Version: 4 ------------
register(
    id='pycr-ctf-level-1-sim-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env:PyCRCTFLevel1Sim4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-1-sim-costs-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env:PyCRCTFLevel1SimWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Version: 4 ------------
register(
    id='pycr-ctf-level-1-generated-sim-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.generated_simulation.pycr_ctf_level1_gensim_env:PyCRCTFLevel1GeneratedSim4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-1-generated-sim-costs-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.generated_simulation.pycr_ctf_level1_gensim_env:PyCRCTFLevel1GeneratedSimWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: emulation, Version: 4 ------------
register(
    id='pycr-ctf-level-1-emulation-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.emulation.pycr_ctf_level1_emulation_env:PyCRCTFLevel1Emulation4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: emulation, Version: 4 ------------
register(
    id='pycr-ctf-level-1-emulation-costs-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level1.emulation.pycr_ctf_level1_emulation_env:PyCRCTFLevel1EmulationWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Simulation, Version: Base ------------
register(
    id='pycr-ctf-level-2-sim-base-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level2.simulation.pycr_ctf_level2_sim_env:PyCRCTFLevel2SimBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: emulation, Version: Base ------------
register(
    id='pycr-ctf-level-2-emulation-base-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level2.emulation.pycr_ctf_level2_emulation_env:PyCRCTFLevel2EmulationBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: emulation, Version: 1 ------------
register(
    id='pycr-ctf-level-2-emulation-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level2.emulation.pycr_ctf_level2_emulation_env:PyCRCTFLevel2Emulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: emulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-2-emulation-costs-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level2.emulation.pycr_ctf_level2_emulation_env:PyCRCTFLevel2EmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: emulation, Version: 2 ------------
register(
    id='pycr-ctf-level-2-emulation-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level2.emulation.pycr_ctf_level2_emulation_env:PyCRCTFLevel2Emulation2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: emulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-2-emulation-costs-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level2.emulation.pycr_ctf_level2_emulation_env:PyCRCTFLevel2EmulationWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: emulation, Version: 3 ------------
register(
    id='pycr-ctf-level-2-emulation-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level2.emulation.pycr_ctf_level2_emulation_env:PyCRCTFLevel2Emulation3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: emulation, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-2-emulation-costs-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level2.emulation.pycr_ctf_level2_emulation_env:PyCRCTFLevel2EmulationWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: emulation, Version: 4 ------------
register(
    id='pycr-ctf-level-2-emulation-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level2.emulation.pycr_ctf_level2_emulation_env:PyCRCTFLevel2Emulation4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: emulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-2-emulation-costs-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level2.emulation.pycr_ctf_level2_emulation_env:PyCRCTFLevel2EmulationWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Version: 1 ------------
register(
    id='pycr-ctf-level-2-generated-sim-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level2.generated_simulation.pycr_ctf_level2_gensim_env:PyCRCTFLevel2GeneratedSim1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-2-generated-sim-costs-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level2.generated_simulation.pycr_ctf_level2_gensim_env:PyCRCTFLevel2GeneratedSimWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Simulation, Version: 1 ------------
register(
    id='pycr-ctf-level-2-sim-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level2.simulation.pycr_ctf_level2_sim_env:PyCRCTFLevel2Sim1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Simulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-2-sim-costs-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level2.simulation.pycr_ctf_level2_sim_env:PyCRCTFLevel2SimWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: emulation, Version: Base ------------
register(
    id='pycr-ctf-level-3-emulation-base-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level3.emulation.pycr_ctf_level3_emulation_env:PyCRCTFLevel3EmulationBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: emulation, Version: 1 ------------
register(
    id='pycr-ctf-level-3-emulation-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level3.emulation.pycr_ctf_level3_emulation_env:PyCRCTFLevel3Emulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: emulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-3-emulation-costs-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level3.emulation.pycr_ctf_level3_emulation_env:PyCRCTFLevel3EmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Version: 2 ------------
register(
    id='pycr-ctf-level-2-generated-sim-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level2.generated_simulation.pycr_ctf_level2_gensim_env:PyCRCTFLevel2GeneratedSim2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-2-generated-sim-costs-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level2.generated_simulation.pycr_ctf_level2_gensim_env:PyCRCTFLevel2GeneratedSimWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: emulation, Version: 2 ------------
register(
    id='pycr-ctf-level-3-emulation-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level3.emulation.pycr_ctf_level3_emulation_env:PyCRCTFLevel3Emulation2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: emulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-3-emulation-costs-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level3.emulation.pycr_ctf_level3_emulation_env:PyCRCTFLevel3EmulationWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Version: 3 ------------
register(
    id='pycr-ctf-level-2-generated-sim-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level2.generated_simulation.pycr_ctf_level2_gensim_env:PyCRCTFLevel2GeneratedSim3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-2-generated-sim-costs-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level2.generated_simulation.pycr_ctf_level2_gensim_env:PyCRCTFLevel2GeneratedSimWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: emulation, Version: 3 ------------
register(
    id='pycr-ctf-level-3-emulation-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level3.emulation.pycr_ctf_level3_emulation_env:PyCRCTFLevel3Emulation3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: emulation, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-3-emulation-costs-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level3.emulation.pycr_ctf_level3_emulation_env:PyCRCTFLevel3EmulationWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Version: 4 ------------
register(
    id='pycr-ctf-level-2-generated-sim-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level2.generated_simulation.pycr_ctf_level2_gensim_env:PyCRCTFLevel2GeneratedSim4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-2-generated-sim-costs-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level2.generated_simulation.pycr_ctf_level2_gensim_env:PyCRCTFLevel2GeneratedSimWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: emulation, Version: 4 ------------
register(
    id='pycr-ctf-level-3-emulation-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level3.emulation.pycr_ctf_level3_emulation_env:PyCRCTFLevel3Emulation4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: emulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-3-emulation-costs-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level3.emulation.pycr_ctf_level3_emulation_env:PyCRCTFLevel3EmulationWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

## Level 4

# -------- Difficulty Level: Level4, Mode: emulation, Version: Base ------------
register(
    id='pycr-ctf-level-4-emulation-base-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level4.emulation.pycr_ctf_level4_emulation_env:PyCRCTFLevel4EmulationBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: emulation, Version: 1 ------------
register(
    id='pycr-ctf-level-4-emulation-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level4.emulation.pycr_ctf_level4_emulation_env:PyCRCTFLevel4Emulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: emulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-4-emulation-costs-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level4.emulation.pycr_ctf_level4_emulation_env:PyCRCTFLevel4EmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: emulation, Version: 2 ------------
register(
    id='pycr-ctf-level-4-emulation-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level4.emulation.pycr_ctf_level4_emulation_env:PyCRCTFLevel4Emulation2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: emulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-4-emulation-costs-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level4.emulation.pycr_ctf_level4_emulation_env:PyCRCTFLevel4EmulationWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: emulation, Version: 3 ------------
register(
    id='pycr-ctf-level-4-emulation-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level4.emulation.pycr_ctf_level4_emulation_env:PyCRCTFLevel4Emulation3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: emulation, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-4-emulation-costs-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level4.emulation.pycr_ctf_level4_emulation_env:PyCRCTFLevel4EmulationWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: emulation, Version: 4 ------------
register(
    id='pycr-ctf-level-4-emulation-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level4.emulation.pycr_ctf_level4_emulation_env:PyCRCTFLevel4Emulation4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: emulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-4-emulation-costs-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level4.emulation.pycr_ctf_level4_emulation_env:PyCRCTFLevel4EmulationWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Generated Simulation, Version: 4 ------------
register(
    id='pycr-ctf-level-4-generated-sim-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level4.generated_simulation.pycr_ctf_level4_gensim_env:PyCRCTFLevel4GeneratedSim1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Generated Simulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-4-generated-sim-costs-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level4.generated_simulation.pycr_ctf_level4_gensim_env:PyCRCTFLevel4GeneratedSimWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Generated Simulation, Version: 2 ------------
register(
    id='pycr-ctf-level-4-generated-sim-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level4.generated_simulation.pycr_ctf_level4_gensim_env:PyCRCTFLevel4GeneratedSim2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Generated Simulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-4-generated-sim-costs-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level4.generated_simulation.pycr_ctf_level4_gensim_env:PyCRCTFLevel4GeneratedSimWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Generated Simulation, Version: 3 ------------
register(
    id='pycr-ctf-level-4-generated-sim-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level4.generated_simulation.pycr_ctf_level4_gensim_env:PyCRCTFLevel4GeneratedSim3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Generated Simulation, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-4-generated-sim-costs-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level4.generated_simulation.pycr_ctf_level4_gensim_env:PyCRCTFLevel4GeneratedSimWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Generated Simulation, Version: 4 ------------
register(
    id='pycr-ctf-level-4-generated-sim-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level4.generated_simulation.pycr_ctf_level4_gensim_env:PyCRCTFLevel4GeneratedSim4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Generated Simulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-4-generated-sim-costs-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level4.generated_simulation.pycr_ctf_level4_gensim_env:PyCRCTFLevel4GeneratedSimWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: emulation, Version: 5 ------------
register(
    id='pycr-ctf-level-4-emulation-v5',
    entry_point='gym_pycr_ctf.envs.derived_envs.level4.emulation.pycr_ctf_level4_emulation_env:PyCRCTFLevel4Emulation5Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Generated Simulation, Version: 5 ------------
register(
    id='pycr-ctf-level-4-generated-sim-v5',
    entry_point='gym_pycr_ctf.envs.derived_envs.level4.generated_simulation.pycr_ctf_level4_gensim_env:PyCRCTFLevel4GeneratedSim5Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

## Level 5

# -------- Difficulty Level: Level5, Mode: emulation, Version: Base ------------
register(
    id='pycr-ctf-level-5-emulation-base-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level5.emulation.pycr_ctf_level5_emulation_env:PyCRCTFLevel5EmulationBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: emulation, Version: 1 ------------
register(
    id='pycr-ctf-level-5-emulation-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level5.emulation.pycr_ctf_level5_emulation_env:PyCRCTFLevel5Emulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: emulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-5-emulation-costs-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level5.emulation.pycr_ctf_level5_emulation_env:PyCRCTFLevel5EmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: emulation, Version: 2 ------------
register(
    id='pycr-ctf-level-5-emulation-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level5.emulation.pycr_ctf_level5_emulation_env:PyCRCTFLevel5Emulation2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: emulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-5-emulation-costs-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level5.emulation.pycr_ctf_level5_emulation_env:PyCRCTFLevel5EmulationWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: emulation, Version: 3 ------------
register(
    id='pycr-ctf-level-5-emulation-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level5.emulation.pycr_ctf_level5_emulation_env:PyCRCTFLevel5Emulation3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: emulation, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-5-emulation-costs-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level5.emulation.pycr_ctf_level5_emulation_env:PyCRCTFLevel5EmulationWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: emulation, Version: 4 ------------
register(
    id='pycr-ctf-level-5-emulation-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level5.emulation.pycr_ctf_level5_emulation_env:PyCRCTFLevel5Emulation4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: emulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-5-emulation-costs-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level5.emulation.pycr_ctf_level5_emulation_env:PyCRCTFLevel5EmulationWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

## Level 6

# -------- Difficulty Level: Level6, Mode: emulation, Version: Base ------------
register(
    id='pycr-ctf-level-6-emulation-base-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level6.emulation.pycr_ctf_level6_emulation_env:PyCRCTFLevel6EmulationBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: emulation, Version: 1 ------------
register(
    id='pycr-ctf-level-6-emulation-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level6.emulation.pycr_ctf_level6_emulation_env:PyCRCTFLevel6Emulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: emulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-6-emulation-costs-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level6.emulation.pycr_ctf_level6_emulation_env:PyCRCTFLevel6EmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: emulation, Version: 2 ------------
register(
    id='pycr-ctf-level-6-emulation-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level6.emulation.pycr_ctf_level6_emulation_env:PyCRCTFLevel6Emulation2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: emulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-6-emulation-costs-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level6.emulation.pycr_ctf_level6_emulation_env:PyCRCTFLevel6EmulationWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: emulation, Version: 3 ------------
register(
    id='pycr-ctf-level-6-emulation-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level6.emulation.pycr_ctf_level6_emulation_env:PyCRCTFLevel6Emulation3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: emulation, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-6-emulation-costs-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level6.emulation.pycr_ctf_level6_emulation_env:PyCRCTFLevel6EmulationWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: emulation, Version: 4 ------------
register(
    id='pycr-ctf-level-6-emulation-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level6.emulation.pycr_ctf_level6_emulation_env:PyCRCTFLevel6Emulation4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: emulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-6-emulation-costs-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level6.emulation.pycr_ctf_level6_emulation_env:PyCRCTFLevel6EmulationWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

## Random

# -------- Difficulty Level: Random, Mode: emulation, Version: Base ------------
register(
    id='pycr-ctf-random-emulation-base-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.random.emulation.pycr_ctf_random_emulation_env:PyCRCTFRandomEmulationBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: emulation, Version: 1 ------------
register(
    id='pycr-ctf-random-emulation-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.random.emulation.pycr_ctf_random_emulation_env:PyCRCTFRandomEmulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: emulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-random-emulation-costs-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.random.emulation.pycr_ctf_random_emulation_env:PyCRCTFRandomEmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Version: 1 ------------
register(
    id='pycr-ctf-random-generated-sim-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.random.generated_simulation.pycr_ctf_random_gensim_env:PyCRCTFRandomGeneratedSim1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-random-generated-sim-costs-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.random.generated_simulation.pycr_ctf_random_gensim_env:PyCRCTFRandomGeneratedSim1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: emulation, Version: 2 ------------
register(
    id='pycr-ctf-random-emulation-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.random.emulation.pycr_ctf_random_emulation_env:PyCRCTFRandomEmulation2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: emulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-random-emulation-costs-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.random.emulation.pycr_ctf_random_emulation_env:PyCRCTFRandomEmulationWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Version: 2 ------------
register(
    id='pycr-ctf-random-generated-sim-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.random.generated_simulation.pycr_ctf_random_gensim_env:PyCRCTFRandomGeneratedSim2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-random-generated-sim-costs-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.random.generated_simulation.pycr_ctf_random_gensim_env:PyCRCTFRandomGeneratedSim2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: emulation, Version: 3 ------------
register(
    id='pycr-ctf-random-emulation-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.random.emulation.pycr_ctf_random_emulation_env:PyCRCTFRandomEmulation3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: emulation, Costs, Version: 3 ------------
register(
    id='pycr-ctf-random-emulation-costs-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.random.emulation.pycr_ctf_random_emulation_env:PyCRCTFRandomEmulationWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Version: 3 ------------
register(
    id='pycr-ctf-random-generated-sim-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.random.generated_simulation.pycr_ctf_random_gensim_env:PyCRCTFRandomGeneratedSim3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Costs, Version: 3 ------------
register(
    id='pycr-ctf-random-generated-sim-costs-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.random.generated_simulation.pycr_ctf_random_gensim_env:PyCRCTFRandomGeneratedSim3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: emulation, Version: 4 ------------
register(
    id='pycr-ctf-random-emulation-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.random.emulation.pycr_ctf_random_emulation_env:PyCRCTFRandomEmulation4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: emulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-random-emulation-costs-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.random.emulation.pycr_ctf_random_emulation_env:PyCRCTFRandomEmulationWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Version: 4 ------------
register(
    id='pycr-ctf-random-generated-sim-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.random.generated_simulation.pycr_ctf_random_gensim_env:PyCRCTFRandomGeneratedSim4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-random-generated-sim-costs-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.random.generated_simulation.pycr_ctf_random_gensim_env:PyCRCTFRandomGeneratedSim4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

## Random Many

# -------- Difficulty Level: Random Many, Mode: emulation, Version: 1 ------------
register(
    id='pycr-ctf-random-many-emulation-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.random_many.emulation.pycr_ctf_random_many_emulation_env:PyCRCTFRandomManyEmulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_configs": None, "flags_configs": None, "idx": None}
)

# -------- Difficulty Level: Random Many, Mode: emulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-random-many-emulation-costs-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.random_many.emulation.pycr_ctf_random_many_emulation_env:PyCRCTFRandomManyEmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_configs": None, "flags_configs": None, "idx": None}
)

# -------- Difficulty Level: Random Many, Mode: Generated Simulation, Version: 1 ------------
register(
    id='pycr-ctf-random-many-generated-sim-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.random_many.generated_simulation.pycr_ctf_random_many_gensim_env:PyCRCTFRandomManyGeneratedSim1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_configs": None, "flags_configs": None, "idx": None}
)

## MultiSim

# -------- Difficulty Level: MultiSim, Mode: Multi-Simulation, Version: 1 ------------
register(
    id='pycr-ctf-multisim-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.multisim.pycr_ctf_multisim_env:PyCRCTFMultiSim1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "idx": None, "dr_max_num_nodes": int, "dr_min_num_nodes": int, "dr_max_num_flags": int,
            "dr_min_num_flags": int, "dr_min_num_users": int, "dr_max_num_users": int}
)

## Level 7

# -------- Difficulty Level: Level7, Mode: emulation, Version: Base ------------
register(
    id='pycr-ctf-level-7-emulation-base-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level7.emulation.pycr_ctf_level7_emulation_env:PyCRCTFLevel7EmulationBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: emulation, Version: 1 ------------
register(
    id='pycr-ctf-level-7-emulation-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level7.emulation.pycr_ctf_level7_emulation_env:PyCRCTFLevel7Emulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: emulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-7-emulation-costs-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level7.emulation.pycr_ctf_level7_emulation_env:PyCRCTFLevel7EmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: emulation, Version: 2 ------------
register(
    id='pycr-ctf-level-7-emulation-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level7.emulation.pycr_ctf_level7_emulation_env:PyCRCTFLevel7Emulation2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: emulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-7-emulation-costs-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level7.emulation.pycr_ctf_level7_emulation_env:PyCRCTFLevel7EmulationWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: emulation, Version: 3 ------------
register(
    id='pycr-ctf-level-7-emulation-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level7.emulation.pycr_ctf_level7_emulation_env:PyCRCTFLevel7Emulation3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: emulation, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-7-emulation-costs-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level7.emulation.pycr_ctf_level7_emulation_env:PyCRCTFLevel7EmulationWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: emulation, Version: 4 ------------
register(
    id='pycr-ctf-level-7-emulation-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level7.emulation.pycr_ctf_level7_emulation_env:PyCRCTFLevel7Emulation4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: emulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-7-emulation-costs-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level7.emulation.pycr_ctf_level7_emulation_env:PyCRCTFLevel7EmulationWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

## Level 8

# -------- Difficulty Level: Level8, Mode: emulation, Version: Base ------------
register(
    id='pycr-ctf-level-8-emulation-base-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level8.emulation.pycr_ctf_level8_emulation_env:PyCRCTFLevel8EmulationBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level8, Mode: emulation, Version: 1 ------------
register(
    id='pycr-ctf-level-8-emulation-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level8.emulation.pycr_ctf_level8_emulation_env:PyCRCTFLevel8Emulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level8, Mode: emulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-8-emulation-costs-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level8.emulation.pycr_ctf_level8_emulation_env:PyCRCTFLevel8EmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level8, Mode: emulation, Version: 2 ------------
register(
    id='pycr-ctf-level-8-emulation-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level8.emulation.pycr_ctf_level8_emulation_env:PyCRCTFLevel8Emulation2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level8, Mode: emulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-8-emulation-costs-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level8.emulation.pycr_ctf_level8_emulation_env:PyCRCTFLevel8EmulationWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level8, Mode: emulation, Version: 3 ------------
register(
    id='pycr-ctf-level-8-emulation-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level8.emulation.pycr_ctf_level8_emulation_env:PyCRCTFLevel8Emulation3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level8, Mode: emulation, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-8-emulation-costs-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level8.emulation.pycr_ctf_level8_emulation_env:PyCRCTFLevel8EmulationWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level8, Mode: emulation, Version: 4 ------------
register(
    id='pycr-ctf-level-8-emulation-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level8.emulation.pycr_ctf_level8_emulation_env:PyCRCTFLevel8Emulation4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level8, Mode: emulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-8-emulation-costs-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level8.emulation.pycr_ctf_level8_emulation_env:PyCRCTFLevel8EmulationWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)


## Level 9

# -------- Difficulty Level: Level9, Mode: emulation, Version: Base ------------
register(
    id='pycr-ctf-level-9-emulation-base-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level9.emulation.pycr_ctf_level9_emulation_env:PyCRCTFLevel9EmulationBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: emulation, Version: 1 ------------
register(
    id='pycr-ctf-level-9-emulation-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level9.emulation.pycr_ctf_level9_emulation_env:PyCRCTFLevel9Emulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: emulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-9-emulation-costs-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level9.emulation.pycr_ctf_level9_emulation_env:PyCRCTFLevel9EmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: emulation, Version: 2 ------------
register(
    id='pycr-ctf-level-9-emulation-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level9.emulation.pycr_ctf_level9_emulation_env:PyCRCTFLevel9Emulation2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: emulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-9-emulation-costs-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level9.emulation.pycr_ctf_level9_emulation_env:PyCRCTFLevel9EmulationWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: emulation, Version: 3 ------------
register(
    id='pycr-ctf-level-9-emulation-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level9.emulation.pycr_ctf_level9_emulation_env:PyCRCTFLevel9Emulation3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: emulation, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-9-emulation-costs-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level9.emulation.pycr_ctf_level9_emulation_env:PyCRCTFLevel9EmulationWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: emulation, Version: 4 ------------
register(
    id='pycr-ctf-level-9-emulation-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level9.emulation.pycr_ctf_level9_emulation_env:PyCRCTFLevel9Emulation4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: emulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-9-emulation-costs-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level9.emulation.pycr_ctf_level9_emulation_env:PyCRCTFLevel9EmulationWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: emulation, Version: 5 ------------
register(
    id='pycr-ctf-level-9-emulation-v5',
    entry_point='gym_pycr_ctf.envs.derived_envs.level9.emulation.pycr_ctf_level9_emulation_env:PyCRCTFLevel9Emulation5Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: emulation, Version: 5 ------------
register(
    id='pycr-ctf-level-9-emulation-v6',
    entry_point='gym_pycr_ctf.envs.derived_envs.level9.emulation.pycr_ctf_level9_emulation_env:PyCRCTFLevel9Emulation6Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: Generated Simulation, Version: 1 ------------
register(
    id='pycr-ctf-level-9-generated-sim-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level9.generated_simulation.pycr_ctf_level9_gensim_env:PyCRCTFLevel9GeneratedSim1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: Generated Simulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-9-generated-sim-costs-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level9.generated_simulation.pycr_ctf_level9_gensim_env:PyCRCTFLevel9GeneratedSimWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: Generated Simulation, Version: 2 ------------
register(
    id='pycr-ctf-level-9-generated-sim-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level9.generated_simulation.pycr_ctf_level9_gensim_env:PyCRCTFLevel9GeneratedSim2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: Generated Simulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-9-generated-sim-costs-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level9.generated_simulation.pycr_ctf_level9_gensim_env:PyCRCTFLevel9GeneratedSimWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: Generated Simulation, Version: 3 ------------
register(
    id='pycr-ctf-level-9-generated-sim-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level9.generated_simulation.pycr_ctf_level9_gensim_env:PyCRCTFLevel9GeneratedSim3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: Generated Simulation, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-9-generated-sim-costs-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level9.generated_simulation.pycr_ctf_level9_gensim_env:PyCRCTFLevel9GeneratedSimWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: Generated Simulation, Version: 4 ------------
register(
    id='pycr-ctf-level-9-generated-sim-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level9.generated_simulation.pycr_ctf_level9_gensim_env:PyCRCTFLevel9GeneratedSim4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: Generated Simulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-9-generated-sim-costs-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level9.generated_simulation.pycr_ctf_level9_gensim_env:PyCRCTFLevel9GeneratedSimWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: Generated Simulation, Version: 5 ------------
register(
    id='pycr-ctf-level-9-generated-sim-v5',
    entry_point='gym_pycr_ctf.envs.derived_envs.level9.generated_simulation.pycr_ctf_level9_gensim_env:PyCRCTFLevel9GeneratedSim5Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: Generated Simulation, Version: 6 ------------
register(
    id='pycr-ctf-level-9-generated-sim-v6',
    entry_point='gym_pycr_ctf.envs.derived_envs.level9.generated_simulation.pycr_ctf_level9_gensim_env:PyCRCTFLevel9GeneratedSim6Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)


## Level 10

# -------- Difficulty Level: Level10, Mode: emulation, Version: Base ------------
register(
    id='pycr-ctf-level-10-emulation-base-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level10.emulation.pycr_ctf_level10_emulation_env:PyCRCTFLevel10EmulationBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level10, Mode: emulation, Version: 1 ------------
register(
    id='pycr-ctf-level-10-emulation-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level10.emulation.pycr_ctf_level10_emulation_env:PyCRCTFLevel10Emulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level10, Mode: emulation, Costs, Version: 1 ------------
register(
    id='pycr-ctf-level-10-emulation-costs-v1',
    entry_point='gym_pycr_ctf.envs.derived_envs.level10.emulation.pycr_ctf_level10_emulation_env:PyCRCTFLevel10EmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level10, Mode: emulation, Version: 2 ------------
register(
    id='pycr-ctf-level-10-emulation-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level10.emulation.pycr_ctf_level10_emulation_env:PyCRCTFLevel10Emulation2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level10, Mode: emulation, Costs, Version: 2 ------------
register(
    id='pycr-ctf-level-10-emulation-costs-v2',
    entry_point='gym_pycr_ctf.envs.derived_envs.level10.emulation.pycr_ctf_level10_emulation_env:PyCRCTFLevel10EmulationWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level10, Mode: emulation, Version: 3 ------------
register(
    id='pycr-ctf-level-10-emulation-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level10.emulation.pycr_ctf_level10_emulation_env:PyCRCTFLevel10Emulation3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level10, Mode: emulation, Costs, Version: 3 ------------
register(
    id='pycr-ctf-level-10-emulation-costs-v3',
    entry_point='gym_pycr_ctf.envs.derived_envs.level10.emulation.pycr_ctf_level10_emulation_env:PyCRCTFLevel10EmulationWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level10, Mode: emulation, Version: 4 ------------
register(
    id='pycr-ctf-level-10-emulation-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level10.emulation.pycr_ctf_level10_emulation_env:PyCRCTFLevel10Emulation4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level10, Mode: emulation, Costs, Version: 4 ------------
register(
    id='pycr-ctf-level-10-emulation-costs-v4',
    entry_point='gym_pycr_ctf.envs.derived_envs.level10.emulation.pycr_ctf_level10_emulation_env:PyCRCTFLevel10EmulationWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)