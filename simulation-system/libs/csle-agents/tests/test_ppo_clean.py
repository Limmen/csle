import numpy as np
import pytest
import pytest_mock
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.ppo_clean.ppo_clean_agent import PPOCleanAgent
import csle_agents.constants.constants as agents_constants
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from gym_csle_stopping_game.dao.stopping_game_defender_pomdp_config import StoppingGameDefenderPomdpConfig
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from csle_common.dao.training.random_policy import RandomPolicy


class TestPPOCleanAgentSuite:
    """
    Test suite for the PPOCleanAgent
    """

    @pytest.fixture
    def experiment_config(self) -> ExperimentConfig:
        """
        Fixture, which is run before every test. It sets up an example experiment config

        :return: the example experiment config
        """
        experiment_config = ExperimentConfig(
            output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}ppo_test",
            title="PPO_clean test", random_seeds=[399], agent_type=AgentType.PPO_CLEAN,
            log_every=1,
            hparams={
                constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER: HParam(
                    value=64, name=constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER,
                    descr="neurons per hidden layer of the policy network"),
                constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS: HParam(
                    value=4, name=constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS,
                    descr="number of layers of the policy network"),
                agents_constants.COMMON.BATCH_SIZE: HParam(value=8, name=agents_constants.COMMON.BATCH_SIZE,
                                                           descr="batch size for updates"),
                agents_constants.COMMON.LEARNING_RATE: HParam(value=2.4e-5,
                                                              name=agents_constants.COMMON.LEARNING_RATE,
                                                              descr="learning rate for updating the policy"),
                agents_constants.PPO_CLEAN.NUM_STEPS: HParam(value=32,
                                                             name=agents_constants.PPO_CLEAN.NUM_STEPS,
                                                             descr="number of steps in each iteration"),
                agents_constants.PPO_CLEAN.ANNEAL_LR: HParam(value=True,
                                                             name=agents_constants.PPO_CLEAN.ANNEAL_LR,
                                                             descr="anneal learning rate for updating the policy"),
                constants.NEURAL_NETWORKS.DEVICE: HParam(value="cpu",
                                                         name=constants.NEURAL_NETWORKS.DEVICE,
                                                         descr="the device to train on (cpu or cuda:x)"),
                agents_constants.COMMON.NUM_PARALLEL_ENVS: HParam(
                    value=1, name=agents_constants.COMMON.NUM_PARALLEL_ENVS,
                    descr="the nunmber of parallel environments for training"),
                agents_constants.PPO_CLEAN.CLIP_VLOSS: HParam(
                    value=True, name=agents_constants.PPO_CLEAN.CLIP_VLOSS, descr="the clip-vloss"),
                agents_constants.COMMON.GAMMA: HParam(
                    value=1, name=agents_constants.COMMON.GAMMA, descr="the discount factor"),
                agents_constants.PPO_CLEAN.GAE_LAMBDA: HParam(
                    value=0.95, name=agents_constants.PPO_CLEAN.GAE_LAMBDA, descr="the GAE weighting term"),
                agents_constants.PPO_CLEAN.CLIP_RANGE: HParam(
                    value=0.2, name=agents_constants.PPO_CLEAN.CLIP_RANGE, descr="the clip range for PPO"),
                agents_constants.PPO_CLEAN.CLIP_RANGE_VF: HParam(
                    value=0.5, name=agents_constants.PPO_CLEAN.CLIP_RANGE_VF,
                    descr="the clip range for PPO-update of the value network"),
                agents_constants.PPO_CLEAN.ENT_COEF: HParam(
                    value=0.01, name=agents_constants.PPO_CLEAN.ENT_COEF,
                    descr="the entropy coefficient for exploration"),
                agents_constants.PPO_CLEAN.VF_COEF: HParam(value=0.5, name=agents_constants.PPO.VF_COEF,
                                                           descr="the coefficient of the value network for the loss"),
                agents_constants.PPO_CLEAN.NUM_MINIBATCHES: HParam(value=4,
                                                                   name=agents_constants.PPO_CLEAN.NUM_MINIBATCHES,
                                                                   descr="the number of minibatches"),
                agents_constants.PPO_CLEAN.MAX_GRAD_NORM: HParam(
                    value=0.5, name=agents_constants.PPO_CLEAN.MAX_GRAD_NORM, descr="the maximum allows gradient norm"),
                agents_constants.PPO_CLEAN.NORM_ADV: HParam(
                    value=0.5, name=agents_constants.PPO_CLEAN.NORM_ADV, descr="norm_av param value"),
                agents_constants.PPO_CLEAN.UPDATE_EPOCHS: HParam(
                    value=4, name=agents_constants.PPO_CLEAN.UPDATE_EPOCHS, descr="value of update_epochs"),
                agents_constants.PPO_CLEAN.TARGET_KL: HParam(value=-1,
                                                             name=agents_constants.PPO_CLEAN.TARGET_KL,
                                                             descr="the target kl"),
                agents_constants.PPO_CLEAN.CUDA: HParam(value=False, name=agents_constants.PPO_CLEAN.TARGET_KL,
                                                        descr="boolean flag indicating whether GPU should be used"),
                agents_constants.COMMON.NUM_TRAINING_TIMESTEPS: HParam(
                    value=int(100), name=agents_constants.COMMON.NUM_TRAINING_TIMESTEPS,
                    descr="number of timesteps to train"),
                agents_constants.COMMON.EVAL_EVERY: HParam(value=1, name=agents_constants.COMMON.EVAL_EVERY,
                                                           descr="training iterations between evaluations"),
                agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=100, name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                                descr="the batch size for evaluation"),
                agents_constants.COMMON.SAVE_EVERY: HParam(value=10000, name=agents_constants.COMMON.SAVE_EVERY,
                                                           descr="how frequently to save the model"),
                agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                    value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                    descr="confidence interval"),
                agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                    value=500, name=agents_constants.COMMON.MAX_ENV_STEPS,
                    descr="maximum number of steps in the environment (for envs with infinite horizon generally)"),
                agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                    value=100, name=agents_constants.COMMON.RUNNING_AVERAGE,
                    descr="the number of samples to include when computing the running avg"),
                agents_constants.COMMON.L: HParam(value=3, name=agents_constants.COMMON.L,
                                                  descr="the number of stop actions")
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
        Tests creation of the PPOCleanAgent

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
        PPOCleanAgent(emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config,
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
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.save_ppo_policy', return_value=True)
        agent = PPOCleanAgent(emulation_env_config=emulation_env_config,
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
