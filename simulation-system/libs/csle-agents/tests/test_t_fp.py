import pytest
import pytest_mock
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.t_fp.t_fp_agent import TFPAgent
from csle_common.dao.training.policy_type import PolicyType
import csle_agents.constants.constants as agents_constants
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_agents.common.objective_type import ObjectiveType


class TestTFPSuite:
    """
    Test suite for the TFPAgent
    """

    @pytest.fixture
    def experiment_config(self) -> ExperimentConfig:
        """
        Fixture, which is run before every test. It sets up an example experiment config

        :return: the example experiment config
        """
        experiment_config = ExperimentConfig(
            output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}tfp_test",
            title="T-FP training attacker and defender through self-play to approximate a Nash equilibrium",
            random_seeds=[399], agent_type=AgentType.T_FP,
            log_every=1, br_log_every=5000,
            hparams={
                constants.T_SPSA.N: HParam(
                    value=2, name=constants.T_SPSA.N,
                    descr="the number of training iterations to learn best response with T-SPSA"),
                constants.T_SPSA.c: HParam(
                    value=10, name=constants.T_SPSA.c,
                    descr="scalar coefficient for determining perturbation sizes in T-SPSA for best-response learning"),
                constants.T_SPSA.a: HParam(
                    value=1, name=constants.T_SPSA.a,
                    descr="scalar coefficient for determining gradient step sizes in T-SPSA for best-response "
                          "learning"),
                constants.T_SPSA.A: HParam(
                    value=100, name=constants.T_SPSA.A,
                    descr="scalar coefficient for determining gradient step sizes in T-SPSA for best-response "
                          "learning"),
                constants.T_SPSA.POLICY_TYPE: HParam(
                    value=PolicyType.MULTI_THRESHOLD, name=constants.T_SPSA.POLICY_TYPE,
                    descr="policy type in T-SPSA"),
                constants.T_SPSA.LAMBDA: HParam(
                    value=0.602, name=constants.T_SPSA.LAMBDA,
                    descr="scalar coefficient for determining perturbation sizes in T-SPSA for best-response learning"),
                constants.T_SPSA.EPSILON: HParam(
                    value=0.101, name=constants.T_SPSA.EPSILON,
                    descr="scalar coefficient for determining gradient step sizes in T-SPSA for best-response "
                          "learning"),
                agents_constants.T_FP.N_2: HParam(
                    value=2, name=agents_constants.T_FP.N_2,
                    descr="the number of self-play training iterations of T-FP"),
                constants.T_SPSA.L: HParam(value=3, name=constants.T_SPSA.L,
                                           descr="the number of stop actions"),
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
                constants.T_SPSA.GRADIENT_BATCH_SIZE: HParam(
                    value=1, name=constants.T_SPSA.GRADIENT_BATCH_SIZE,
                    descr="the batch size of the gradient estimator"),
                agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                    value=40, name=agents_constants.COMMON.RUNNING_AVERAGE,
                    descr="the number of samples to include when computing the running avg"),
                agents_constants.T_FP.BEST_RESPONSE_EVALUATION_ITERATIONS: HParam(
                    value=5, name=agents_constants.T_FP.BEST_RESPONSE_EVALUATION_ITERATIONS,
                    descr="number of iterations to evaluate best response strategies when calculating exploitability"),
                agents_constants.COMMON.GAMMA: HParam(
                    value=0.99, name=agents_constants.COMMON.GAMMA,
                    descr="the discount factor gamma"),
                agents_constants.T_FP.EQUILIBRIUM_STRATEGIES_EVALUATION_ITERATIONS: HParam(
                    value=5, name=agents_constants.T_FP.EQUILIBRIUM_STRATEGIES_EVALUATION_ITERATIONS,
                    descr="number of iterations to evaluate equilibrium strategies in each iteration"),
                constants.T_SPSA.OBJECTIVE_TYPE: HParam(
                    value=ObjectiveType.MIN, name=constants.T_SPSA.OBJECTIVE_TYPE,
                    descr="Objective type")
            },
            player_type=PlayerType.ATTACKER, player_idx=1
        )
        return experiment_config

    def test_create_agent(self, mocker: pytest_mock.MockFixture, experiment_config: ExperimentConfig,
                          example_attacker_simulation_config: SimulationEnvConfig,
                          example_defender_simulation_config: SimulationEnvConfig) -> None:
        """
        Tests creation of the TFPAgent

        :param mocker: the mocker object
        :param experiment_config: the experiment confi
        :param example_attacker_simulation_config: the simulation config for the attacker
        :param example_defender_simulation_config: the simulation config for the defender
        :return: None
        """
        emulation_env_config = mocker.MagicMock()
        TFPAgent(emulation_env_config=emulation_env_config,
                 attacker_simulation_env_config=example_attacker_simulation_config,
                 defender_simulation_env_config=example_defender_simulation_config, experiment_config=experiment_config)

    def test_run_agent(self, mocker: pytest_mock.MockFixture, experiment_config: ExperimentConfig,
                       example_attacker_simulation_config: SimulationEnvConfig,
                       example_defender_simulation_config: SimulationEnvConfig) -> None:
        """
        Tests running the agent

        :param mocker: object for mocking API calls
        :param experiment_config: the example experiment config
        :param example_attacker_simulation_config: the simulation config for the attacker
        :param example_defender_simulation_config: the simulation config for the defender

        :return: None
        """
        # Mock emulation and simulation configs
        emulation_env_config = mocker.MagicMock()

        # Set attributes of the mocks
        emulation_env_config.configure_mock(**{
            "name": "emulation-test-env"
        })
        # Mock metastore facade
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.save_training_job', return_value=True)
        mocker.patch(
            'csle_common.metastore.metastore_facade.MetastoreFacade.get_training_job_config',
            return_value=TrainingJobConfig(simulation_env_name="", experiment_config=experiment_config,
                                           progress_percentage=0.0, pid=1, experiment_result=None,
                                           emulation_env_name="", simulation_traces=[], num_cached_traces=0,
                                           log_file_path="", descr="", physical_host_ip="")
        )
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.save_experiment_execution',
                     return_value=True)
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.update_training_job', return_value=True)
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.remove_training_job', return_value=True)
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.update_experiment_execution',
                     return_value=True)
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.save_simulation_trace', return_value=True)
        mocker.patch('csle_common.metastore.metastore_facade.MetastoreFacade.save_multi_threshold_stopping_policy',
                     return_value=True)
        agent = TFPAgent(emulation_env_config=emulation_env_config,
                         attacker_simulation_env_config=example_attacker_simulation_config,
                         defender_simulation_env_config=example_defender_simulation_config,
                         experiment_config=experiment_config)
        experiment_execution = agent.train()
        assert experiment_execution is not None
        assert experiment_execution.descr != ""
        assert experiment_execution.id is not None
        assert experiment_execution.config == experiment_config
        for seed in experiment_config.random_seeds:
            assert seed in experiment_execution.result.all_metrics
