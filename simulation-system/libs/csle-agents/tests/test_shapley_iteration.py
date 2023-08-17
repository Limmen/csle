import numpy as np
import pytest
import pytest_mock
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.shapley_iteration.shapley_iteration_agent import ShapleyIterationAgent
import csle_agents.constants.constants as agents_constants
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from gym_csle_stopping_game.dao.stopping_game_defender_pomdp_config import StoppingGameDefenderPomdpConfig
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from csle_common.dao.training.random_policy import RandomPolicy
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig


class TestShapleyIterationSuite:
    """
    Test suite for the ShapleyIterationAgent
    """

    @pytest.fixture
    def experiment_config(self, example_simulation_config: SimulationEnvConfig) -> ExperimentConfig:
        """
        Fixture, which is run before every test. It sets up an example experiment config

        :param: example_simulation_config: the example_simulation_config fixture with an example simulation config
        :return: the example experiment config
        """
        simulation_env_config = example_simulation_config
        state_space = simulation_env_config.state_space_config.states_ids()
        action_space_player_1 = simulation_env_config.joint_action_space_config.action_spaces[0].actions_ids()
        action_space_player_2 = simulation_env_config.joint_action_space_config.action_spaces[1].actions_ids()
        experiment_config = ExperimentConfig(
            output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}shapley_iteration_test",
            title="Shapley iteration  training attacker and defender through self-play to approximate a Nash "
                  "equilibrium",
            random_seeds=[399, 98912], agent_type=AgentType.SHAPLEY_ITERATION,
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
                agents_constants.SHAPLEY_ITERATION.N: HParam(
                    value=100, name=agents_constants.SHAPLEY_ITERATION.N,
                    descr="the number of iterations of Shapley iteration"),
                agents_constants.SHAPLEY_ITERATION.DELTA: HParam(
                    value=0.001, name=agents_constants.SHAPLEY_ITERATION.DELTA,
                    descr="the delta threshold parameter for Shapley iteration"),
                agents_constants.SHAPLEY_ITERATION.TRANSITION_TENSOR: HParam(
                    value=simulation_env_config.transition_operator_config.transition_tensor[0],
                    name=agents_constants.COMMON.GAMMA,
                    descr="the transition tensor for Shapley iteration"),
                agents_constants.SHAPLEY_ITERATION.REWARD_TENSOR: HParam(
                    value=simulation_env_config.reward_function_config.reward_tensor[0],
                    name=agents_constants.SHAPLEY_ITERATION.REWARD_TENSOR,
                    descr="the reward tensor for Shapley iteration"),
                agents_constants.SHAPLEY_ITERATION.STATE_SPACE: HParam(
                    value=state_space,
                    name=agents_constants.SHAPLEY_ITERATION.STATE_SPACE,
                    descr="the state space for Shapley iteration"),
                agents_constants.SHAPLEY_ITERATION.ACTION_SPACE_PLAYER_1: HParam(
                    value=action_space_player_1,
                    name=agents_constants.SHAPLEY_ITERATION.ACTION_SPACE_PLAYER_1,
                    descr="the action space for player 1 in Shapley iteration"),
                agents_constants.SHAPLEY_ITERATION.ACTION_SPACE_PLAYER_2: HParam(
                    value=action_space_player_2,
                    name=agents_constants.SHAPLEY_ITERATION.ACTION_SPACE_PLAYER_2,
                    descr="the action space for player 2 in Shapley iteration")
            },
            player_type=PlayerType.SELF_PLAY, player_idx=1
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
        Tests creation of the ShapleyIerationAgent

        :return: None
        """
        simulation_env_config = mocker.MagicMock()
        ShapleyIterationAgent(simulation_env_config=simulation_env_config, experiment_config=experiment_config)

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
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.save_vector_policy', return_value=True)
        agent = ShapleyIterationAgent(simulation_env_config=simulation_env_config, experiment_config=experiment_config)
        experiment_execution = agent.train()
        assert experiment_execution is not None
        assert experiment_execution.descr != ""
        assert experiment_execution.id is not None
        assert experiment_execution.config == experiment_config
        for seed in experiment_config.random_seeds:
            assert seed in experiment_execution.result.all_metrics
