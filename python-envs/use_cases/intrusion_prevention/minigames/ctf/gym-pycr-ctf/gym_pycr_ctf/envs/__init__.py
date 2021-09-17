# ------ Base ----- #

from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv

# ------ Level 1 ----- #

from gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env import PyCRCTFLevel1SimBaseEnv, \
    PyCRCTFLevel1Sim1Env, PyCRCTFLevel1Sim2Env, PyCRCTFLevel1Sim3Env, PyCRCTFLevel1Sim4Env, \
    PyCRCTFLevel1SimWithCosts1Env, \
    PyCRCTFLevel1SimWithCosts2Env, PyCRCTFLevel1SimWithCosts3Env, \
    PyCRCTFLevel1SimWithCosts4Env

from gym_pycr_ctf.envs.derived_envs.level1.generated_simulation.pycr_ctf_level1_gensim_env import \
    PyCRCTFLevel1GeneratedSimWithCosts1Env, PyCRCTFLevel1GeneratedSim2Env, PyCRCTFLevel1GeneratedSim1Env, \
    PyCRCTFLevel1GeneratedSimWithCosts2Env, PyCRCTFLevel1GeneratedSim3Env, \
    PyCRCTFLevel1GeneratedSimWithCosts3Env, PyCRCTFLevel1GeneratedSim4Env, \
    PyCRCTFLevel1GeneratedSimWithCosts4Env

# ------ Level 2 ----- #

from gym_pycr_ctf.envs.derived_envs.level2.emulation.pycr_ctf_level2_emulation_env import PyCRCTFLevel2EmulationBaseEnv, \
    PyCRCTFLevel2Emulation1Env, PyCRCTFLevel2Emulation2Env, PyCRCTFLevel2Emulation3Env, PyCRCTFLevel2Emulation4Env, \
    PyCRCTFLevel2EmulationWithCosts1Env, PyCRCTFLevel2EmulationWithCosts2Env, PyCRCTFLevel2EmulationWithCosts3Env, \
    PyCRCTFLevel2EmulationWithCosts4Env

from gym_pycr_ctf.envs.derived_envs.level2.simulation.pycr_ctf_level2_sim_env import PyCRCTFLevel2SimBaseEnv, \
    PyCRCTFLevel2Sim1Env, PyCRCTFLevel2SimWithCosts1Env

from gym_pycr_ctf.envs.derived_envs.level2.generated_simulation.pycr_ctf_level2_gensim_env import \
    PyCRCTFLevel2GeneratedSimWithCosts1Env, PyCRCTFLevel2GeneratedSim2Env, PyCRCTFLevel2GeneratedSim1Env, \
    PyCRCTFLevel2GeneratedSimWithCosts2Env, PyCRCTFLevel2GeneratedSim3Env, \
    PyCRCTFLevel2GeneratedSimWithCosts3Env, PyCRCTFLevel2GeneratedSim4Env, \
    PyCRCTFLevel2GeneratedSimWithCosts4Env


# ------ Level 3 ----- #

from gym_pycr_ctf.envs.derived_envs.level3.emulation.pycr_ctf_level3_emulation_env import PyCRCTFLevel3EmulationBaseEnv, \
    PyCRCTFLevel3Emulation1Env, PyCRCTFLevel3Emulation2Env, PyCRCTFLevel3Emulation3Env, PyCRCTFLevel3Emulation4Env, \
    PyCRCTFLevel3EmulationWithCosts1Env, PyCRCTFLevel3EmulationWithCosts2Env, PyCRCTFLevel3EmulationWithCosts3Env, \
    PyCRCTFLevel3EmulationWithCosts4Env


# ------ Level 4 ----- #

from gym_pycr_ctf.envs.derived_envs.level4.emulation.pycr_ctf_level4_emulation_env import PyCRCTFLevel4EmulationBaseEnv, \
    PyCRCTFLevel4Emulation1Env, PyCRCTFLevel4Emulation2Env, PyCRCTFLevel4Emulation3Env, PyCRCTFLevel4Emulation4Env, \
    PyCRCTFLevel4EmulationWithCosts1Env, PyCRCTFLevel4EmulationWithCosts2Env, PyCRCTFLevel4EmulationWithCosts3Env, \
    PyCRCTFLevel4EmulationWithCosts4Env, PyCRCTFLevel4Emulation5Env

from gym_pycr_ctf.envs.derived_envs.level4.generated_simulation.pycr_ctf_level4_gensim_env import \
    PyCRCTFLevel4GeneratedSimWithCosts1Env, PyCRCTFLevel4GeneratedSim2Env, PyCRCTFLevel4GeneratedSim1Env, \
    PyCRCTFLevel4GeneratedSimWithCosts2Env, PyCRCTFLevel4GeneratedSim3Env, \
    PyCRCTFLevel4GeneratedSimWithCosts3Env, PyCRCTFLevel4GeneratedSim4Env, \
    PyCRCTFLevel4GeneratedSimWithCosts4Env, PyCRCTFLevel4GeneratedSim5Env

# ------ Level 5 ----- #

from gym_pycr_ctf.envs.derived_envs.level5.emulation.pycr_ctf_level5_emulation_env import PyCRCTFLevel5EmulationBaseEnv, \
    PyCRCTFLevel5Emulation1Env, PyCRCTFLevel5Emulation2Env, PyCRCTFLevel5Emulation3Env, PyCRCTFLevel5Emulation4Env, \
    PyCRCTFLevel5EmulationWithCosts1Env, PyCRCTFLevel5EmulationWithCosts2Env, PyCRCTFLevel5EmulationWithCosts3Env, \
    PyCRCTFLevel5EmulationWithCosts4Env

