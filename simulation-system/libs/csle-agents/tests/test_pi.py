import numpy as np
import pytest
import pytest_mock
import random
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.pi.pi_agent import PIAgent
import csle_agents.constants.constants as agents_constants
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from gym_csle_stopping_game.dao.stopping_game_attacker_mdp_config import StoppingGameAttackerMdpConfig
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.random_policy import RandomPolicy


def reduce_T(T, strategy):
    """
    Reduces the transition tensor based on a given strategy

    :param T: the transition tensor to reduce
    :param strategy: the strategy to use for the reduction
    :return: the reduced transition tensor
    """
    reduced_T = np.zeros((T.shape[1], T.shape[2], T.shape[3]))
    for i in range(T.shape[1]):
        for j in range(T.shape[2]):
            for k in range(T.shape[3]):
                reduced_T[i][j][k] = T[0][i][j][k] * strategy.probability(j, 0) + T[1][i][j][k] * strategy.probability(
                    j, 1)
    return reduced_T


def reduce_R(R, strategy):
    """
    Reduces the reward tensor based on a given strategy

    :param R: the reward tensor
    :param strategy: the strategy to use for the reduction
    :return: the reduced tensor
    """
    reduced_R = np.zeros((R.shape[1], R.shape[2]))
    for i in range(R.shape[1]):
        for j in range(R.shape[2]):
            reduced_R[i][j] = R[0][i][j] * strategy.probability(i, 0) + R[1][i][j] * strategy.probability(i, 1)
    return reduced_R


class TestPISuite:
    """
    Test suite for the PIAgent
    """

    @pytest.fixture
    def experiment_config(self, example_simulation_config: SimulationEnvConfig) -> ExperimentConfig:
        """
        Fixture, which is run before every test. It sets up an example experiment config

        :param: example_simulation_config: the example_simulation_config fixture
        :return: the example experiment config
        """
        simulation_env_config = example_simulation_config
        simulation_env_config.simulation_env_input_config.defender_strategy = RandomPolicy(
            actions=simulation_env_config.joint_action_space_config.action_spaces[0].actions,
            player_type=PlayerType.DEFENDER, stage_policy_tensor=None)

        T = np.array(simulation_env_config.transition_operator_config.transition_tensor)
        if len(T.shape) == 5:
            T = T[0]
        num_states = len(simulation_env_config.state_space_config.states)
        R = np.array(simulation_env_config.reward_function_config.reward_tensor)
        if len(R.shape) == 4:
            R = R[0]
        num_actions = len(simulation_env_config.joint_action_space_config.action_spaces[1].actions)

        T = reduce_T(T, simulation_env_config.simulation_env_input_config.defender_strategy)
        R = -reduce_R(R, simulation_env_config.simulation_env_input_config.defender_strategy)

        initial_pi = np.zeros((num_states, num_actions))
        for s in range(num_states):
            a = random.choice(list(range(num_actions)))
            initial_pi[s][a] = 1

        experiment_config = ExperimentConfig(
            output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}pi_test",
            title="Policy iteration computation",
            random_seeds=[399], agent_type=AgentType.POLICY_ITERATION,
            log_every=1,
            hparams={
                agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=100,
                                                                name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                                descr="number of iterations to evaluate"),
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
                agents_constants.PI.TRANSITION_TENSOR: HParam(
                    value=list(T.tolist()), name=agents_constants.PI.TRANSITION_TENSOR,
                    descr="the transition tensor"),
                agents_constants.PI.REWARD_TENSOR: HParam(
                    value=list(R.tolist()), name=agents_constants.PI.REWARD_TENSOR,
                    descr="the reward tensor"),
                agents_constants.PI.NUM_STATES: HParam(
                    value=num_states, name=agents_constants.PI.NUM_STATES,
                    descr="the number of states"),
                agents_constants.PI.NUM_ACTIONS: HParam(
                    value=num_actions, name=agents_constants.PI.NUM_ACTIONS,
                    descr="the number of actions"),
                agents_constants.PI.N: HParam(
                    value=2, name=agents_constants.PI.N,
                    descr="the number of iterations"),
                agents_constants.PI.INITIAL_POLICY: HParam(
                    value=list(initial_pi.tolist()), name=agents_constants.PI.INITIAL_POLICY,
                    descr="the initial policy")
            },
            player_type=PlayerType.ATTACKER, player_idx=1
        )
        return experiment_config

    @pytest.fixture
    def mdp_config(self, example_simulation_config: SimulationEnvConfig) -> StoppingGameAttackerMdpConfig:
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
        mdp_config = StoppingGameAttackerMdpConfig(
            stopping_game_config=stopping_game_config, stopping_game_name="csle-stopping-game-v1",
            defender_strategy=RandomPolicy(
                actions=example_simulation_config.joint_action_space_config.action_spaces[0].actions,
                player_type=PlayerType.DEFENDER, stage_policy_tensor=None),
            env_name="csle-stopping-game-mdp-attacker-v1")
        return mdp_config

    def test_create_agent(self, mocker: pytest_mock.MockFixture, experiment_config: ExperimentConfig) -> None:
        """
        Tests creation of the PIAgent

        :return: None
        """
        simulation_env_config = mocker.MagicMock()
        PIAgent(simulation_env_config=simulation_env_config, experiment_config=experiment_config)

    def test_run_agent(self, mocker: pytest_mock.MockFixture, experiment_config: ExperimentConfig,
                       mdp_config: StoppingGameAttackerMdpConfig) -> None:
        """
        Tests running the agent

        :param mocker: object for mocking API calls
        :param experiment_config: the example experiment config
        :param mdp_config: the example MDP config

        :return: None
        """
        # Mock emulation and simulation configs
        emulation_env_config = mocker.MagicMock()
        simulation_env_config = mocker.MagicMock()

        # Set attributes of the mocks
        simulation_env_config.configure_mock(**{
            "name": "simulation-test-env", "gym_env_name": "csle-stopping-game-mdp-attacker-v1",
            "simulation_env_input_config": mdp_config
        })
        emulation_env_config.configure_mock(**{"name": "emulation-test-env"})

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
        agent = PIAgent(simulation_env_config=simulation_env_config, experiment_config=experiment_config)
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
