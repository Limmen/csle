# ------ Base ----- #

from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv

# ------ Level 1 ----- #

from gym_pycr_ctf.envs.derived_envs.level1.cluster.pycr_ctf_level1_cluster_env import PyCRCTFLevel1ClusterBaseEnv, \
    PyCRCTFLevel1Cluster1Env, PyCRCTFLevel1Cluster2Env, PyCRCTFLevel1Cluster3Env, PyCRCTFLevel1Cluster4Env, \
    PyCRCTFLevel1ClusterWithCosts1Env, PyCRCTFLevel1ClusterWithCosts2Env, PyCRCTFLevel1ClusterWithCosts3Env, \
    PyCRCTFLevel1ClusterWithCosts4Env, PyCRCTFLevel1ClusterNoCache1Env

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

from gym_pycr_ctf.envs.derived_envs.level2.cluster.pycr_ctf_level2_cluster_env import PyCRCTFLevel2ClusterBaseEnv, \
    PyCRCTFLevel2Cluster1Env, PyCRCTFLevel2Cluster2Env, PyCRCTFLevel2Cluster3Env, PyCRCTFLevel2Cluster4Env, \
    PyCRCTFLevel2ClusterWithCosts1Env, PyCRCTFLevel2ClusterWithCosts2Env, PyCRCTFLevel2ClusterWithCosts3Env, \
    PyCRCTFLevel2ClusterWithCosts4Env

from gym_pycr_ctf.envs.derived_envs.level2.simulation.pycr_ctf_level2_sim_env import PyCRCTFLevel2SimBaseEnv, \
    PyCRCTFLevel2Sim1Env, PyCRCTFLevel2SimWithCosts1Env

from gym_pycr_ctf.envs.derived_envs.level2.generated_simulation.pycr_ctf_level2_gensim_env import \
    PyCRCTFLevel2GeneratedSimWithCosts1Env, PyCRCTFLevel2GeneratedSim2Env, PyCRCTFLevel2GeneratedSim1Env, \
    PyCRCTFLevel2GeneratedSimWithCosts2Env, PyCRCTFLevel2GeneratedSim3Env, \
    PyCRCTFLevel2GeneratedSimWithCosts3Env, PyCRCTFLevel2GeneratedSim4Env, \
    PyCRCTFLevel2GeneratedSimWithCosts4Env


# ------ Level 3 ----- #

from gym_pycr_ctf.envs.derived_envs.level3.cluster.pycr_ctf_level3_cluster_env import PyCRCTFLevel3ClusterBaseEnv, \
    PyCRCTFLevel3Cluster1Env, PyCRCTFLevel3Cluster2Env, PyCRCTFLevel3Cluster3Env, PyCRCTFLevel3Cluster4Env, \
    PyCRCTFLevel3ClusterWithCosts1Env, PyCRCTFLevel3ClusterWithCosts2Env, PyCRCTFLevel3ClusterWithCosts3Env, \
    PyCRCTFLevel3ClusterWithCosts4Env


# ------ Level 4 ----- #

from gym_pycr_ctf.envs.derived_envs.level4.cluster.pycr_ctf_level4_cluster_env import PyCRCTFLevel4ClusterBaseEnv, \
    PyCRCTFLevel4Cluster1Env, PyCRCTFLevel4Cluster2Env, PyCRCTFLevel4Cluster3Env, PyCRCTFLevel4Cluster4Env, \
    PyCRCTFLevel4ClusterWithCosts1Env, PyCRCTFLevel4ClusterWithCosts2Env, PyCRCTFLevel4ClusterWithCosts3Env, \
    PyCRCTFLevel4ClusterWithCosts4Env

# ------ Level 5 ----- #

from gym_pycr_ctf.envs.derived_envs.level5.cluster.pycr_ctf_level5_cluster_env import PyCRCTFLevel5ClusterBaseEnv, \
    PyCRCTFLevel5Cluster1Env, PyCRCTFLevel5Cluster2Env, PyCRCTFLevel5Cluster3Env, PyCRCTFLevel5Cluster4Env, \
    PyCRCTFLevel5ClusterWithCosts1Env, PyCRCTFLevel5ClusterWithCosts2Env, PyCRCTFLevel5ClusterWithCosts3Env, \
    PyCRCTFLevel5ClusterWithCosts4Env