# ------ Level 6 ----- #

from gym_pycr_ctf.envs.derived_envs.level6.emulation.pycr_ctf_level6_emulation_env import PyCRCTFLevel6EmulationBaseEnv, \
    PyCRCTFLevel6Emulation1Env, PyCRCTFLevel6Emulation2Env, PyCRCTFLevel6Emulation3Env, PyCRCTFLevel6Emulation4Env, \
    PyCRCTFLevel6EmulationWithCosts1Env, PyCRCTFLevel6EmulationWithCosts2Env, PyCRCTFLevel6EmulationWithCosts3Env, \
    PyCRCTFLevel6EmulationWithCosts4Env

# ------ Level 7 ----- #

from gym_pycr_ctf.envs.derived_envs.level7.emulation.pycr_ctf_level7_emulation_env import PyCRCTFLevel7EmulationBaseEnv, \
    PyCRCTFLevel7Emulation1Env, PyCRCTFLevel7Emulation2Env, PyCRCTFLevel7Emulation3Env, PyCRCTFLevel7Emulation4Env, \
    PyCRCTFLevel7EmulationWithCosts1Env, PyCRCTFLevel7EmulationWithCosts2Env, PyCRCTFLevel7EmulationWithCosts3Env, \
    PyCRCTFLevel7EmulationWithCosts4Env

# ------ Level 8 ----- #

from gym_pycr_ctf.envs.derived_envs.level8.emulation.pycr_ctf_level8_emulation_env import PyCRCTFLevel8EmulationBaseEnv, \
    PyCRCTFLevel8Emulation1Env, PyCRCTFLevel8Emulation2Env, PyCRCTFLevel8Emulation3Env, PyCRCTFLevel8Emulation4Env, \
    PyCRCTFLevel8EmulationWithCosts1Env, PyCRCTFLevel8EmulationWithCosts2Env, PyCRCTFLevel8EmulationWithCosts3Env, \
    PyCRCTFLevel8EmulationWithCosts4Env

# ------ Level 9 ----- #
from gym_pycr_ctf.envs.derived_envs.level9.emulation.pycr_ctf_level9_emulation_env import PyCRCTFLevel9EmulationBaseEnv, \
    PyCRCTFLevel9Emulation1Env, PyCRCTFLevel9Emulation2Env, PyCRCTFLevel9Emulation3Env, PyCRCTFLevel9Emulation4Env, \
    PyCRCTFLevel9EmulationWithCosts1Env, PyCRCTFLevel9EmulationWithCosts2Env, PyCRCTFLevel9EmulationWithCosts3Env, \
    PyCRCTFLevel9EmulationWithCosts4Env, PyCRCTFLevel9Emulation5Env, PyCRCTFLevel9Emulation6Env

from gym_pycr_ctf.envs.derived_envs.level9.generated_simulation.pycr_ctf_level9_gensim_env import \
    PyCRCTFLevel9GeneratedSimWithCosts1Env, PyCRCTFLevel9GeneratedSim2Env, PyCRCTFLevel9GeneratedSim1Env, \
    PyCRCTFLevel9GeneratedSimWithCosts2Env, PyCRCTFLevel9GeneratedSim3Env, \
    PyCRCTFLevel9GeneratedSimWithCosts3Env, PyCRCTFLevel9GeneratedSim4Env, \
    PyCRCTFLevel9GeneratedSimWithCosts4Env, PyCRCTFLevel9GeneratedSim5Env, PyCRCTFLevel9GeneratedSim6Env

# ------ Level 10 ----- #

from gym_pycr_ctf.envs.derived_envs.level10.emulation.pycr_ctf_level10_emulation_env import PyCRCTFLevel10EmulationBaseEnv, \
    PyCRCTFLevel10Emulation1Env, PyCRCTFLevel10Emulation2Env, PyCRCTFLevel10Emulation3Env, PyCRCTFLevel10Emulation4Env, \
    PyCRCTFLevel10EmulationWithCosts1Env, PyCRCTFLevel10EmulationWithCosts2Env, PyCRCTFLevel10EmulationWithCosts3Env, \
    PyCRCTFLevel10EmulationWithCosts4Env

# ------ Random ----- #

from gym_pycr_ctf.envs.derived_envs.random.generated_simulation.pycr_ctf_random_gensim_env import \
    PyCRCTFRandomGeneratedSim1Env, PyCRCTFRandomGeneratedSimWithCosts1Env, PyCRCTFRandomGeneratedSim2Env, \
    PyCRCTFRandomGeneratedSimWithCosts2Env, PyCRCTFRandomGeneratedSim3Env, PyCRCTFRandomGeneratedSimWithCosts3Env, \
    PyCRCTFRandomGeneratedSim4Env, PyCRCTFRandomGeneratedSimWithCosts4Env

# ------ Random Many ----- #

from gym_pycr_ctf.envs.derived_envs.random_many.emulation.pycr_ctf_random_many_emulation_env import \
    PyCRCTFRandomManyEmulation1Env, PyCRCTFRandomManyEmulationWithCosts1Env

from gym_pycr_ctf.envs.derived_envs.random_many.generated_simulation.pycr_ctf_random_many_gensim_env import \
    PyCRCTFRandomManyGeneratedSim1Env

# ------ Multisim ----- #

from gym_pycr_ctf.envs.derived_envs.multisim.pycr_ctf_multisim_env import \
    PyCRCTFMultiSim1Env
