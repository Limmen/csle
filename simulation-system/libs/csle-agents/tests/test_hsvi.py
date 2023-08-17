import numpy as np
import pytest
import pytest_mock
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.hsvi.hsvi_agent import HSVIAgent
import csle_agents.constants.constants as agents_constants
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from gym_csle_stopping_game.dao.stopping_game_defender_pomdp_config import StoppingGameDefenderPomdpConfig
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.random_policy import RandomPolicy


def reduce_T(T, intrusion_start_prob: float = 0.1, intrusion_stop_prob: float = 0.05):
    """
    Reduces the transition tensor based on a given strategy

    :param T: the transition tensor to reduce
    :param intrusion_start_prob: the intrusion start probability
    :param intrusion_stop_prob: the intrusion stop probability
    :return: the reduced tensor
    """
    reduced_T = np.zeros((T.shape[0], T.shape[2], T.shape[3]))
    for i in range(T.shape[0]):
        for j in range(T.shape[2]):
            for k in range(T.shape[3]):
                if j == 0:
                    reduced_T[i][j][k] = T[i][0][j][k] * (1 - intrusion_start_prob) + T[i][1][j][
                        k] * intrusion_start_prob
                else:
                    reduced_T[i][j][k] = T[i][0][j][k] * (1 - intrusion_stop_prob) + T[i][1][j][k] * intrusion_stop_prob
    return reduced_T


def reduce_R(R, intrusion_start_prob: float = 0.1, intrusion_stop_prob: float = 0.05):
    """
    Reduces the reward tensor

    :param R: the reward tensor to reduce
    :param intrusion_start_prob: the intrusion start probability
    :param intrusion_stop_prob: the intrusion stop probability
    :return: the reduced tensor
    """
    reduced_R = np.zeros((R.shape[0], R.shape[2]))
    for i in range(R.shape[0]):
        for j in range(R.shape[2]):
            if j == 0:
                reduced_R[i][j] = R[i][0][j] * (1 - intrusion_start_prob) + R[i][1][j] * intrusion_start_prob
            else:
                reduced_R[i][j] = R[i][0][j] * (1 - intrusion_stop_prob) + R[i][1][j] * intrusion_stop_prob
    return reduced_R


def reduce_Z(Z, strategy):
    """
    Reduces the observation tensor based on a given strategy

    :param Z: the observation tensor to reduce
    :param strategy: the strategy to use for the reduction
    :return: the reduced observation tensor
    """
    reduced_Z = np.zeros((Z.shape[0], Z.shape[2], Z.shape[3]))
    for i in range(Z.shape[0]):
        for j in range(Z.shape[2]):
            for k in range(Z.shape[3]):
                reduced_Z[i][j][k] = Z[i][0][j][k] * strategy.probability(i, 0) + Z[i][1][j][k] * strategy.probability(
                    i, 1)
    return reduced_Z


