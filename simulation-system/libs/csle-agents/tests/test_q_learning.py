import numpy as np
import pytest
import pytest_mock
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.simulation_config.initial_state_distribution_config import InitialStateDistributionConfig
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.q_learning.q_learning_agent import QLearningAgent
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
import csle_agents.constants.constants as agents_constants
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from gym_csle_stopping_game.dao.stopping_game_attacker_mdp_config import StoppingGameAttackerMdpConfig
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from csle_common.dao.training.random_policy import RandomPolicy


class TestQLearningSuite:
    """
    Test suite for the QLearningAgent
    """

    @pytest.fixture
    def experiment_config(self, example_simulation_config: SimulationEnvConfig) -> ExperimentConfig:
        """
        Fixture, which is run before every test. It sets up an example experiment config

        :param: example_simulation_config: the example_simulation_config fixture with an example simulation config
        :return: the example experiment config
        """
        simulation_env_config = example_simulation_config
        simulation_env_config.simulation_env_input_config.defender_strategy = RandomPolicy(
            actions=simulation_env_config.joint_action_space_config.action_spaces[0].actions,
            player_type=PlayerType.DEFENDER, stage_policy_tensor=None)
        A = simulation_env_config.joint_action_space_config.action_spaces[1].actions_ids()
        S = simulation_env_config.state_space_config.states_ids()

        experiment_config = ExperimentConfig(
            output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}q_learning_test",
            title="Q-learning",
            random_seeds=[399], agent_type=AgentType.Q_LEARNING,
            log_every=1,
            hparams={
                agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=2,
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
                    value=0.99, name=agents_constants.COMMON.GAMMA,
                    descr="the discount factor"),
                agents_constants.Q_LEARNING.S: HParam(
                    value=S, name=agents_constants.Q_LEARNING.S,
                    descr="the state spaec"),
                agents_constants.Q_LEARNING.A: HParam(
                    value=A, name=agents_constants.Q_LEARNING.A,
                    descr="the action space"),
                agents_constants.Q_LEARNING.EPSILON: HParam(
                    value=0.05, name=agents_constants.Q_LEARNING.EPSILON,
                    descr="the exploration parameter"),
                agents_constants.Q_LEARNING.N: HParam(
                    value=2, name=agents_constants.Q_LEARNING.N,
                    descr="the number of iterations"),
                agents_constants.Q_LEARNING.EPSILON_DECAY_RATE: HParam(
                    value=0.99999, name=agents_constants.Q_LEARNING.EPSILON_DECAY_RATE,
                    descr="epsilon decay rate")
            },
            player_type=PlayerType.ATTACKER, player_idx=1
        )
        return experiment_config

    @pytest.fixture
    def mdp_config(self, example_simulation_config) -> StoppingGameAttackerMdpConfig:
        """
        Fixture, which is run before every test. It sets up an input MDP config

        :param: example_simulation_config: the example_simulation_config fixture with an example simulation config
        :return: The example config
        """
        L = 1
        R_INT = -5
        R_COST = -5
        R_SLA = 1
        R_ST = 5
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
            T=StoppingGameUtil.transition_tensor(L=L),
            O=StoppingGameUtil.observation_space(n=n),
            Z=StoppingGameUtil.observation_tensor(n=n),
            R=StoppingGameUtil.reward_tensor(R_SLA=R_SLA, R_INT=R_INT, R_COST=R_COST, L=L, R_ST=R_ST),
            S=StoppingGameUtil.state_space(), env_name="csle-stopping-game-v1", checkpoint_traces_freq=100000,
            gamma=1)
        mdp_config = StoppingGameAttackerMdpConfig(
            stopping_game_config=stopping_game_config, stopping_game_name="csle-stopping-game-v1",
            defender_strategy=RandomPolicy(
                actions=example_simulation_config.joint_action_space_config.action_spaces[0].actions,
                player_type=PlayerType.DEFENDER, stage_policy_tensor=None),
            env_name="csle-stopping-game-mdp-attacker-v1")
        return mdp_config

    @pytest.fixture
    def initial_state_distribution_config(self, example_simulation_config: SimulationEnvConfig) -> \
            InitialStateDistributionConfig:
        """
        Fixture, which is run before every test. It sets up an initial state distribution config

        :param: example_simulation_config: the example_simulation_config fixture with an example simulation config
        :return: The example config
        """
        initial_state_distribution_config = example_simulation_config.initial_state_distribution_config
        return initial_state_distribution_config

    def test_create_agent(self, mocker: pytest_mock.MockFixture, experiment_config: ExperimentConfig) -> None:
        """
        Tests creation of the QLearningAgent

        :return: None
        """
        simulation_env_config = mocker.MagicMock()
        QLearningAgent(simulation_env_config=simulation_env_config, experiment_config=experiment_config)

    def test_run_agent(self, mocker: pytest_mock.MockFixture, experiment_config: ExperimentConfig,
                       mdp_config: StoppingGameAttackerMdpConfig,
                       initial_state_distribution_config: InitialStateDistributionConfig) -> None:
        """
        Tests running the agent

        :param mocker: object for mocking API calls
        :param experiment_config: the example experiment config
        :param mdp_config: the example MDP config
        :param initial_state_distribution_config: the example initial state distribiution config

        :return: None
        """
        # Mock emulation and simulation configs
        emulation_env_config = mocker.MagicMock()
        simulation_env_config = mocker.MagicMock()

        # Set attributes of the mocks
        simulation_env_config.configure_mock(**{
            "name": "simulation-test-env", "gym_env_name": "csle-stopping-game-mdp-attacker-v1",
            "simulation_env_input_config": mdp_config,
            "initial_state_distribution_config": initial_state_distribution_config
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
        agent = QLearningAgent(simulation_env_config=simulation_env_config, experiment_config=experiment_config)
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
