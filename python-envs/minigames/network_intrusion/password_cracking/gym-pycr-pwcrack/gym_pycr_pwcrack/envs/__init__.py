from gym_pycr_pwcrack.envs.pycr_pwcrack_env import PyCRPwCrackEnv, PyCrPwCrackLevel1Base, \
    PyCRPwCrackLevel1ClusterBaseEnv, PyCRPwCrackLevel1Sim1Env, PyCRPwCrackLevel1Cluster1Env, \
    PyCRPwCrackLevel1Cluster2Env, PyCRPwCrackLevel1Cluster3Env, PyCRPwCrackLevel1Cluster4Env, \
    PyCRPwCrackLevel2SimBaseEnv, PyCRPwCrackLevel2ClusterBaseEnv, PyCRPwCrackLevel2Cluster1Env, \
    PyCRPwCrackLevel1GeneratedSim1Env, PyCRPwCrackLevel2GeneratedSim1Env, PyCRPwCrackLevel2Sim1Env, \
    PyCRPwCrackLevel2Cluster2Env, PyCRPwCrackLevel2Cluster3Env, PyCRPwCrackLevel2Cluster4Env, \
    PyCRPwCrackLevel3ClusterBaseEnv, PyCRPwCrackLevel3Cluster1Env, PyCRPwCrackLevel3Cluster2Env, \
    PyCRPwCrackLevel3Cluster3Env, PyCRPwCrackLevel3Cluster4Env, PyCRPwCrackLevel1ClusterNoCache1Env, \
    PyCRPwCrackLevel1ClusterWithCosts1Env, PyCRPwCrackLevel1ClusterWithCosts2Env, PyCRPwCrackLevel1ClusterWithCosts3Env, \
    PyCRPwCrackLevel1ClusterWithCosts4Env, PyCRPwCrackLevel2ClusterWithCosts1Env, PyCRPwCrackLevel2ClusterWithCosts2Env, \
    PyCRPwCrackLevel2ClusterWithCosts3Env, PyCRPwCrackLevel2ClusterWithCosts4Env, PyCRPwCrackLevel3ClusterWithCosts1Env, \
    PyCRPwCrackLevel3ClusterWithCosts2Env, PyCRPwCrackLevel3ClusterWithCosts3Env, \
    PyCRPwCrackLevel3ClusterWithCosts4Env, PyCRPwCrackLevel1SimWithCosts1Env, \
    PyCRPwCrackLevel1GeneratedSimWithCosts1Env, PyCRPwCrackLevel2GeneratedSimWithCosts1Env, \
    PyCRPwCrackLevel2SimWithCosts1Env, PyCRPwCrackLevel1GeneratedSim2Env, PyCRPwCrackLevel1Sim2Env, \
    PyCRPwCrackLevel1SimWithCosts2Env, PyCRPwCrackLevel1Sim3Env, PyCRPwCrackLevel1SimWithCosts3Env, \
    PyCRPwCrackLevel1Sim4Env, PyCRPwCrackLevel1SimWithCosts4Env, PyCRPwCrackLevel1GeneratedSimWithCosts2Env, \
    PyCRPwCrackLevel1GeneratedSim3Env, PyCRPwCrackLevel1GeneratedSimWithCosts3Env, PyCRPwCrackLevel1GeneratedSim4Env, \
    PyCRPwCrackLevel1GeneratedSimWithCosts4Env, PyCRPwCrackLevel2GeneratedSim2Env, PyCRPwCrackLevel2GeneratedSimWithCosts2Env, \
    PyCRPwCrackLevel2GeneratedSim3Env, PyCRPwCrackLevel2GeneratedSimWithCosts3Env, PyCRPwCrackLevel2GeneratedSim4Env, \
    PyCRPwCrackLevel2GeneratedSimWithCosts4Env, PyCRPwCrackLevel4ClusterBaseEnv, PyCRPwCrackLevel4Cluster1Env, \
    PyCRPwCrackLevel4ClusterWithCosts1Env, PyCRPwCrackLevel4Cluster2Env, PyCRPwCrackLevel4Cluster3Env, \
    PyCRPwCrackLevel4Cluster4Env, PyCRPwCrackLevel4ClusterWithCosts2Env, PyCRPwCrackLevel4ClusterWithCosts3Env, \
    PyCRPwCrackLevel4ClusterWithCosts4Env, PyCRPwCrackLevel5ClusterBaseEnv, PyCRPwCrackLevel5Cluster1Env, \
    PyCRPwCrackLevel5ClusterWithCosts1Env, PyCRPwCrackLevel5Cluster2Env, PyCRPwCrackLevel5Cluster3Env, \
    PyCRPwCrackLevel5Cluster4Env, PyCRPwCrackLevel5ClusterWithCosts2Env, PyCRPwCrackLevel5ClusterWithCosts3Env, \
    PyCRPwCrackLevel5ClusterWithCosts4Env, PyCRPwCrackLevel6ClusterBaseEnv, PyCRPwCrackLevel6Cluster1Env, \
    PyCRPwCrackLevel6ClusterWithCosts1Env, PyCRPwCrackLevel6Cluster2Env, PyCRPwCrackLevel6Cluster3Env, \
    PyCRPwCrackLevel6Cluster4Env, PyCRPwCrackLevel6ClusterWithCosts2Env, PyCRPwCrackLevel6ClusterWithCosts3Env, \
    PyCRPwCrackLevel6ClusterWithCosts4Env, PyCRPwCrackRandomClusterBaseEnv, PyCRPwCrackRandomCluster1Env, \
    PyCRPwCrackRandomClusterWithCosts1Env, PyCRPwCrackRandomCluster2Env, PyCRPwCrackRandomCluster3Env, \
    PyCRPwCrackRandomCluster4Env, PyCRPwCrackRandomClusterWithCosts2Env, PyCRPwCrackRandomClusterWithCosts3Env, \
    PyCRPwCrackRandomClusterWithCosts4Env, PyCRPwCrackRandomManyCluster1Env, PyCRPwCrackRandomManyClusterWithCosts1Env, \
    PyCRPwCrackRandomGeneratedSim1Env