import numpy as np
from scipy.stats import norm
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
import csle_agents.constants.constants as agents_constants
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from sklearn.mixture import GaussianMixture
from csle_common.dao.training.mixed_multi_threshold_stopping_policy import MixedMultiThresholdStoppingPolicy
from csle_agents.agents.t_spsa.t_spsa_agent import TSPSAAgent
from csle_common.dao.training.policy_type import PolicyType
from csle_agents.common.objective_type import ObjectiveType


def get_obs_tensor():
    """
    Utility function to get the observation tensor from a given emulation statistic

    :return: the emulation statistic
    """
    model = MetastoreFacade.get_emulation_statistic(id=1)
    model.compute_descriptive_statistics_and_distributions()
    intrusion_counts = model.conditionals_counts[constants.SYSTEM_IDENTIFICATION.INTRUSION_CONDITIONAL][
        "alerts_weighted_by_priority"]
    no_intrusion_counts = model.conditionals_counts[constants.SYSTEM_IDENTIFICATION.NO_INTRUSION_CONDITIONAL][
        "alerts_weighted_by_priority"]
    intrusion_probs = model.conditionals_probs[constants.SYSTEM_IDENTIFICATION.INTRUSION_CONDITIONAL][
        "alerts_weighted_by_priority"]
    no_intrusion_probs = model.conditionals_probs[constants.SYSTEM_IDENTIFICATION.NO_INTRUSION_CONDITIONAL][
        "alerts_weighted_by_priority"]
    X_intrusion = []
    X_intrusion_prob = []
    for val, count in intrusion_counts.items():
        for j in range(count):
            X_intrusion.append([val])
    for val, prob_intrusion in intrusion_probs.items():
        X_intrusion_prob.append(prob_intrusion)
    X_intrusion = np.array(X_intrusion)

    X_no_intrusion = []
    X_no_intrusion_prob = []

    for val, count in no_intrusion_counts.items():
        for j in range(count):
            X_no_intrusion.append(val)

    X_no_intrusion_2 = []
    for x in X_no_intrusion:
        X_no_intrusion_2.append([x])
    X_no_intrusion = np.array(X_no_intrusion_2)

    for val, prob_intrusion in no_intrusion_probs.items():
        X_no_intrusion_prob.append(prob_intrusion)
    X_no_intrusion = np.array(X_no_intrusion)
    X_no_intrusion_prob = np.array(X_no_intrusion_prob)

    gmm_intrusion = GaussianMixture(n_components=3).fit(X_intrusion)
    gmm_no_intrusion = GaussianMixture(n_components=2).fit(X_no_intrusion)
    gmm_intrusion_probs = []
    gmm_no_intrusion_probs = []
    zero_prob_intrusion = 0
    zero_prob_no_intrusion = 0
    for i in range(-8000, 1):
        for weight, mean, covar in zip(gmm_intrusion.weights_, gmm_intrusion.means_, gmm_intrusion.covariances_):
            zero_prob_intrusion += weight * norm.pdf(i, mean, np.sqrt(covar)).ravel()[0]
        for weight, mean, covar in zip(gmm_no_intrusion.weights_, gmm_no_intrusion.means_,
                                       gmm_no_intrusion.covariances_):
            zero_prob_no_intrusion += weight * norm.pdf(i, mean, np.sqrt(covar)).ravel()[0]
    gmm_intrusion_probs.append(zero_prob_intrusion)
    gmm_no_intrusion_probs.append(zero_prob_no_intrusion)

    for i in range(1, 12000):
        prob_intrusion = 0
        prob_no_intrusion = 0
        for weight, mean, covar in zip(gmm_intrusion.weights_, gmm_intrusion.means_, gmm_intrusion.covariances_):
            prob_intrusion += weight * norm.pdf(i, mean, np.sqrt(covar)).ravel()[0]
        for weight, mean, covar in zip(gmm_no_intrusion.weights_, gmm_no_intrusion.means_,
                                       gmm_no_intrusion.covariances_):
            prob_no_intrusion += weight * norm.pdf(i, mean, np.sqrt(covar)).ravel()[0]
        gmm_intrusion_probs.append(prob_intrusion)
        gmm_no_intrusion_probs.append(prob_no_intrusion)
    O = list(range(0, 12000))
    print(round(sum(gmm_intrusion_probs), 3))
    print(round(sum(gmm_no_intrusion_probs), 3))
    terminal_dist = np.zeros(len(gmm_intrusion_probs))
    terminal_dist[-1] = 1
    Z = np.array(
        [
            [
                [
                    gmm_no_intrusion_probs,
                    gmm_intrusion_probs,
                    terminal_dist
                ],
                [
                    gmm_no_intrusion_probs,
                    gmm_intrusion_probs,
                    terminal_dist
                ],
            ],
            [
                [
                    gmm_no_intrusion_probs,
                    gmm_intrusion_probs,
                    terminal_dist
                ],
                [
                    gmm_no_intrusion_probs,
                    gmm_intrusion_probs,
                    terminal_dist
                ],
            ]
        ]
    )
    return Z, np.array(O)


