from typing import Tuple, Any, Dict
import numpy as np
import numpy.typing as npt
import pytest
import pytest_mock
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_agents.agents.hsvi_os_posg.hsvi_os_posg_agent import HSVIOSPOSGAgent
import csle_agents.constants.constants as agents_constants


def states() -> Tuple[npt.NDArray[Any], Dict[int, str]]:
    """
    :return: the set of states and a lookup dict
    """
    return np.array([0, 1]), {0: "NO_INTRUSION", 1: "INTRUSION", 2: "TERMINAL"}


def player_1_actions() -> Tuple[npt.NDArray[Any], Dict[int, str]]:
    """
    :return: the set of actions of player 1 and a lookup dict
    """
    return np.array([0, 1]), {0: "CONTINUE", 1: "STOP"}


def player_2_actions() -> Tuple[npt.NDArray[Any], Dict[int, str]]:
    """
    :return: the set of actions of player 2 and a lookup dict
    """
    return np.array([0, 1]), {0: "CONTINUE", 1: "STOP"}


def observations() -> Tuple[npt.NDArray[Any], Dict[int, str]]:
    """
    :return: the set of observations and a lookup dict
    """
    return np.array([0, 1, 2]), {0: "NO ALERT", 1: "ONE ALERT", 2: "TERMINAL"}


def observation_tensor() -> npt.NDArray[Any]:
    """
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


def reward_tensor() -> npt.NDArray[Any]:
    """
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


def transition_tensor() -> npt.NDArray[Any]:
    """
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


def initial_belief() -> npt.NDArray[Any]:
    """
    :return: the initial belief point
    """
    return np.array([1, 0])


class TestHSVISuite(object):
    """
    Test suite for the HSVIAgent
    """

    @pytest.fixture
    def experiment_config(self, example_simulation_config: SimulationEnvConfig) -> ExperimentConfig:
        """
        Fixture, which is run before every test. It sets up an example experiment config

        :param: example_simulation_config: the example_simulation_config fixture
        :return: the example experiment config
        """
        Z = observation_tensor()
        A1, _ = player_1_actions()
        A2, _ = player_2_actions()
        O, _ = observations()
        S, _ = states()
        b0 = initial_belief()
        simulation_env_config = example_simulation_config
        experiment_config = ExperimentConfig(
            output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}hsvi_os_posg_iteration_test",
            title="HSVI for OS-POSGs to approximate a Nash equilibrium",
            random_seeds=[399], agent_type=AgentType.HSVI_OS_POSG,
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
                    value=0.1, name=agents_constants.COMMON.GAMMA,
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
        return experiment_config

    def test_create_agent(self, mocker: pytest_mock.MockFixture, experiment_config: ExperimentConfig) -> None:
        """
        Tests creation of the HSVIOSPOSGAgent

        :return: None
        """
        simulation_env_config = mocker.MagicMock()
        HSVIOSPOSGAgent(simulation_env_config=simulation_env_config, experiment_config=experiment_config)

    def test_run_agent(self, mocker: pytest_mock.MockFixture, experiment_config: ExperimentConfig) -> None:
        """
        Tests running the agent

        :param mocker: object for mocking API calls
        :param experiment_config: the example experiment config

        :return: None
        """
        # Mock emulation and simulation configs
        simulation_env_config = mocker.MagicMock()

        # Mock metastore facade
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.save_training_job', return_value=True)
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.save_experiment_execution',
                     return_value=True)
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.update_training_job', return_value=True)
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.update_experiment_execution',
                     return_value=True)
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.save_simulation_trace', return_value=True)
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.save_multi_threshold_stopping_policy',
                     return_value=True)
        agent = HSVIOSPOSGAgent(simulation_env_config=simulation_env_config, experiment_config=experiment_config)
        experiment_execution = agent.train()
        assert experiment_execution is not None
        assert experiment_execution.descr != ""
        assert experiment_execution.id is not None
        assert experiment_execution.config == experiment_config
        for seed in experiment_config.random_seeds:
            assert seed in experiment_execution.result.all_metrics
