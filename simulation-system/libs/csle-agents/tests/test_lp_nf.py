import numpy as np
import pytest
import pytest_mock
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.lp_nf.linear_programming_normal_form_game_agent import LinearProgrammingNormalFormGameAgent
import csle_agents.constants.constants as agents_constants
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig


class TestLPNFSuite:
    """
    Test suite for the LPNFAgent
    """

    @pytest.fixture
    def experiment_config(self) -> ExperimentConfig:
        """
        Fixture, which is run before every test. It sets up an example experiment config

        :return: the example experiment config
        """
        A = np.array([
            [3, 3, 1, 4],
            [2, 5, 6, 3],
            [1, 0, 7, 0],
        ])
        A1 = list(range(3))
        A2 = list(range(4))
        experiment_config = ExperimentConfig(
            output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}fp_test",
            title="Linear programming for normal-form games to approximate a Nash equilibrium",
            random_seeds=[399], agent_type=AgentType.LINEAR_PROGRAMMING_NORMAL_FORM,
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
                    value=50, name=agents_constants.COMMON.MAX_ENV_STEPS,
                    descr="maximum number of steps in the environment (for envs with infinite horizon generally)"),
                agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                    value=40, name=agents_constants.COMMON.RUNNING_AVERAGE,
                    descr="the number of samples to include when computing the running avg"),
                agents_constants.COMMON.GAMMA: HParam(
                    value=0.99, name=agents_constants.COMMON.GAMMA,
                    descr="the discount factor gamma"),
                agents_constants.LP_FOR_NF_GAMES.PAYOFF_MATRIX: HParam(
                    value=list(A.tolist()), name=agents_constants.LP_FOR_NF_GAMES.PAYOFF_MATRIX,
                    descr="the payoff matrix"),
                agents_constants.LP_FOR_NF_GAMES.ACTION_SPACE_PLAYER_1: HParam(
                    value=A1, name=agents_constants.LP_FOR_NF_GAMES.ACTION_SPACE_PLAYER_1,
                    descr="the action space for player 1"),
                agents_constants.LP_FOR_NF_GAMES.ACTION_SPACE_PLAYER_2: HParam(
                    value=A2, name=agents_constants.LP_FOR_NF_GAMES.ACTION_SPACE_PLAYER_2,
                    descr="the action space for player 2")
            },
            player_type=PlayerType.SELF_PLAY, player_idx=1
        )
        return experiment_config

    def test_create_agent(self, mocker: pytest_mock.MockFixture, experiment_config: ExperimentConfig) -> None:
        """
        Tests creation of the LP-NF agent

        :return: None
        """
        simulation_env_config = mocker.MagicMock()
        LinearProgrammingNormalFormGameAgent(simulation_env_config=simulation_env_config,
                                             experiment_config=experiment_config)

    def test_run_agent(self, mocker: pytest_mock.MockFixture, experiment_config: ExperimentConfig,
                       example_simulation_config: SimulationEnvConfig) -> None:
        """
        Tests running the agent

        :param mocker: object for mocking API calls
        :param experiment_config: the example experiment config
        :param example_simulation_config: the example_simulation_config fixture

        :return: None
        """
        # Mock metastore facade
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.save_training_job', return_value=True)
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.save_experiment_execution',
                     return_value=True)
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.update_training_job', return_value=True)
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.update_experiment_execution',
                     return_value=True)
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.save_simulation_trace', return_value=True)
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.save_vector_policy', return_value=True)
        agent = LinearProgrammingNormalFormGameAgent(simulation_env_config=example_simulation_config,
                                                     experiment_config=experiment_config)
        experiment_execution = agent.train()
        assert experiment_execution is not None
        assert experiment_execution.descr != ""
        assert experiment_execution.id is not None
        assert experiment_execution.config == experiment_config
        for seed in experiment_config.random_seeds:
            assert seed in experiment_execution.result.all_metrics