# ------ Level 6 ----- #

from gym_pycr_ctf.envs.derived_envs.level6.cluster.pycr_ctf_level6_cluster_env import PyCRCTFLevel6ClusterBaseEnv, \
    PyCRCTFLevel6Cluster1Env, PyCRCTFLevel6Cluster2Env, PyCRCTFLevel6Cluster3Env, PyCRCTFLevel6Cluster4Env, \
    PyCRCTFLevel6ClusterWithCosts1Env, PyCRCTFLevel6ClusterWithCosts2Env, PyCRCTFLevel6ClusterWithCosts3Env, \
    PyCRCTFLevel6ClusterWithCosts4Env

# ------ Level 7 ----- #

from gym_pycr_ctf.envs.derived_envs.level7.cluster.pycr_ctf_level7_cluster_env import PyCRCTFLevel7ClusterBaseEnv, \
    PyCRCTFLevel7Cluster1Env, PyCRCTFLevel7Cluster2Env, PyCRCTFLevel7Cluster3Env, PyCRCTFLevel7Cluster4Env, \
    PyCRCTFLevel7ClusterWithCosts1Env, PyCRCTFLevel7ClusterWithCosts2Env, PyCRCTFLevel7ClusterWithCosts3Env, \
    PyCRCTFLevel7ClusterWithCosts4Env


# ------ Level 8 ----- #

from gym_pycr_ctf.envs.derived_envs.level8.cluster.pycr_ctf_level8_cluster_env import PyCRCTFLevel8ClusterBaseEnv, \
    PyCRCTFLevel8Cluster1Env, PyCRCTFLevel8Cluster2Env, PyCRCTFLevel8Cluster3Env, PyCRCTFLevel8Cluster4Env, \
    PyCRCTFLevel8ClusterWithCosts1Env, PyCRCTFLevel8ClusterWithCosts2Env, PyCRCTFLevel8ClusterWithCosts3Env, \
    PyCRCTFLevel8ClusterWithCosts4Env

# ------ Random ----- #

from gym_pycr_ctf.envs.derived_envs.random.cluster.pycr_ctf_random_cluster_env import PyCRCTFRandomClusterBaseEnv, PyCRCTFRandomCluster1Env, \
    PyCRCTFRandomClusterWithCosts1Env, PyCRCTFRandomCluster2Env, PyCRCTFRandomCluster3Env, \
    PyCRCTFRandomCluster4Env, PyCRCTFRandomClusterWithCosts2Env, PyCRCTFRandomClusterWithCosts3Env, \
    PyCRCTFRandomClusterWithCosts4Env

from gym_pycr_ctf.envs.derived_envs.random.generated_simulation.pycr_ctf_random_gensim_env import \
    PyCRCTFRandomGeneratedSim1Env, PyCRCTFRandomGeneratedSimWithCosts1Env, PyCRCTFRandomGeneratedSim2Env, \
    PyCRCTFRandomGeneratedSimWithCosts2Env, PyCRCTFRandomGeneratedSim3Env, PyCRCTFRandomGeneratedSimWithCosts3Env, \
    PyCRCTFRandomGeneratedSim4Env, PyCRCTFRandomGeneratedSimWithCosts4Env

# ------ Random Many ----- #

from gym_pycr_ctf.envs.derived_envs.random_many.cluster.pycr_ctf_random_many_cluster_env import \
    PyCRCTFRandomManyCluster1Env, PyCRCTFRandomManyClusterWithCosts1Env

from gym_pycr_ctf.envs.derived_envs.random_many.generated_simulation.pycr_ctf_random_many_gensim_env import \
    PyCRCTFRandomManyGeneratedSim1Env

# ------ Multisim ----- #

from gym_pycr_ctf.envs.derived_envs.multisim.pycr_ctf_multisim_env import \
    PyCRCTFMultiSim1Env
