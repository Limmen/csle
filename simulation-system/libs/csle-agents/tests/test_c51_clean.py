import numpy as np
import pytest
import pytest_mock
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.c51_clean.c51_clean_agent import C51CleanAgent
import csle_agents.constants.constants as agents_constants
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from gym_csle_stopping_game.dao.stopping_game_defender_pomdp_config import StoppingGameDefenderPomdpConfig
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from csle_common.dao.training.random_policy import RandomPolicy


class TestC51CleanAgentSuite:
    """
    Test suite for the C51CleanAgent
    """

    @pytest.fixture
    def experiment_config(self) -> ExperimentConfig:
        """
        Fixture, which is run before every test. It sets up an example experiment config

        :return: the example experiment config
        """
        experiment_config = ExperimentConfig(
            output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}ppo_test",
            title="C51_CLEAN test", random_seeds=[399, 98912, 999], agent_type=AgentType.C51_CLEAN,
            log_every=1,
            hparams={
                constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER: HParam(
                    value=7, name=constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER,
                    descr="neurons per hidden layer of the policy network"),
                constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS: HParam(
                    value=4, name=constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS,
                    descr="number of layers of the policy network"),
                agents_constants.C51_CLEAN.EXP_FRAC: HParam(value=0.5, name=agents_constants.C51_CLEAN.EXP_FRAC,
                                                            descr="the fraction of `total-timesteps` "
                                                                  "it takes from start-e to go end-e"),
                agents_constants.C51_CLEAN.TAU: HParam(value=1.0, name=agents_constants.C51_CLEAN.TAU,
                                                       descr="target network update rate"),
                agents_constants.COMMON.BATCH_SIZE: HParam(value=1, name=agents_constants.COMMON.BATCH_SIZE,
                                                           descr="batch size for updates"),
                agents_constants.C51_CLEAN.LEARNING_STARTS: HParam(
                    value=10, name=agents_constants.C51_CLEAN.LEARNING_STARTS, descr="timestep to start learning"),
                agents_constants.C51_CLEAN.TRAIN_FREQ: HParam(
                    value=10, name=agents_constants.C51_CLEAN.TRAIN_FREQ, descr="the frequency of training"),
                agents_constants.C51_CLEAN.T_N_FREQ: HParam(
                    value=500, name=agents_constants.C51_CLEAN.T_N_FREQ,
                    descr="the batch size of sample from the reply memory"),
                agents_constants.C51_CLEAN.BUFFER_SIZE: HParam(
                    value=1000, name=agents_constants.C51_CLEAN.BUFFER_SIZE, descr="the replay memory buffer size"),
                agents_constants.C51_CLEAN.SAVE_MODEL: HParam(
                    value=False, name=agents_constants.C51_CLEAN.SAVE_MODEL,
                    descr="decision param for model saving"),
                agents_constants.COMMON.LEARNING_RATE: HParam(
                    value=2.4e-5, name=agents_constants.COMMON.LEARNING_RATE,
                    descr="learning rate for updating the policy"),
                agents_constants.C51_CLEAN.NUM_STEPS: HParam(
                    value=164, name=agents_constants.C51_CLEAN.NUM_STEPS, descr="number of steps in each time step"),
                constants.NEURAL_NETWORKS.DEVICE: HParam(
                    value="cpu", name=constants.NEURAL_NETWORKS.DEVICE, descr="the device to train on (cpu or cuda:x)"),
                agents_constants.COMMON.NUM_PARALLEL_ENVS: HParam(
                    value=1, name=agents_constants.COMMON.NUM_PARALLEL_ENVS,
                    descr="the nunmber of parallel environments for training"),
                agents_constants.C51_CLEAN.CLIP_VLOSS: HParam(
                    value=True, name=agents_constants.C51_CLEAN.CLIP_VLOSS, descr="the clip-vloss"),
                agents_constants.COMMON.GAMMA: HParam(
                    value=0.99, name=agents_constants.COMMON.GAMMA, descr="the discount factor"),
                agents_constants.C51_CLEAN.NORM_ADV: HParam(
                    value=0.5, name=agents_constants.C51_CLEAN.NORM_ADV, descr="norm_av param value"),
                agents_constants.COMMON.NUM_TRAINING_TIMESTEPS: HParam(
                    value=int(100), name=agents_constants.COMMON.NUM_TRAINING_TIMESTEPS,
                    descr="number of timesteps to train"),
                agents_constants.COMMON.EVAL_EVERY: HParam(
                    value=1, name=agents_constants.COMMON.EVAL_EVERY, descr="training iterations between evaluations"),
                agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(
                    value=100, name=agents_constants.COMMON.EVAL_BATCH_SIZE, descr="the batch size for evaluation"),
                agents_constants.COMMON.SAVE_EVERY: HParam(
                    value=10000, name=agents_constants.COMMON.SAVE_EVERY, descr="how frequently to save the model"),
                agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                    value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL, descr="confidence interval"),
                agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                    value=500, name=agents_constants.COMMON.MAX_ENV_STEPS,
                    descr="maximum number of steps in the environment (for envs with infinite horizon generally)"),
                agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                    value=100, name=agents_constants.COMMON.RUNNING_AVERAGE,
                    descr="the number of samples to include when computing the running avg"),
                agents_constants.COMMON.L: HParam(
                    value=1, name=agents_constants.COMMON.L, descr="the number of stop actions"),
                agents_constants.C51_CLEAN.N_ATOMS: HParam(
                    value=101, name=agents_constants.C51_CLEAN.N_ATOMS,
                    descr="the number of atoms"),
                agents_constants.C51_CLEAN.V_MIN: HParam(
                    value=-100, name=agents_constants.C51_CLEAN.V_MIN,
                    descr="the return lower bound"),
                agents_constants.C51_CLEAN.V_MAX: HParam(
                    value=100, name=agents_constants.C51_CLEAN.V_MAX,
                    descr="the return upper bound"),
                agents_constants.C51_CLEAN.START_EXPLORATION_RATE: HParam(
                    value=1, name=agents_constants.C51_CLEAN.START_EXPLORATION_RATE,
                    descr="the initial exploration rate"),
                agents_constants.C51_CLEAN.END_EXPLORATION_RATE: HParam(
                    value=0.05, name=agents_constants.C51_CLEAN.END_EXPLORATION_RATE,
                    descr="the final exploration rate")
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
        pomdp_config = StoppingGameDefenderPomdpConfig(
            stopping_game_config=stopping_game_config, stopping_game_name="csle-stopping-game-v1",
            attacker_strategy=RandomPolicy(actions=list(stopping_game_config.A2),
                                           player_type=PlayerType.ATTACKER,
                                           stage_policy_tensor=list(attacker_stage_strategy)),
            env_name="csle-stopping-game-pomdp-defender-v1")

        return pomdp_config

    def test_create_agent(self, mocker: pytest_mock.MockFixture, experiment_config: ExperimentConfig,
                          pomdp_config: StoppingGameDefenderPomdpConfig) -> None:
        """
        Tests creation of the C51CleanAgent

        :param mocker:  object for mocking API calls
        :param experiment_config: the example experiment config
        :param pomdp_config: the example POMDP config
        :return:
        """
        emulation_env_config = mocker.MagicMock()
        simulation_env_config = mocker.MagicMock()
        simulation_env_config.configure_mock(**{
            "name": "simulation-test-env", "gym_env_name": "csle-stopping-game-pomdp-defender-v1",
            "simulation_env_input_config": pomdp_config
        })

        C51CleanAgent(emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config,
                      experiment_config=experiment_config)

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
                     return_value=True),
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.save_dqn_policy', return_value=True)
        agent = C51CleanAgent(emulation_env_config=emulation_env_config,
                              simulation_env_config=simulation_env_config,
                              experiment_config=experiment_config)
        experiment_execution = agent.train()
        assert experiment_execution is not None
        assert experiment_execution.descr != ""
        assert experiment_execution.id is not None
        assert experiment_execution.config == experiment_config
        assert agents_constants.COMMON.AVERAGE_RETURN in experiment_execution.result.plot_metrics
        for seed in experiment_config.random_seeds:
            assert seed in experiment_execution.result.all_metrics
            assert agents_constants.COMMON.AVERAGE_RETURN in experiment_execution.result.all_metrics[seed]