class TestHSVISuite(object):
    """
    Test suite for the HSVIAgent
    """

    @pytest.fixture
    def experiment_config(self, example_simulation_config: SimulationEnvConfig) -> ExperimentConfig:
        """
        Fixture, which is run before every test. It sets up an example experiment config

        :param example_simulation_config: the example_simulation_config fixture
        :return: the example experiment config
        """
        simulation_env_config = example_simulation_config
        simulation_env_config.simulation_env_input_config.attacker_strategy = RandomPolicy(
            actions=simulation_env_config.joint_action_space_config.action_spaces[1].actions,
            player_type=PlayerType.ATTACKER, stage_policy_tensor=[
                [0.5, 0.5],
                [0.5, 0.5],
                [0.5, 0.5]
            ])
        T = np.array(simulation_env_config.transition_operator_config.transition_tensor)
        if len(T.shape) == 5:
            T = T[0]
        simulation_env_config.reward_function_config.reward_tensor = list(StoppingGameUtil.reward_tensor(
            R_INT=-10, R_COST=-10, R_SLA=0, R_ST=100, L=1))
        R = np.array(simulation_env_config.reward_function_config.reward_tensor)
        if len(R.shape) == 4:
            R = R[0]
        num_observations = 50
        Z = StoppingGameUtil.observation_tensor(len(range(0, num_observations)))
        if len(R.shape) == 5:
            Z = Z[0]
        T = reduce_T(T)
        R = reduce_R(R)
        Z = reduce_Z(Z, simulation_env_config.simulation_env_input_config.attacker_strategy)
        state_space = simulation_env_config.state_space_config.states_ids()
        action_space = simulation_env_config.joint_action_space_config.action_spaces[0].actions_ids()
        observation_space = list(range(0, num_observations + 1))
        experiment_config = ExperimentConfig(
            output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}hsvi_test",
            title="HSVI computation",
            random_seeds=[399], agent_type=AgentType.HSVI,
            log_every=1,
            hparams={
                agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=10,
                                                                name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                                descr="number of iterations to evaluate theta"),
                agents_constants.COMMON.EVAL_EVERY: HParam(value=1,
                                                           name=agents_constants.COMMON.EVAL_EVERY,
                                                           descr="how frequently to run evaluation"),
                agents_constants.COMMON.SAVE_EVERY: HParam(value=1000, name=agents_constants.COMMON.SAVE_EVERY,
                                                           descr="how frequently to save the model"),
                agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                    value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                    descr="confidence interval"),
                agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                    value=100, name=agents_constants.COMMON.RUNNING_AVERAGE,
                    descr="the number of samples to include when computing the running avg"),
                agents_constants.COMMON.GAMMA: HParam(
                    value=0.1, name=agents_constants.COMMON.GAMMA,
                    descr="the discount factor"),
                agents_constants.HSVI.TRANSITION_TENSOR: HParam(
                    value=list(T.tolist()), name=agents_constants.VI.TRANSITION_TENSOR,
                    descr="the transition tensor"),
                agents_constants.HSVI.REWARD_TENSOR: HParam(
                    value=list(R.tolist()), name=agents_constants.VI.REWARD_TENSOR,
                    descr="the reward tensor"),
                agents_constants.HSVI.EPSILON: HParam(
                    value=0.001, name=agents_constants.HSVI.EPSILON,
                    descr="the epsilon parameter of HSVI"),
                agents_constants.HSVI.INITIAL_BELIEF: HParam(
                    value=[1, 0, 0], name=agents_constants.HSVI.INITIAL_BELIEF,
                    descr="the initial belief"),
                agents_constants.HSVI.USE_LP: HParam(
                    value=False, name=agents_constants.HSVI.USE_LP,
                    descr="boolean flag whether to use LP for pruning or not"),
                agents_constants.HSVI.PRUNE_FREQUENCY: HParam(
                    value=100, name=agents_constants.HSVI.PRUNE_FREQUENCY,
                    descr="how frequently to prune alpha vectors"),
                agents_constants.HSVI.SIMULATION_FREQUENCY: HParam(
                    value=1, name=agents_constants.HSVI.SIMULATION_FREQUENCY,
                    descr="how frequently to run evaluation simulations"),
                agents_constants.HSVI.SIMULATE_HORIZON: HParam(
                    value=10, name=agents_constants.HSVI.SIMULATE_HORIZON,
                    descr="maximum time horizon for simulations"),
                agents_constants.HSVI.NUMBER_OF_SIMULATIONS: HParam(
                    value=1, name=agents_constants.HSVI.NUMBER_OF_SIMULATIONS,
                    descr="batch size for simulations"),
                agents_constants.HSVI.ACTION_SPACE: HParam(
                    value=action_space, name=agents_constants.HSVI.ACTION_SPACE,
                    descr="action space of the POMDP"),
                agents_constants.HSVI.STATE_SPACE: HParam(
                    value=state_space, name=agents_constants.HSVI.STATE_SPACE,
                    descr="state space of the POMDP"),
                agents_constants.HSVI.OBSERVATION_SPACE: HParam(
                    value=observation_space, name=agents_constants.HSVI.OBSERVATION_SPACE,
                    descr="observation space of the POMDP"),
                agents_constants.HSVI.OBSERVATION_TENSOR: HParam(
                    value=list(Z.tolist()), name=agents_constants.HSVI.OBSERVATION_TENSOR,
                    descr="observation tensor of the POMDP")
            },
            player_type=PlayerType.DEFENDER, player_idx=0
        )
        return experiment_config

    @pytest.fixture
    def pomdp_config(self) -> StoppingGameDefenderPomdpConfig:
        """
        Fixture, which is run before every test. It sets up an input POMDP config

        :return: The example config
        """
        L = 1
        R_INT = -5
        R_COST = -5
        R_SLA = 1
        R_ST = 5
        p = 0.1
        n = 100

        attacker_stage_strategy = np.zeros((3, 2))
        attacker_stage_strategy[0][0] = 0.9
        attacker_stage_strategy[0][1] = 0.1
        attacker_stage_strategy[1][0] = 0.9
        attacker_stage_strategy[1][1] = 0.1
        attacker_stage_strategy[2] = attacker_stage_strategy[1]

        stopping_game_config = StoppingGameConfig(
            A1=StoppingGameUtil.attacker_actions(), A2=StoppingGameUtil.defender_actions(), L=L, R_INT=R_INT,
            R_COST=R_COST,
            R_SLA=R_SLA, R_ST=R_ST, b1=np.array(list(StoppingGameUtil.b1())),
            save_dir="./results",
            T=StoppingGameUtil.transition_tensor(L=L, p=p),
            O=StoppingGameUtil.observation_space(n=n),
            Z=StoppingGameUtil.observation_tensor(n=n),
            R=StoppingGameUtil.reward_tensor(R_SLA=R_SLA, R_INT=R_INT, R_COST=R_COST, L=L, R_ST=R_ST),
            S=StoppingGameUtil.state_space(), env_name="csle-stopping-game-v1", checkpoint_traces_freq=100000,
            gamma=1)
        pomdp_config = StoppingGameDefenderPomdpConfig(
            stopping_game_config=stopping_game_config, stopping_game_name="csle-stopping-game-v1",
            attacker_strategy=RandomPolicy(actions=list(stopping_game_config.A2),
                                           player_type=PlayerType.ATTACKER,
                                           stage_policy_tensor=list(attacker_stage_strategy)),
            env_name="csle-stopping-game-pomdp-defender-v1")
        return pomdp_config

    def test_create_agent(self, mocker: pytest_mock.MockFixture, experiment_config: ExperimentConfig) -> None:
        """
        Tests creation of the HSVIAgent

        :return: None
        """
        simulation_env_config = mocker.MagicMock()
        HSVIAgent(simulation_env_config=simulation_env_config, experiment_config=experiment_config)

    def test_run_agent(self, mocker: pytest_mock.MockFixture, experiment_config: ExperimentConfig,
                       pomdp_config: StoppingGameDefenderPomdpConfig) -> None:
        """
        Tests running the agent

        :param mocker: object for mocking API calls
        :param experiment_config: the example experiment config
        :param pomdp_config: the example POMDP config
        :return: None
        """
        # Mock emulation and simulation configs
        emulation_env_config = mocker.MagicMock()
        simulation_env_config = mocker.MagicMock()

        # Set attributes of the mocks
        simulation_env_config.configure_mock(**{
            "name": "simulation-test-env", "gym_env_name": "csle-stopping-game-pomdp-defender-v1",
            "simulation_env_input_config": pomdp_config
        })
        emulation_env_config.configure_mock(**{
            "name": "emulation-test-env"
        })

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
        agent = HSVIAgent(simulation_env_config=simulation_env_config, experiment_config=experiment_config)
        experiment_execution = agent.train()
        assert experiment_execution is not None
        assert experiment_execution.descr != ""
        assert experiment_execution.id is not None
        assert experiment_execution.config == experiment_config
        assert agents_constants.COMMON.AVERAGE_RETURN in experiment_execution.result.plot_metrics
        assert agents_constants.COMMON.RUNNING_AVERAGE_RETURN in experiment_execution.result.plot_metrics
        for seed in experiment_config.random_seeds:
            assert seed in experiment_execution.result.all_metrics
            assert agents_constants.COMMON.AVERAGE_RETURN in experiment_execution.result.all_metrics[seed]
            assert agents_constants.COMMON.RUNNING_AVERAGE_RETURN in experiment_execution.result.all_metrics[seed]
