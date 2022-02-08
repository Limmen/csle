# ------ Base ----- #

from gym_csle_ctf.envs.csle_ctf_env import CSLECTFEnv

# ------ Level 1 ----- #

from gym_csle_ctf.envs.derived_envs.level1.simulation.csle_ctf_level1_sim_env import CSLECTFLevel1SimBaseEnv, \
    CSLECTFLevel1Sim1Env, CSLECTFLevel1Sim2Env, CSLECTFLevel1Sim3Env, CSLECTFLevel1Sim4Env, \
    CSLECTFLevel1SimWithCosts1Env, \
    CSLECTFLevel1SimWithCosts2Env, CSLECTFLevel1SimWithCosts3Env, \
    CSLECTFLevel1SimWithCosts4Env

from gym_csle_ctf.envs.derived_envs.level1.generated_simulation.csle_ctf_level1_gensim_env import \
    CSLECTFLevel1GeneratedSimWithCosts1Env, CSLECTFLevel1GeneratedSim2Env, CSLECTFLevel1GeneratedSim1Env, \
    CSLECTFLevel1GeneratedSimWithCosts2Env, CSLECTFLevel1GeneratedSim3Env, \
    CSLECTFLevel1GeneratedSimWithCosts3Env, CSLECTFLevel1GeneratedSim4Env, \
    CSLECTFLevel1GeneratedSimWithCosts4Env

# ------ Level 2 ----- #

from gym_csle_ctf.envs.derived_envs.level2.emulation.csle_ctf_level2_emulation_env import CSLECTFLevel2EmulationBaseEnv, \
    CSLECTFLevel2Emulation1Env, CSLECTFLevel2Emulation2Env, CSLECTFLevel2Emulation3Env, CSLECTFLevel2Emulation4Env, \
    CSLECTFLevel2EmulationWithCosts1Env, CSLECTFLevel2EmulationWithCosts2Env, CSLECTFLevel2EmulationWithCosts3Env, \
    CSLECTFLevel2EmulationWithCosts4Env

from gym_csle_ctf.envs.derived_envs.level2.simulation.csle_ctf_level2_sim_env import CSLECTFLevel2SimBaseEnv, \
    CSLECTFLevel2Sim1Env, CSLECTFLevel2SimWithCosts1Env

from gym_csle_ctf.envs.derived_envs.level2.generated_simulation.csle_ctf_level2_gensim_env import \
    CSLECTFLevel2GeneratedSimWithCosts1Env, CSLECTFLevel2GeneratedSim2Env, CSLECTFLevel2GeneratedSim1Env, \
    CSLECTFLevel2GeneratedSimWithCosts2Env, CSLECTFLevel2GeneratedSim3Env, \
    CSLECTFLevel2GeneratedSimWithCosts3Env, CSLECTFLevel2GeneratedSim4Env, \
    CSLECTFLevel2GeneratedSimWithCosts4Env


# ------ Level 3 ----- #

from gym_csle_ctf.envs.derived_envs.level3.emulation.csle_ctf_level3_emulation_env import CSLECTFLevel3EmulationBaseEnv, \
    CSLECTFLevel3Emulation1Env, CSLECTFLevel3Emulation2Env, CSLECTFLevel3Emulation3Env, CSLECTFLevel3Emulation4Env, \
    CSLECTFLevel3EmulationWithCosts1Env, CSLECTFLevel3EmulationWithCosts2Env, CSLECTFLevel3EmulationWithCosts3Env, \
    CSLECTFLevel3EmulationWithCosts4Env


# ------ Level 4 ----- #

from gym_csle_ctf.envs.derived_envs.level4.emulation.csle_ctf_level4_emulation_env import CSLECTFLevel4EmulationBaseEnv, \
    CSLECTFLevel4Emulation1Env, CSLECTFLevel4Emulation2Env, CSLECTFLevel4Emulation3Env, CSLECTFLevel4Emulation4Env, \
    CSLECTFLevel4EmulationWithCosts1Env, CSLECTFLevel4EmulationWithCosts2Env, CSLECTFLevel4EmulationWithCosts3Env, \
    CSLECTFLevel4EmulationWithCosts4Env, CSLECTFLevel4Emulation5Env

from gym_csle_ctf.envs.derived_envs.level4.generated_simulation.csle_ctf_level4_gensim_env import \
    CSLECTFLevel4GeneratedSimWithCosts1Env, CSLECTFLevel4GeneratedSim2Env, CSLECTFLevel4GeneratedSim1Env, \
    CSLECTFLevel4GeneratedSimWithCosts2Env, CSLECTFLevel4GeneratedSim3Env, \
    CSLECTFLevel4GeneratedSimWithCosts3Env, CSLECTFLevel4GeneratedSim4Env, \
    CSLECTFLevel4GeneratedSimWithCosts4Env, CSLECTFLevel4GeneratedSim5Env

# ------ Level 5 ----- #

from gym_csle_ctf.envs.derived_envs.level5.emulation.csle_ctf_level5_emulation_env import CSLECTFLevel5EmulationBaseEnv, \
    CSLECTFLevel5Emulation1Env, CSLECTFLevel5Emulation2Env, CSLECTFLevel5Emulation3Env, CSLECTFLevel5Emulation4Env, \
    CSLECTFLevel5EmulationWithCosts1Env, CSLECTFLevel5EmulationWithCosts2Env, CSLECTFLevel5EmulationWithCosts3Env, \
    CSLECTFLevel5EmulationWithCosts4Env

