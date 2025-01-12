import io
import json
import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.cross_entropy.cross_entropy_agent import CrossEntropyAgent
import csle_agents.constants.constants as agents_constants
from csle_common.dao.training.policy_type import PolicyType
from csle_agents.common.objective_type import ObjectiveType
from gym_csle_apt_game.dao.apt_game_config import AptGameConfig
from gym_csle_apt_game.util.apt_game_util import AptGameUtil
from gym_csle_apt_game.envs.apt_game_mdp_attacker_env import AptGameMdpAttackerEnv

if __name__ == '__main__':
    emulation_name = "csle-level9-070"
    emulation_env_config = MetastoreFacade.get_emulation_by_name(emulation_name)
    if emulation_env_config is None:
        raise ValueError(f"Could not find an emulation environment with the name: {emulation_name}")
    simulation_name = "csle-apt-mdp-attacker-001"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}cross_entropy_test", title="Cross-entropy test",
        random_seeds=[399, 98912, 999],
        agent_type=AgentType.CROSS_ENTROPY,
        log_every=1,
        hparams={
            agents_constants.CROSS_ENTROPY.N: HParam(value=50, name=constants.T_SPSA.N,
                                                     descr="the number of training iterations"),
            agents_constants.CROSS_ENTROPY.L: HParam(value=1, name=agents_constants.CROSS_ENTROPY.L,
                                                     descr="the number of stop actions"),
            agents_constants.CROSS_ENTROPY.K: HParam(value=20, name=agents_constants.CROSS_ENTROPY.K,
                                                     descr="the number of samples in each iteration of CE"),
            agents_constants.CROSS_ENTROPY.LAMB: HParam(value=0.15, name=agents_constants.CROSS_ENTROPY.K,
                                                        descr="the number of samples to keep in each iteration of CE"),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=10, name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="number of iterations to evaluate theta"),
            agents_constants.CROSS_ENTROPY.THETA1: HParam(value=[-3],
                                                          name=agents_constants.CROSS_ENTROPY.THETA1,
                                                          descr="initial thresholds"),
            agents_constants.COMMON.SAVE_EVERY: HParam(value=1000, name=agents_constants.COMMON.SAVE_EVERY,
                                                       descr="how frequently to save the model"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval"),
            agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                value=30, name=agents_constants.COMMON.MAX_ENV_STEPS,
                descr="maximum number of steps in the environment (for envs with infinite horizon generally)"),
            agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                value=100, name=agents_constants.COMMON.RUNNING_AVERAGE,
                descr="the number of samples to include when computing the running avg"),
            agents_constants.COMMON.GAMMA: HParam(
                value=0.99, name=agents_constants.COMMON.GAMMA,
                descr="the discount factor"),
            agents_constants.CROSS_ENTROPY.POLICY_TYPE: HParam(
                value=PolicyType.MULTI_THRESHOLD, name=agents_constants.CROSS_ENTROPY.POLICY_TYPE,
                descr="policy type for the execution"),
            agents_constants.CROSS_ENTROPY.OBJECTIVE_TYPE: HParam(
                value=ObjectiveType.MAX, name=agents_constants.CROSS_ENTROPY.OBJECTIVE_TYPE,
                descr="Objective type")
        },
        player_type=PlayerType.ATTACKER, player_idx=1
    )
    N = 10
    filename = "/home/kim/nyu_data_dict_3"
    with io.open(filename, 'r') as f:
        json_str = f.read()
    data_dict = json.loads(json_str)
    Z = []
    no_intrusion_min_val = max([0, int(data_dict["no_intrusion_alerts_means"][10] -
                                       data_dict["no_intrusion_alerts_stds"][10])])
    no_intrusion_max_val = data_dict["no_intrusion_alerts_means"][10] + data_dict["no_intrusion_alerts_stds"][10]
    no_intrusion_range = (no_intrusion_min_val, no_intrusion_max_val)
    intrusion_min_val = max([0, int(data_dict["intrusion_alerts_means"][10] * (1 + N * 0.2) -
                                    data_dict["intrusion_alerts_stds"][10])])
    intrusion_max_val = data_dict["intrusion_alerts_means"][10] * (1 + N * 0.2) + data_dict["intrusion_alerts_stds"][10]
    max_intrusion_range = (intrusion_min_val, intrusion_max_val)
    O = list(range(int(no_intrusion_range[0]), int(max_intrusion_range[1])))
    no_intrusion_dist = []
    for i in O:
        if i in list(range(int(no_intrusion_range[0]), int(no_intrusion_range[1]))):
            no_intrusion_dist.append(round(1 / (no_intrusion_range[1] - no_intrusion_range[0]), 10))
        else:
            no_intrusion_dist.append(0)
    Z.append(list(np.array(no_intrusion_dist) / sum(no_intrusion_dist)))
    for s in range(1, N + 1):
        intrusion_dist = []
        min_val = max([0, int(data_dict["intrusion_alerts_means"][10] * (1 + s * 0.2) -
                              data_dict["intrusion_alerts_stds"][10])])
        max_val = data_dict["intrusion_alerts_means"][10] * (1 + s * 0.2) + data_dict["intrusion_alerts_stds"][10]
        intrusion_range = (min_val, max_val)
        for i in O:
            if i in range(int(intrusion_range[0]), int(intrusion_range[1])):
                intrusion_dist.append(round(1 / (intrusion_range[1] - intrusion_range[0]), 10))
            else:
                intrusion_dist.append(0)
        Z.append(list(np.array(intrusion_dist) / sum(intrusion_dist)))

    p_a = 0.1
    C = AptGameUtil.cost_tensor(N=N)
    T = AptGameUtil.transition_tensor(N=N, p_a=p_a)
    S = AptGameUtil.state_space(N=N)
    A1 = AptGameUtil.defender_actions()
    A2 = AptGameUtil.attacker_actions()
    b1 = AptGameUtil.b1(N=N)
    gamma = 0.99
    input_config = AptGameConfig(
        T=T, O=O, Z=Z, C=C, S=S, A1=A1, A2=A2, N=N, p_a=p_a, save_dir=".", checkpoint_traces_freq=10000, gamma=gamma,
        b1=b1, env_name="csle-apt-game-mdp-attacker-v1")
    simulation_env_config.simulation_env_input_config.apt_game_config = input_config
    env = AptGameMdpAttackerEnv(config=simulation_env_config.simulation_env_input_config)
    agent = CrossEntropyAgent(emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config,
                              experiment_config=experiment_config, save_to_metastore=True, env=env)
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        if experiment_config.hparams[agents_constants.CROSS_ENTROPY.POLICY_TYPE].value == \
                PolicyType.MULTI_THRESHOLD:
            MetastoreFacade.save_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
        elif experiment_config.hparams[agents_constants.CROSS_ENTROPY.POLICY_TYPE].value \
                == PolicyType.LINEAR_THRESHOLD:
            MetastoreFacade.save_linear_threshold_stopping_policy(linear_threshold_stopping_policy=policy)
        else:
            raise ValueError("Policy type: "
                             f"{experiment_config.hparams[agents_constants.CROSS_ENTROPY.POLICY_TYPE].value} "
                             f"not recognized for cross entropy")
