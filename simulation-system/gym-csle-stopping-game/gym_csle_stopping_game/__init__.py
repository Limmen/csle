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

# -------- Difficulty Level: Level1, Mode: emulation, Version: Base ------------
register(
    id='csle-ctf-level-1-emulation-base-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.emulation.csle_ctf_level1_emulation_env:CSLECTFLevel1EmulationBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Version: 1 ------------
register(
    id='csle-ctf-level-1-sim-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.simulation.csle_ctf_level1_sim_env:CSLECTFLevel1Sim1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Costs, Version: 1 ------------
register(
    id='csle-ctf-level-1-sim-costs-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.simulation.csle_ctf_level1_sim_env:CSLECTFLevel1SimWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: emulation, Version: 1 ------------
register(
    id='csle-ctf-level-1-emulation-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.emulation.csle_ctf_level1_emulation_env:CSLECTFLevel1Emulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: emulation, No Cache Version: 1 ------------
register(
    id='csle-ctf-level-1-emulation-nocache-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.emulation.csle_ctf_level1_emulation_env:CSLECTFLevel1EmulationNoCache1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: emulation, Costs, Version: 1 ------------
register(
    id='csle-ctf-level-1-emulation-costs-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.emulation.csle_ctf_level1_emulation_env:CSLECTFLevel1EmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Version: 1 ------------
register(
    id='csle-ctf-level-1-generated-sim-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.generated_simulation.csle_ctf_level1_gensim_env:CSLECTFLevel1GeneratedSim1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Costs, Version: 1 ------------
register(
    id='csle-ctf-level-1-generated-sim-costs-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.generated_simulation.csle_ctf_level1_gensim_env:CSLECTFLevel1GeneratedSimWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Version: 2 ------------
register(
    id='csle-ctf-level-1-sim-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.simulation.csle_ctf_level1_sim_env:CSLECTFLevel1Sim2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Costs, Version: 2 ------------
register(
    id='csle-ctf-level-1-sim-costs-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.simulation.csle_ctf_level1_sim_env:CSLECTFLevel1SimWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: emulation, Version: 2 ------------
register(
    id='csle-ctf-level-1-emulation-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.emulation.csle_ctf_level1_emulation_env:CSLECTFLevel1Emulation2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: emulation, Costs, Version: 2 ------------
register(
    id='csle-ctf-level-1-emulation-costs-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.emulation.csle_ctf_level1_emulation_env:CSLECTFLevel1EmulationWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Version: 2 ------------
register(
    id='csle-ctf-level-1-generated-sim-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.generated_simulation.csle_ctf_level1_gensim_env:CSLECTFLevel1GeneratedSim2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Costs, Version: 2 ------------
register(
    id='csle-ctf-level-1-generated-sim-costs-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.generated_simulation.csle_ctf_level1_gensim_env:CSLECTFLevel1GeneratedSimWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Version: 3 ------------
register(
    id='csle-ctf-level-1-sim-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.simulation.csle_ctf_level1_sim_env:CSLECTFLevel1Sim3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, costs, Version: 3 ------------
register(
    id='csle-ctf-level-1-sim-costs-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.simulation.csle_ctf_level1_sim_env:CSLECTFLevel1SimWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Version: 3 ------------
register(
    id='csle-ctf-level-1-generated-sim-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.generated_simulation.csle_ctf_level1_gensim_env:CSLECTFLevel1GeneratedSim3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Costs, Version: 3 ------------
register(
    id='csle-ctf-level-1-generated-sim-costs-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.generated_simulation.csle_ctf_level1_gensim_env:CSLECTFLevel1GeneratedSimWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: emulation, Version: 3 ------------
register(
    id='csle-ctf-level-1-emulation-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.emulation.csle_ctf_level1_emulation_env:CSLECTFLevel1Emulation3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: emulation, Costs, Version: 3 ------------
register(
    id='csle-ctf-level-1-emulation-costs-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.emulation.csle_ctf_level1_emulation_env:CSLECTFLevel1EmulationWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Version: 4 ------------
register(
    id='csle-ctf-level-1-sim-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.simulation.csle_ctf_level1_sim_env:CSLECTFLevel1Sim4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Simulation, Costs, Version: 4 ------------
register(
    id='csle-ctf-level-1-sim-costs-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.simulation.csle_ctf_level1_sim_env:CSLECTFLevel1SimWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Version: 4 ------------
register(
    id='csle-ctf-level-1-generated-sim-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.generated_simulation.csle_ctf_level1_gensim_env:CSLECTFLevel1GeneratedSim4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: Generated Simulation, Costs, Version: 4 ------------
register(
    id='csle-ctf-level-1-generated-sim-costs-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.generated_simulation.csle_ctf_level1_gensim_env:CSLECTFLevel1GeneratedSimWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: emulation, Version: 4 ------------
register(
    id='csle-ctf-level-1-emulation-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.emulation.csle_ctf_level1_emulation_env:CSLECTFLevel1Emulation4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level1, Mode: emulation, Version: 4 ------------
register(
    id='csle-ctf-level-1-emulation-costs-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level1.emulation.csle_ctf_level1_emulation_env:CSLECTFLevel1EmulationWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Simulation, Version: Base ------------
register(
    id='csle-ctf-level-2-sim-base-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level2.simulation.csle_ctf_level2_sim_env:CSLECTFLevel2SimBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: emulation, Version: Base ------------
register(
    id='csle-ctf-level-2-emulation-base-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level2.emulation.csle_ctf_level2_emulation_env:CSLECTFLevel2EmulationBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: emulation, Version: 1 ------------
register(
    id='csle-ctf-level-2-emulation-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level2.emulation.csle_ctf_level2_emulation_env:CSLECTFLevel2Emulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: emulation, Costs, Version: 1 ------------
register(
    id='csle-ctf-level-2-emulation-costs-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level2.emulation.csle_ctf_level2_emulation_env:CSLECTFLevel2EmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: emulation, Version: 2 ------------
register(
    id='csle-ctf-level-2-emulation-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level2.emulation.csle_ctf_level2_emulation_env:CSLECTFLevel2Emulation2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: emulation, Costs, Version: 2 ------------
register(
    id='csle-ctf-level-2-emulation-costs-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level2.emulation.csle_ctf_level2_emulation_env:CSLECTFLevel2EmulationWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: emulation, Version: 3 ------------
register(
    id='csle-ctf-level-2-emulation-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level2.emulation.csle_ctf_level2_emulation_env:CSLECTFLevel2Emulation3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: emulation, Costs, Version: 3 ------------
register(
    id='csle-ctf-level-2-emulation-costs-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level2.emulation.csle_ctf_level2_emulation_env:CSLECTFLevel2EmulationWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: emulation, Version: 4 ------------
register(
    id='csle-ctf-level-2-emulation-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level2.emulation.csle_ctf_level2_emulation_env:CSLECTFLevel2Emulation4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: emulation, Costs, Version: 4 ------------
register(
    id='csle-ctf-level-2-emulation-costs-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level2.emulation.csle_ctf_level2_emulation_env:CSLECTFLevel2EmulationWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Version: 1 ------------
register(
    id='csle-ctf-level-2-generated-sim-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level2.generated_simulation.csle_ctf_level2_gensim_env:CSLECTFLevel2GeneratedSim1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Costs, Version: 1 ------------
register(
    id='csle-ctf-level-2-generated-sim-costs-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level2.generated_simulation.csle_ctf_level2_gensim_env:CSLECTFLevel2GeneratedSimWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Simulation, Version: 1 ------------
register(
    id='csle-ctf-level-2-sim-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level2.simulation.csle_ctf_level2_sim_env:CSLECTFLevel2Sim1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Simulation, Costs, Version: 1 ------------
register(
    id='csle-ctf-level-2-sim-costs-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level2.simulation.csle_ctf_level2_sim_env:CSLECTFLevel2SimWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: emulation, Version: Base ------------
register(
    id='csle-ctf-level-3-emulation-base-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level3.emulation.csle_ctf_level3_emulation_env:CSLECTFLevel3EmulationBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: emulation, Version: 1 ------------
register(
    id='csle-ctf-level-3-emulation-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level3.emulation.csle_ctf_level3_emulation_env:CSLECTFLevel3Emulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: emulation, Costs, Version: 1 ------------
register(
    id='csle-ctf-level-3-emulation-costs-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level3.emulation.csle_ctf_level3_emulation_env:CSLECTFLevel3EmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Version: 2 ------------
register(
    id='csle-ctf-level-2-generated-sim-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level2.generated_simulation.csle_ctf_level2_gensim_env:CSLECTFLevel2GeneratedSim2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Costs, Version: 2 ------------
register(
    id='csle-ctf-level-2-generated-sim-costs-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level2.generated_simulation.csle_ctf_level2_gensim_env:CSLECTFLevel2GeneratedSimWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: emulation, Version: 2 ------------
register(
    id='csle-ctf-level-3-emulation-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level3.emulation.csle_ctf_level3_emulation_env:CSLECTFLevel3Emulation2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: emulation, Costs, Version: 2 ------------
register(
    id='csle-ctf-level-3-emulation-costs-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level3.emulation.csle_ctf_level3_emulation_env:CSLECTFLevel3EmulationWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Version: 3 ------------
register(
    id='csle-ctf-level-2-generated-sim-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level2.generated_simulation.csle_ctf_level2_gensim_env:CSLECTFLevel2GeneratedSim3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Costs, Version: 3 ------------
register(
    id='csle-ctf-level-2-generated-sim-costs-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level2.generated_simulation.csle_ctf_level2_gensim_env:CSLECTFLevel2GeneratedSimWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: emulation, Version: 3 ------------
register(
    id='csle-ctf-level-3-emulation-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level3.emulation.csle_ctf_level3_emulation_env:CSLECTFLevel3Emulation3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: emulation, Costs, Version: 3 ------------
register(
    id='csle-ctf-level-3-emulation-costs-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level3.emulation.csle_ctf_level3_emulation_env:CSLECTFLevel3EmulationWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Version: 4 ------------
register(
    id='csle-ctf-level-2-generated-sim-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level2.generated_simulation.csle_ctf_level2_gensim_env:CSLECTFLevel2GeneratedSim4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level2, Mode: Generated Simulation, Costs, Version: 4 ------------
register(
    id='csle-ctf-level-2-generated-sim-costs-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level2.generated_simulation.csle_ctf_level2_gensim_env:CSLECTFLevel2GeneratedSimWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: emulation, Version: 4 ------------
register(
    id='csle-ctf-level-3-emulation-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level3.emulation.csle_ctf_level3_emulation_env:CSLECTFLevel3Emulation4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level3, Mode: emulation, Costs, Version: 4 ------------
register(
    id='csle-ctf-level-3-emulation-costs-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level3.emulation.csle_ctf_level3_emulation_env:CSLECTFLevel3EmulationWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

## Level 4

# -------- Difficulty Level: Level4, Mode: emulation, Version: Base ------------
register(
    id='csle-ctf-level-4-emulation-base-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level4.emulation.csle_ctf_level4_emulation_env:CSLECTFLevel4EmulationBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: emulation, Version: 1 ------------
register(
    id='csle-ctf-level-4-emulation-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level4.emulation.csle_ctf_level4_emulation_env:CSLECTFLevel4Emulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: emulation, Costs, Version: 1 ------------
register(
    id='csle-ctf-level-4-emulation-costs-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level4.emulation.csle_ctf_level4_emulation_env:CSLECTFLevel4EmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: emulation, Version: 2 ------------
register(
    id='csle-ctf-level-4-emulation-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level4.emulation.csle_ctf_level4_emulation_env:CSLECTFLevel4Emulation2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: emulation, Costs, Version: 2 ------------
register(
    id='csle-ctf-level-4-emulation-costs-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level4.emulation.csle_ctf_level4_emulation_env:CSLECTFLevel4EmulationWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: emulation, Version: 3 ------------
register(
    id='csle-ctf-level-4-emulation-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level4.emulation.csle_ctf_level4_emulation_env:CSLECTFLevel4Emulation3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: emulation, Costs, Version: 3 ------------
register(
    id='csle-ctf-level-4-emulation-costs-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level4.emulation.csle_ctf_level4_emulation_env:CSLECTFLevel4EmulationWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: emulation, Version: 4 ------------
register(
    id='csle-ctf-level-4-emulation-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level4.emulation.csle_ctf_level4_emulation_env:CSLECTFLevel4Emulation4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: emulation, Costs, Version: 4 ------------
register(
    id='csle-ctf-level-4-emulation-costs-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level4.emulation.csle_ctf_level4_emulation_env:CSLECTFLevel4EmulationWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Generated Simulation, Version: 4 ------------
register(
    id='csle-ctf-level-4-generated-sim-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level4.generated_simulation.csle_ctf_level4_gensim_env:CSLECTFLevel4GeneratedSim1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Generated Simulation, Costs, Version: 1 ------------
register(
    id='csle-ctf-level-4-generated-sim-costs-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level4.generated_simulation.csle_ctf_level4_gensim_env:CSLECTFLevel4GeneratedSimWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Generated Simulation, Version: 2 ------------
register(
    id='csle-ctf-level-4-generated-sim-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level4.generated_simulation.csle_ctf_level4_gensim_env:CSLECTFLevel4GeneratedSim2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Generated Simulation, Costs, Version: 2 ------------
register(
    id='csle-ctf-level-4-generated-sim-costs-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level4.generated_simulation.csle_ctf_level4_gensim_env:CSLECTFLevel4GeneratedSimWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Generated Simulation, Version: 3 ------------
register(
    id='csle-ctf-level-4-generated-sim-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level4.generated_simulation.csle_ctf_level4_gensim_env:CSLECTFLevel4GeneratedSim3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Generated Simulation, Costs, Version: 3 ------------
register(
    id='csle-ctf-level-4-generated-sim-costs-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level4.generated_simulation.csle_ctf_level4_gensim_env:CSLECTFLevel4GeneratedSimWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Generated Simulation, Version: 4 ------------
register(
    id='csle-ctf-level-4-generated-sim-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level4.generated_simulation.csle_ctf_level4_gensim_env:CSLECTFLevel4GeneratedSim4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Generated Simulation, Costs, Version: 4 ------------
register(
    id='csle-ctf-level-4-generated-sim-costs-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level4.generated_simulation.csle_ctf_level4_gensim_env:CSLECTFLevel4GeneratedSimWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: emulation, Version: 5 ------------
register(
    id='csle-ctf-level-4-emulation-v5',
    entry_point='gym_csle_ctf.envs.derived_envs.level4.emulation.csle_ctf_level4_emulation_env:CSLECTFLevel4Emulation5Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level4, Mode: Generated Simulation, Version: 5 ------------
register(
    id='csle-ctf-level-4-generated-sim-v5',
    entry_point='gym_csle_ctf.envs.derived_envs.level4.generated_simulation.csle_ctf_level4_gensim_env:CSLECTFLevel4GeneratedSim5Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

## Level 5

# -------- Difficulty Level: Level5, Mode: emulation, Version: Base ------------
register(
    id='csle-ctf-level-5-emulation-base-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level5.emulation.csle_ctf_level5_emulation_env:CSLECTFLevel5EmulationBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: emulation, Version: 1 ------------
register(
    id='csle-ctf-level-5-emulation-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level5.emulation.csle_ctf_level5_emulation_env:CSLECTFLevel5Emulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: emulation, Costs, Version: 1 ------------
register(
    id='csle-ctf-level-5-emulation-costs-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level5.emulation.csle_ctf_level5_emulation_env:CSLECTFLevel5EmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: emulation, Version: 2 ------------
register(
    id='csle-ctf-level-5-emulation-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level5.emulation.csle_ctf_level5_emulation_env:CSLECTFLevel5Emulation2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: emulation, Costs, Version: 2 ------------
register(
    id='csle-ctf-level-5-emulation-costs-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level5.emulation.csle_ctf_level5_emulation_env:CSLECTFLevel5EmulationWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: emulation, Version: 3 ------------
register(
    id='csle-ctf-level-5-emulation-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level5.emulation.csle_ctf_level5_emulation_env:CSLECTFLevel5Emulation3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: emulation, Costs, Version: 3 ------------
register(
    id='csle-ctf-level-5-emulation-costs-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level5.emulation.csle_ctf_level5_emulation_env:CSLECTFLevel5EmulationWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: emulation, Version: 4 ------------
register(
    id='csle-ctf-level-5-emulation-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level5.emulation.csle_ctf_level5_emulation_env:CSLECTFLevel5Emulation4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level5, Mode: emulation, Costs, Version: 4 ------------
register(
    id='csle-ctf-level-5-emulation-costs-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level5.emulation.csle_ctf_level5_emulation_env:CSLECTFLevel5EmulationWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

## Level 6

# -------- Difficulty Level: Level6, Mode: emulation, Version: Base ------------
register(
    id='csle-ctf-level-6-emulation-base-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level6.emulation.csle_ctf_level6_emulation_env:CSLECTFLevel6EmulationBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: emulation, Version: 1 ------------
register(
    id='csle-ctf-level-6-emulation-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level6.emulation.csle_ctf_level6_emulation_env:CSLECTFLevel6Emulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: emulation, Costs, Version: 1 ------------
register(
    id='csle-ctf-level-6-emulation-costs-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level6.emulation.csle_ctf_level6_emulation_env:CSLECTFLevel6EmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: emulation, Version: 2 ------------
register(
    id='csle-ctf-level-6-emulation-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level6.emulation.csle_ctf_level6_emulation_env:CSLECTFLevel6Emulation2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: emulation, Costs, Version: 2 ------------
register(
    id='csle-ctf-level-6-emulation-costs-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level6.emulation.csle_ctf_level6_emulation_env:CSLECTFLevel6EmulationWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: emulation, Version: 3 ------------
register(
    id='csle-ctf-level-6-emulation-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level6.emulation.csle_ctf_level6_emulation_env:CSLECTFLevel6Emulation3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: emulation, Costs, Version: 3 ------------
register(
    id='csle-ctf-level-6-emulation-costs-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level6.emulation.csle_ctf_level6_emulation_env:CSLECTFLevel6EmulationWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: emulation, Version: 4 ------------
register(
    id='csle-ctf-level-6-emulation-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level6.emulation.csle_ctf_level6_emulation_env:CSLECTFLevel6Emulation4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level6, Mode: emulation, Costs, Version: 4 ------------
register(
    id='csle-ctf-level-6-emulation-costs-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level6.emulation.csle_ctf_level6_emulation_env:CSLECTFLevel6EmulationWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

## Random

# -------- Difficulty Level: Random, Mode: emulation, Version: Base ------------
register(
    id='csle-ctf-random-emulation-base-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.random.emulation.csle_ctf_random_emulation_env:CSLECTFRandomEmulationBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: emulation, Version: 1 ------------
register(
    id='csle-ctf-random-emulation-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.random.emulation.csle_ctf_random_emulation_env:CSLECTFRandomEmulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: emulation, Costs, Version: 1 ------------
register(
    id='csle-ctf-random-emulation-costs-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.random.emulation.csle_ctf_random_emulation_env:CSLECTFRandomEmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Version: 1 ------------
register(
    id='csle-ctf-random-generated-sim-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.random.generated_simulation.csle_ctf_random_gensim_env:CSLECTFRandomGeneratedSim1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Costs, Version: 1 ------------
register(
    id='csle-ctf-random-generated-sim-costs-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.random.generated_simulation.csle_ctf_random_gensim_env:CSLECTFRandomGeneratedSim1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: emulation, Version: 2 ------------
register(
    id='csle-ctf-random-emulation-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.random.emulation.csle_ctf_random_emulation_env:CSLECTFRandomEmulation2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: emulation, Costs, Version: 2 ------------
register(
    id='csle-ctf-random-emulation-costs-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.random.emulation.csle_ctf_random_emulation_env:CSLECTFRandomEmulationWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Version: 2 ------------
register(
    id='csle-ctf-random-generated-sim-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.random.generated_simulation.csle_ctf_random_gensim_env:CSLECTFRandomGeneratedSim2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Costs, Version: 2 ------------
register(
    id='csle-ctf-random-generated-sim-costs-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.random.generated_simulation.csle_ctf_random_gensim_env:CSLECTFRandomGeneratedSim2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: emulation, Version: 3 ------------
register(
    id='csle-ctf-random-emulation-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.random.emulation.csle_ctf_random_emulation_env:CSLECTFRandomEmulation3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: emulation, Costs, Version: 3 ------------
register(
    id='csle-ctf-random-emulation-costs-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.random.emulation.csle_ctf_random_emulation_env:CSLECTFRandomEmulationWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Version: 3 ------------
register(
    id='csle-ctf-random-generated-sim-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.random.generated_simulation.csle_ctf_random_gensim_env:CSLECTFRandomGeneratedSim3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Costs, Version: 3 ------------
register(
    id='csle-ctf-random-generated-sim-costs-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.random.generated_simulation.csle_ctf_random_gensim_env:CSLECTFRandomGeneratedSim3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: emulation, Version: 4 ------------
register(
    id='csle-ctf-random-emulation-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.random.emulation.csle_ctf_random_emulation_env:CSLECTFRandomEmulation4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: emulation, Costs, Version: 4 ------------
register(
    id='csle-ctf-random-emulation-costs-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.random.emulation.csle_ctf_random_emulation_env:CSLECTFRandomEmulationWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Version: 4 ------------
register(
    id='csle-ctf-random-generated-sim-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.random.generated_simulation.csle_ctf_random_gensim_env:CSLECTFRandomGeneratedSim4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

# -------- Difficulty Level: Random, Mode: Generated Simulation, Costs, Version: 4 ------------
register(
    id='csle-ctf-random-generated-sim-costs-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.random.generated_simulation.csle_ctf_random_gensim_env:CSLECTFRandomGeneratedSim4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_config": None, "flags_config": None, "num_nodes" : None}
)

## Random Many

# -------- Difficulty Level: Random Many, Mode: emulation, Version: 1 ------------
register(
    id='csle-ctf-random-many-emulation-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.random_many.emulation.csle_ctf_random_many_emulation_env:CSLECTFRandomManyEmulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_configs": None, "flags_configs": None, "idx": None}
)

# -------- Difficulty Level: Random Many, Mode: emulation, Costs, Version: 1 ------------
register(
    id='csle-ctf-random-many-emulation-costs-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.random_many.emulation.csle_ctf_random_many_emulation_env:CSLECTFRandomManyEmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_configs": None, "flags_configs": None, "idx": None}
)

# -------- Difficulty Level: Random Many, Mode: Generated Simulation, Version: 1 ------------
register(
    id='csle-ctf-random-many-generated-sim-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.random_many.generated_simulation.csle_ctf_random_many_gensim_env:CSLECTFRandomManyGeneratedSim1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "containers_configs": None, "flags_configs": None, "idx": None}
)

## MultiSim

# -------- Difficulty Level: MultiSim, Mode: Multi-Simulation, Version: 1 ------------
register(
    id='csle-ctf-multisim-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.multisim.csle_ctf_multisim_env:CSLECTFMultiSim1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None,
            "idx": None, "dr_max_num_nodes": int, "dr_min_num_nodes": int, "dr_max_num_flags": int,
            "dr_min_num_flags": int, "dr_min_num_users": int, "dr_max_num_users": int}
)

## Level 7

# -------- Difficulty Level: Level7, Mode: emulation, Version: Base ------------
register(
    id='csle-ctf-level-7-emulation-base-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level7.emulation.csle_ctf_level7_emulation_env:CSLECTFLevel7EmulationBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: emulation, Version: 1 ------------
register(
    id='csle-ctf-level-7-emulation-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level7.emulation.csle_ctf_level7_emulation_env:CSLECTFLevel7Emulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: emulation, Costs, Version: 1 ------------
register(
    id='csle-ctf-level-7-emulation-costs-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level7.emulation.csle_ctf_level7_emulation_env:CSLECTFLevel7EmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: emulation, Version: 2 ------------
register(
    id='csle-ctf-level-7-emulation-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level7.emulation.csle_ctf_level7_emulation_env:CSLECTFLevel7Emulation2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: emulation, Costs, Version: 2 ------------
register(
    id='csle-ctf-level-7-emulation-costs-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level7.emulation.csle_ctf_level7_emulation_env:CSLECTFLevel7EmulationWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: emulation, Version: 3 ------------
register(
    id='csle-ctf-level-7-emulation-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level7.emulation.csle_ctf_level7_emulation_env:CSLECTFLevel7Emulation3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: emulation, Costs, Version: 3 ------------
register(
    id='csle-ctf-level-7-emulation-costs-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level7.emulation.csle_ctf_level7_emulation_env:CSLECTFLevel7EmulationWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: emulation, Version: 4 ------------
register(
    id='csle-ctf-level-7-emulation-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level7.emulation.csle_ctf_level7_emulation_env:CSLECTFLevel7Emulation4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level7, Mode: emulation, Costs, Version: 4 ------------
register(
    id='csle-ctf-level-7-emulation-costs-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level7.emulation.csle_ctf_level7_emulation_env:CSLECTFLevel7EmulationWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

## Level 8

# -------- Difficulty Level: Level8, Mode: emulation, Version: Base ------------
register(
    id='csle-ctf-level-8-emulation-base-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level8.emulation.csle_ctf_level8_emulation_env:CSLECTFLevel8EmulationBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level8, Mode: emulation, Version: 1 ------------
register(
    id='csle-ctf-level-8-emulation-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level8.emulation.csle_ctf_level8_emulation_env:CSLECTFLevel8Emulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level8, Mode: emulation, Costs, Version: 1 ------------
register(
    id='csle-ctf-level-8-emulation-costs-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level8.emulation.csle_ctf_level8_emulation_env:CSLECTFLevel8EmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level8, Mode: emulation, Version: 2 ------------
register(
    id='csle-ctf-level-8-emulation-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level8.emulation.csle_ctf_level8_emulation_env:CSLECTFLevel8Emulation2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level8, Mode: emulation, Costs, Version: 2 ------------
register(
    id='csle-ctf-level-8-emulation-costs-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level8.emulation.csle_ctf_level8_emulation_env:CSLECTFLevel8EmulationWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level8, Mode: emulation, Version: 3 ------------
register(
    id='csle-ctf-level-8-emulation-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level8.emulation.csle_ctf_level8_emulation_env:CSLECTFLevel8Emulation3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level8, Mode: emulation, Costs, Version: 3 ------------
register(
    id='csle-ctf-level-8-emulation-costs-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level8.emulation.csle_ctf_level8_emulation_env:CSLECTFLevel8EmulationWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level8, Mode: emulation, Version: 4 ------------
register(
    id='csle-ctf-level-8-emulation-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level8.emulation.csle_ctf_level8_emulation_env:CSLECTFLevel8Emulation4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level8, Mode: emulation, Costs, Version: 4 ------------
register(
    id='csle-ctf-level-8-emulation-costs-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level8.emulation.csle_ctf_level8_emulation_env:CSLECTFLevel8EmulationWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)


## Level 9

# -------- Difficulty Level: Level9, Mode: emulation, Version: Base ------------
register(
    id='csle-ctf-level-9-emulation-base-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level9.emulation.csle_ctf_level9_emulation_env:CSLECTFLevel9EmulationBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: emulation, Version: 1 ------------
register(
    id='csle-ctf-level-9-emulation-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level9.emulation.csle_ctf_level9_emulation_env:CSLECTFLevel9Emulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: emulation, Costs, Version: 1 ------------
register(
    id='csle-ctf-level-9-emulation-costs-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level9.emulation.csle_ctf_level9_emulation_env:CSLECTFLevel9EmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: emulation, Version: 2 ------------
register(
    id='csle-ctf-level-9-emulation-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level9.emulation.csle_ctf_level9_emulation_env:CSLECTFLevel9Emulation2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: emulation, Costs, Version: 2 ------------
register(
    id='csle-ctf-level-9-emulation-costs-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level9.emulation.csle_ctf_level9_emulation_env:CSLECTFLevel9EmulationWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: emulation, Version: 3 ------------
register(
    id='csle-ctf-level-9-emulation-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level9.emulation.csle_ctf_level9_emulation_env:CSLECTFLevel9Emulation3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: emulation, Costs, Version: 3 ------------
register(
    id='csle-ctf-level-9-emulation-costs-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level9.emulation.csle_ctf_level9_emulation_env:CSLECTFLevel9EmulationWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: emulation, Version: 4 ------------
register(
    id='csle-ctf-level-9-emulation-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level9.emulation.csle_ctf_level9_emulation_env:CSLECTFLevel9Emulation4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: emulation, Costs, Version: 4 ------------
register(
    id='csle-ctf-level-9-emulation-costs-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level9.emulation.csle_ctf_level9_emulation_env:CSLECTFLevel9EmulationWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: emulation, Version: 5 ------------
register(
    id='csle-ctf-level-9-emulation-v5',
    entry_point='gym_csle_ctf.envs.derived_envs.level9.emulation.csle_ctf_level9_emulation_env:CSLECTFLevel9Emulation5Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: emulation, Version: 5 ------------
register(
    id='csle-ctf-level-9-emulation-v6',
    entry_point='gym_csle_ctf.envs.derived_envs.level9.emulation.csle_ctf_level9_emulation_env:CSLECTFLevel9Emulation6Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: Generated Simulation, Version: 1 ------------
register(
    id='csle-ctf-level-9-generated-sim-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level9.generated_simulation.csle_ctf_level9_gensim_env:CSLECTFLevel9GeneratedSim1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: Generated Simulation, Costs, Version: 1 ------------
register(
    id='csle-ctf-level-9-generated-sim-costs-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level9.generated_simulation.csle_ctf_level9_gensim_env:CSLECTFLevel9GeneratedSimWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: Generated Simulation, Version: 2 ------------
register(
    id='csle-ctf-level-9-generated-sim-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level9.generated_simulation.csle_ctf_level9_gensim_env:CSLECTFLevel9GeneratedSim2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: Generated Simulation, Costs, Version: 2 ------------
register(
    id='csle-ctf-level-9-generated-sim-costs-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level9.generated_simulation.csle_ctf_level9_gensim_env:CSLECTFLevel9GeneratedSimWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: Generated Simulation, Version: 3 ------------
register(
    id='csle-ctf-level-9-generated-sim-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level9.generated_simulation.csle_ctf_level9_gensim_env:CSLECTFLevel9GeneratedSim3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: Generated Simulation, Costs, Version: 3 ------------
register(
    id='csle-ctf-level-9-generated-sim-costs-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level9.generated_simulation.csle_ctf_level9_gensim_env:CSLECTFLevel9GeneratedSimWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: Generated Simulation, Version: 4 ------------
register(
    id='csle-ctf-level-9-generated-sim-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level9.generated_simulation.csle_ctf_level9_gensim_env:CSLECTFLevel9GeneratedSim4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: Generated Simulation, Costs, Version: 4 ------------
register(
    id='csle-ctf-level-9-generated-sim-costs-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level9.generated_simulation.csle_ctf_level9_gensim_env:CSLECTFLevel9GeneratedSimWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: Generated Simulation, Version: 5 ------------
register(
    id='csle-ctf-level-9-generated-sim-v5',
    entry_point='gym_csle_ctf.envs.derived_envs.level9.generated_simulation.csle_ctf_level9_gensim_env:CSLECTFLevel9GeneratedSim5Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level9, Mode: Generated Simulation, Version: 6 ------------
register(
    id='csle-ctf-level-9-generated-sim-v6',
    entry_point='gym_csle_ctf.envs.derived_envs.level9.generated_simulation.csle_ctf_level9_gensim_env:CSLECTFLevel9GeneratedSim6Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)


## Level 10

# -------- Difficulty Level: Level10, Mode: emulation, Version: Base ------------
register(
    id='csle-ctf-level-10-emulation-base-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level10.emulation.csle_ctf_level10_emulation_env:CSLECTFLevel10EmulationBaseEnv',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level10, Mode: emulation, Version: 1 ------------
register(
    id='csle-ctf-level-10-emulation-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level10.emulation.csle_ctf_level10_emulation_env:CSLECTFLevel10Emulation1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level10, Mode: emulation, Costs, Version: 1 ------------
register(
    id='csle-ctf-level-10-emulation-costs-v1',
    entry_point='gym_csle_ctf.envs.derived_envs.level10.emulation.csle_ctf_level10_emulation_env:CSLECTFLevel10EmulationWithCosts1Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level10, Mode: emulation, Version: 2 ------------
register(
    id='csle-ctf-level-10-emulation-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level10.emulation.csle_ctf_level10_emulation_env:CSLECTFLevel10Emulation2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level10, Mode: emulation, Costs, Version: 2 ------------
register(
    id='csle-ctf-level-10-emulation-costs-v2',
    entry_point='gym_csle_ctf.envs.derived_envs.level10.emulation.csle_ctf_level10_emulation_env:CSLECTFLevel10EmulationWithCosts2Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level10, Mode: emulation, Version: 3 ------------
register(
    id='csle-ctf-level-10-emulation-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level10.emulation.csle_ctf_level10_emulation_env:CSLECTFLevel10Emulation3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level10, Mode: emulation, Costs, Version: 3 ------------
register(
    id='csle-ctf-level-10-emulation-costs-v3',
    entry_point='gym_csle_ctf.envs.derived_envs.level10.emulation.csle_ctf_level10_emulation_env:CSLECTFLevel10EmulationWithCosts3Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level10, Mode: emulation, Version: 4 ------------
register(
    id='csle-ctf-level-10-emulation-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level10.emulation.csle_ctf_level10_emulation_env:CSLECTFLevel10Emulation4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Level10, Mode: emulation, Costs, Version: 4 ------------
register(
    id='csle-ctf-level-10-emulation-costs-v4',
    entry_point='gym_csle_ctf.envs.derived_envs.level10.emulation.csle_ctf_level10_emulation_env:CSLECTFLevel10EmulationWithCosts4Env',
    kwargs={'env_config': None, 'emulation_config': None, "checkpoint_dir": None}
)