# ------ Level 6 ----- #

from gym_csle_ctf.envs.derived_envs.level6.emulation.csle_ctf_level6_emulation_env import CSLECTFLevel6EmulationBaseEnv, \
    CSLECTFLevel6Emulation1Env, CSLECTFLevel6Emulation2Env, CSLECTFLevel6Emulation3Env, CSLECTFLevel6Emulation4Env, \
    CSLECTFLevel6EmulationWithCosts1Env, CSLECTFLevel6EmulationWithCosts2Env, CSLECTFLevel6EmulationWithCosts3Env, \
    CSLECTFLevel6EmulationWithCosts4Env

# ------ Level 7 ----- #

from gym_csle_ctf.envs.derived_envs.level7.emulation.csle_ctf_level7_emulation_env import CSLECTFLevel7EmulationBaseEnv, \
    CSLECTFLevel7Emulation1Env, CSLECTFLevel7Emulation2Env, CSLECTFLevel7Emulation3Env, CSLECTFLevel7Emulation4Env, \
    CSLECTFLevel7EmulationWithCosts1Env, CSLECTFLevel7EmulationWithCosts2Env, CSLECTFLevel7EmulationWithCosts3Env, \
    CSLECTFLevel7EmulationWithCosts4Env

# ------ Level 8 ----- #

from gym_csle_ctf.envs.derived_envs.level8.emulation.csle_ctf_level8_emulation_env import CSLECTFLevel8EmulationBaseEnv, \
    CSLECTFLevel8Emulation1Env, CSLECTFLevel8Emulation2Env, CSLECTFLevel8Emulation3Env, CSLECTFLevel8Emulation4Env, \
    CSLECTFLevel8EmulationWithCosts1Env, CSLECTFLevel8EmulationWithCosts2Env, CSLECTFLevel8EmulationWithCosts3Env, \
    CSLECTFLevel8EmulationWithCosts4Env

# ------ Level 9 ----- #
from gym_csle_ctf.envs.derived_envs.level9.emulation.csle_ctf_level9_emulation_env import CSLECTFLevel9EmulationBaseEnv, \
    CSLECTFLevel9Emulation1Env, CSLECTFLevel9Emulation2Env, CSLECTFLevel9Emulation3Env, CSLECTFLevel9Emulation4Env, \
    CSLECTFLevel9EmulationWithCosts1Env, CSLECTFLevel9EmulationWithCosts2Env, CSLECTFLevel9EmulationWithCosts3Env, \
    CSLECTFLevel9EmulationWithCosts4Env, CSLECTFLevel9Emulation5Env, CSLECTFLevel9Emulation6Env

from gym_csle_ctf.envs.derived_envs.level9.generated_simulation.csle_ctf_level9_gensim_env import \
    CSLECTFLevel9GeneratedSimWithCosts1Env, CSLECTFLevel9GeneratedSim2Env, CSLECTFLevel9GeneratedSim1Env, \
    CSLECTFLevel9GeneratedSimWithCosts2Env, CSLECTFLevel9GeneratedSim3Env, \
    CSLECTFLevel9GeneratedSimWithCosts3Env, CSLECTFLevel9GeneratedSim4Env, \
    CSLECTFLevel9GeneratedSimWithCosts4Env, CSLECTFLevel9GeneratedSim5Env, CSLECTFLevel9GeneratedSim6Env

# ------ Level 10 ----- #

from gym_csle_ctf.envs.derived_envs.level10.emulation.csle_ctf_level10_emulation_env import CSLECTFLevel10EmulationBaseEnv, \
    CSLECTFLevel10Emulation1Env, CSLECTFLevel10Emulation2Env, CSLECTFLevel10Emulation3Env, CSLECTFLevel10Emulation4Env, \
    CSLECTFLevel10EmulationWithCosts1Env, CSLECTFLevel10EmulationWithCosts2Env, CSLECTFLevel10EmulationWithCosts3Env, \
    CSLECTFLevel10EmulationWithCosts4Env

# ------ Random ----- #

from gym_csle_ctf.envs.derived_envs.random.generated_simulation.csle_ctf_random_gensim_env import \
    CSLECTFRandomGeneratedSim1Env, CSLECTFRandomGeneratedSimWithCosts1Env, CSLECTFRandomGeneratedSim2Env, \
    CSLECTFRandomGeneratedSimWithCosts2Env, CSLECTFRandomGeneratedSim3Env, CSLECTFRandomGeneratedSimWithCosts3Env, \
    CSLECTFRandomGeneratedSim4Env, CSLECTFRandomGeneratedSimWithCosts4Env

# ------ Random Many ----- #

from gym_csle_ctf.envs.derived_envs.random_many.emulation.csle_ctf_random_many_emulation_env import \
    CSLECTFRandomManyEmulation1Env, CSLECTFRandomManyEmulationWithCosts1Env

from gym_csle_ctf.envs.derived_envs.random_many.generated_simulation.csle_ctf_random_many_gensim_env import \
    CSLECTFRandomManyGeneratedSim1Env

# ------ Multisim ----- #

from gym_csle_ctf.envs.derived_envs.multisim.csle_ctf_multisim_env import \
    CSLECTFMultiSim1Env
