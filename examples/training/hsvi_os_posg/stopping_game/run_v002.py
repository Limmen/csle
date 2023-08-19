from typing import Tuple
import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.hsvi_os_posg.hsvi_os_posg_agent import HSVIOSPOSGAgent
import csle_agents.constants.constants as agents_constants


def states() -> Tuple[np.ndarray, dict]:
    """
    Returns the state space

    :return: the set of states and a lookup dict
    """
    return np.array([0, 1]), {0: "NO_INTRUSION", 1: "INTRUSION", 2: "TERMINAL"}


def player_1_actions() -> Tuple[np.ndarray, dict]:
    """
    Returns the action space of player 1

    :return: the set of actions of player 1 and a lookup dict
    """
    return np.array([0, 1]), {0: "CONTINUE", 1: "STOP"}


def player_2_actions() -> Tuple[np.ndarray, dict]:
    """
    Returns the action space of player 2

    :return: the set of actions of player 2 and a lookup dict
    """
    return np.array([0, 1]), {0: "CONTINUE", 1: "STOP"}


def observations() -> Tuple[np.ndarray, dict]:
    """
    Returns the observation space

    :return: the set of observations and a lookup dict
    """
    return np.array([0, 1, 2]), {0: "NO ALERT", 1: "ONE ALERT", 2: "TERMINAL"}


def observation_tensor() -> np.ndarray:
    """
    Returns the observation tensor

    :return:  a |A1|x|A2|x|S|x|O| tensor
    """
    O = np.array(
        [
            [
                [
                    [0.48, 0.48, 0.01],
                    [0.01, 0.01, 0.98]
                ],
                [
                    [0.01, 0.01, 0.98],
                    [0.01, 0.01, 0.98]
                ]
            ],
            [
                [
                    [0.01, 0.01, 0.98],
                    [0.01, 0.01, 0.98]
                ],
                [
                    [0.01, 0.01, 0.98],
                    [0.01, 0.01, 0.98]
                ]
            ]
        ]
    )

    return O


def reward_tensor() -> np.ndarray:
    """
    Returns the reward tensor

    :return: return a |A1|x|A2|x|S| tensor
    """
    R_ST = 20.0
    R_SLA = 5.0
    R_COST = -5.0
    R_INT = -10.0
    R = np.array(
        [
            [
                [R_SLA + R_INT, 0],
                [R_SLA, 0]
            ],
            [
                [R_COST + R_ST, 0],
                [R_COST, 0]
            ]
        ]
    )
    return R


def transition_tensor() -> np.ndarray:
    """
    Returns the transition tensor

    :return: a |A1|x|A2||S|^2 tensor
    """
    p = 0.01
    return np.array(
        [
            [
                [
                    [1 - p, p],
                    [0, 1]
                ],
                [
                    [0, 1],
                    [0, 1]
                ]
            ],
            [
                [
                    [0, 1],
                    [0, 1]
                ],
                [
                    [0, 1],
                    [0, 1]
                ]
            ]
        ]
    )


def initial_belief() -> np.ndarray:
    """
    Returns the initial belief

    :return: the initial belief point
    """
    return np.array([1, 0])


if __name__ == '__main__':
    Z = observation_tensor()
    R = reward_tensor()
    T = transition_tensor()
    A1, _ = player_1_actions()
    A2, _ = player_2_actions()
    O, _ = observations()
    S, _ = states()
    b0 = initial_belief()
    simulation_name = "csle-stopping-game-002"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}hsvi_os_posg_iteration_test",
        title="HSVI for OS-POSGs to approximate a Nash equilibrium",
        random_seeds=[399, 98912], agent_type=AgentType.HSVI_OS_POSG,
        log_every=1, br_log_every=5000,
        hparams={
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=1,
                                                            name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="number of iterations to evaluate theta"),
            agents_constants.COMMON.SAVE_EVERY: HParam(
                value=10000, name=agents_constants.COMMON.SAVE_EVERY, descr="how frequently to save the model"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval"),
            agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                value=500, name=agents_constants.COMMON.MAX_ENV_STEPS,
                descr="maximum number of steps in the environment (for envs with infinite horizon generally)"),
            agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                value=40, name=agents_constants.COMMON.RUNNING_AVERAGE,
                descr="the number of samples to include when computing the running avg"),
            agents_constants.COMMON.GAMMA: HParam(
                value=0.99, name=agents_constants.COMMON.GAMMA,
                descr="the discount factor gamma"),
            agents_constants.HSVI_OS_POSG.TRANSITION_TENSOR: HParam(
                value=simulation_env_config.transition_operator_config.transition_tensor[0],
                name=agents_constants.COMMON.GAMMA,
                descr="the transition tensor for HSVI for OS-POSGs iteration"),
            agents_constants.HSVI_OS_POSG.REWARD_TENSOR: HParam(
                value=simulation_env_config.reward_function_config.reward_tensor[0],
                name=agents_constants.HSVI_OS_POSG.REWARD_TENSOR,
                descr="the reward tensor for HSVI for OS-POSGs iteration"),
            agents_constants.HSVI_OS_POSG.STATE_SPACE: HParam(
                value=list(S.tolist()),
                name=agents_constants.HSVI_OS_POSG.STATE_SPACE,
                descr="the state space for HSVI for OS-POSGs iteration"),
            agents_constants.HSVI_OS_POSG.ACTION_SPACE_PLAYER_1: HParam(
                value=list(A1.tolist()),
                name=agents_constants.HSVI_OS_POSG.ACTION_SPACE_PLAYER_1,
                descr="the action space for player 1 in HSVI for OS-POSGs iteration"),
            agents_constants.HSVI_OS_POSG.ACTION_SPACE_PLAYER_2: HParam(
                value=list(A2.tolist()),
                name=agents_constants.HSVI_OS_POSG.ACTION_SPACE_PLAYER_2,
                descr="the action space for player 2 in HSVI for OS-POSGs iteration"),
            agents_constants.HSVI_OS_POSG.OBSERVATION_SPACE: HParam(
                value=list(O.tolist()),
                name=agents_constants.HSVI_OS_POSG.OBSERVATION_SPACE,
                descr="the observation space"),
            agents_constants.HSVI_OS_POSG.OBSERVATION_FUNCTION: HParam(
                value=list(Z.tolist()),
                name=agents_constants.HSVI_OS_POSG.OBSERVATION_FUNCTION,
                descr="the observation space"),
            agents_constants.HSVI_OS_POSG.EPSILON: HParam(
                value=0.01,
                name=agents_constants.HSVI_OS_POSG.EPSILON,
                descr="the epsilon parameter for HSVI"),
            agents_constants.HSVI_OS_POSG.PRUNE_FREQUENCY: HParam(
                value=100,
                name=agents_constants.HSVI_OS_POSG.PRUNE_FREQUENCY,
                descr="prune frequency for HSVI"),
            agents_constants.HSVI_OS_POSG.INITIAL_BELIEF: HParam(
                value=list(b0.tolist()),
                name=agents_constants.HSVI_OS_POSG.INITIAL_BELIEF,
                descr="the initial belief")
        },
        player_type=PlayerType.SELF_PLAY, player_idx=1
    )
    agent = HSVIOSPOSGAgent(simulation_env_config=simulation_env_config,
                            experiment_config=experiment_config, save_to_metastore=True)
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        MetastoreFacade.save_alpha_vec_policy(alpha_vec_policy=policy)