if __name__ == '__main__':
    emulation_env_name = "csle-level9-070"
    emulation_env_config = MetastoreFacade.get_emulation_by_name(emulation_env_name)
    if emulation_env_config is None:
        raise ValueError(f"Could not find an emulation with name: {emulation_env_name}")
    simulation_name = "csle-stopping-mdp-attacker-001"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}tspsa_test",
        title="T-SPSA training attacker to learn 2L thresholds",
        random_seeds=[52132199, 98912], agent_type=AgentType.T_SPSA,
        log_every=1,
        hparams={
            constants.T_SPSA.N: HParam(
                value=500, name=constants.T_SPSA.N,
                descr="the number of training iterations"),
            constants.T_SPSA.c: HParam(
                value=10, name=constants.T_SPSA.c,
                descr="scalar coefficient for determining perturbation sizes in T-SPSA"),
            constants.T_SPSA.a: HParam(
                value=1, name=constants.T_SPSA.a,
                descr="scalar coefficient for determining gradient step sizes in T-SPSA"),
            constants.T_SPSA.A: HParam(
                value=100, name=constants.T_SPSA.A,
                descr="scalar coefficient for determining gradient step sizes in T-SPSA"),
            constants.T_SPSA.LAMBDA: HParam(
                value=0.602, name=constants.T_SPSA.LAMBDA,
                descr="scalar coefficient for determining perturbation sizes in T-SPSA"),
            constants.T_SPSA.EPSILON: HParam(
                value=0.101, name=constants.T_SPSA.EPSILON,
                descr="scalar coefficient for determining gradient step sizes in T-SPSA"),
            constants.T_SPSA.L: HParam(value=3, name=constants.T_SPSA.L,
                                       descr="the number of stop actions"),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=5,
                                                            name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="number of iterations to evaluate theta"),
            agents_constants.COMMON.SAVE_EVERY: HParam(value=1000, name=agents_constants.COMMON.SAVE_EVERY,
                                                       descr="how frequently to save the model"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval"),
            agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                value=100, name=agents_constants.COMMON.MAX_ENV_STEPS,
                descr="maximum number of steps in the environment (for envs with infinite horizon generally)"),
            constants.T_SPSA.GRADIENT_BATCH_SIZE: HParam(
                value=1, name=constants.T_SPSA.GRADIENT_BATCH_SIZE,
                descr="the batch size of the gradient estimator"),
            agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                value=100, name=agents_constants.COMMON.RUNNING_AVERAGE,
                descr="the number of samples to include when computing the running avg"),
            agents_constants.COMMON.GAMMA: HParam(
                value=0.99, name=agents_constants.COMMON.GAMMA,
                descr="the discount factor gamma"),
            constants.T_SPSA.POLICY_TYPE: HParam(
                value=PolicyType.MULTI_THRESHOLD, name=constants.T_SPSA.POLICY_TYPE,
                descr="policy type in T-SPSA"),
            constants.T_SPSA.OBJECTIVE_TYPE: HParam(
                value=ObjectiveType.MAX, name=constants.T_SPSA.OBJECTIVE_TYPE,
                descr="Objective type")
        },
        player_type=PlayerType.ATTACKER, player_idx=1
    )
    simulation_env_config.simulation_env_input_config.defender_strategy = MixedMultiThresholdStoppingPolicy(
        actions=simulation_env_config.joint_action_space_config.action_spaces[0].actions,
        simulation_name=simulation_env_config.name,
        L=simulation_env_config.simulation_env_input_config.stopping_game_config.L,
        states=simulation_env_config.state_space_config.states, player_type=PlayerType.DEFENDER,
        experiment_config=experiment_config, avg_R=-1, agent_type=AgentType.NONE,
        defender_Theta=[
            [[0.01], [1.0]],
            [[0.01], [1.0]],
            [[0.01], [1.0]]], attacker_Theta=[])
    simulation_env_config.simulation_env_input_config.stopping_game_config.R = list(StoppingGameUtil.reward_tensor(
        R_INT=-1, R_COST=-2, R_SLA=0, R_ST=20, L=3))
    simulation_env_config.simulation_env_input_config.stopping_game_config.d_b1 = np.array([0.99, 0.01, 0])
    Z, O = get_obs_tensor()
    simulation_env_config.simulation_env_input_config.stopping_game_config.Z = Z
    simulation_env_config.simulation_env_input_config.stopping_game_config.O = O
    simulation_env_config.simulation_env_input_config.stopping_game_config.gamma = 0.99
    simulation_env_config.simulation_env_input_config.stopping_game_config.L = 3

    agent = TSPSAAgent(emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config,
                       experiment_config=experiment_config)
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        MetastoreFacade.save_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
