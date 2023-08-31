from csle_common.dao.training.alpha_vectors_policy import AlphaVectorsPolicy
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.state_type import StateType
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.dqn_policy import DQNPolicy
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.fnn_with_softmax_policy import FNNWithSoftmaxPolicy
from csle_common.dao.training.linear_tabular_policy import LinearTabularPolicy
from csle_common.dao.training.linear_threshold_stopping_policy import LinearThresholdStoppingPolicy
from csle_common.dao.training.tabular_policy import TabularPolicy
from csle_common.dao.training.mixed_linear_tabular import MixedLinearTabularPolicy
from csle_common.dao.training.hparam import HParam


class TestTrainingDaoSuite:
    """
    Test suite for training data access objects (DAOs)
    """

    def test_alpha_vectors_policy(self) -> None:
        """
        Tests creation and dict conversion of the AlphaVectorsPolicy DAO

        :return: None
        """

        action = Action(id=1, descr="test")
        states = State(id=1, name="test", descr="test1", state_type=StateType.TERMINAL)
        alpha_vectors_policy = AlphaVectorsPolicy(
            player_type=PlayerType.DEFENDER, actions=[action], alpha_vectors=[1, 2], transition_tensor=[1, 3],
            reward_tensor=[5, 6], states=[states], agent_type=AgentType.PPO, simulation_name="test", avg_R=0.3)

        assert isinstance(alpha_vectors_policy.to_dict(), dict)
        assert isinstance(AlphaVectorsPolicy.from_dict(alpha_vectors_policy.to_dict()),
                          AlphaVectorsPolicy)
        assert (AlphaVectorsPolicy.from_dict(alpha_vectors_policy.to_dict()).to_dict() ==
                alpha_vectors_policy.to_dict())
        assert (AlphaVectorsPolicy.from_dict(alpha_vectors_policy.to_dict()) ==
                alpha_vectors_policy)

    def test_dqn_policy(self) -> None:
        """
        Tests creation and dict conversion of the DQNPolicy DAO

        :return: None
        """

        hparams = dict()
        hparams["test"] = HParam(value=1, name="test", descr="test")
        experiment_config = ExperimentConfig(
            output_dir="test", title="test2", random_seeds=[1, 2, 3], agent_type=AgentType.RANDOM, hparams=hparams,
            log_every=10, player_type=PlayerType.ATTACKER, player_idx=0)
        actions = Action(id=1, descr="test")
        states = State(id=1, name="test", descr="test1", state_type=StateType.TERMINAL)
        dqn_policy = DQNPolicy(model=None, simulation_name="test", save_path="test/test",
                               player_type=PlayerType.ATTACKER, states=[states], actions=[actions], avg_R=0.6,
                               experiment_config=experiment_config)

        assert isinstance(dqn_policy.to_dict(), dict)
        assert isinstance(DQNPolicy.from_dict(dqn_policy.to_dict()),
                          DQNPolicy)
        assert (DQNPolicy.from_dict(dqn_policy.to_dict()).to_dict() ==
                dqn_policy.to_dict())
        assert (DQNPolicy.from_dict(dqn_policy.to_dict()) ==
                dqn_policy)

    def test_experiment_config(self) -> None:
        """
        Tests creation and dict conversion of the ExperimentConfig DAO

        :return: None
        """

        hparams = dict()
        hparams["test"] = HParam(value=1, name="test", descr="test")
        experiment_config = ExperimentConfig(
            output_dir="test", title="test2", random_seeds=[1, 2], agent_type=AgentType.HSVI, hparams=hparams,
            log_every=10, player_type=PlayerType.DEFENDER, player_idx=12)

        assert isinstance(experiment_config.to_dict(), dict)
        assert isinstance(ExperimentConfig.from_dict(experiment_config.to_dict()),
                          ExperimentConfig)
        assert (ExperimentConfig.from_dict(experiment_config.to_dict()).to_dict() ==
                experiment_config.to_dict())
        assert (ExperimentConfig.from_dict(experiment_config.to_dict()) ==
                experiment_config)

    def test_experiment_execution(self) -> None:
        """
        Tests creation and dict conversion of the ExperimentExecution DAO

        :return: None
        """

        hparams = dict()
        hparams["test"] = HParam(value=1, name="test", descr="test")
        experiment_config = ExperimentConfig(
            output_dir="test", title="test2", random_seeds=[1, 2], agent_type=AgentType.HSVI, hparams=hparams,
            log_every=10, player_type=PlayerType.DEFENDER, player_idx=12)
        experiment_execution = ExperimentExecution(
            config=experiment_config, result=ExperimentResult(), timestamp=10.10, emulation_name="test",
            simulation_name="test1", descr="test2", log_file_path="test/test")

        assert isinstance(experiment_execution.to_dict(), dict)
        assert isinstance(ExperimentExecution.from_dict(experiment_execution.to_dict()),
                          ExperimentExecution)
        assert (ExperimentExecution.from_dict(experiment_execution.to_dict()).to_dict() ==
                experiment_execution.to_dict())
        assert (ExperimentExecution.from_dict(experiment_execution.to_dict()) ==
                experiment_execution)

    def test_experiment_result(self) -> None:
        """
        Tests creation and dict conversion of the ExperimentResult DAO

        :return: None
        """

        experiment_result = ExperimentResult()

        assert isinstance(experiment_result.to_dict(), dict)
        assert isinstance(ExperimentResult.from_dict(experiment_result.to_dict()),
                          ExperimentResult)
        assert (ExperimentResult.from_dict(experiment_result.to_dict()).to_dict() ==
                experiment_result.to_dict())
        assert (ExperimentResult.from_dict(experiment_result.to_dict()) ==
                experiment_result)

    def test_fnn_with_softmax_policy(self) -> None:
        """
        Tests creation and dict conversion of the FNNWithSoftmaxPolicy DAO

        :return: None
        """

        actions = Action(id=1, descr="test")
        states = State(id=1, name="test", descr="test1", state_type=StateType.TERMINAL)
        hparams = dict()
        hparams["test"] = HParam(value=1, name="test", descr="test")
        experiment_config = ExperimentConfig(
            output_dir="test", title="test2", random_seeds=[1, 2], agent_type=AgentType.HSVI, hparams=hparams,
            log_every=10, player_type=PlayerType.DEFENDER, player_idx=12)
        fnn_with_softmax_policy = FNNWithSoftmaxPolicy(
            None, simulation_name="test", save_path="test/test", player_type=PlayerType.DEFENDER,
            states=[states], actions=[actions], experiment_config=experiment_config, avg_R=0.1, input_dim=100,
            output_dim=10)

        assert isinstance(fnn_with_softmax_policy.to_dict(), dict)
        assert isinstance(FNNWithSoftmaxPolicy.from_dict(fnn_with_softmax_policy.to_dict()),
                          FNNWithSoftmaxPolicy)
        assert (FNNWithSoftmaxPolicy.from_dict(fnn_with_softmax_policy.to_dict()).to_dict() ==
                fnn_with_softmax_policy.to_dict())
        assert (FNNWithSoftmaxPolicy.from_dict(fnn_with_softmax_policy.to_dict()) ==
                fnn_with_softmax_policy)

    def test_hparam(self) -> None:
        """
        Tests creation and dict conversion of the HParam DAO

        :return: None
        """

        hparam = HParam(value=10, name="test", descr="test2")

        assert isinstance(hparam.to_dict(), dict)
        assert isinstance(HParam.from_dict(hparam.to_dict()),
                          HParam)
        assert (HParam.from_dict(hparam.to_dict()).to_dict() ==
                hparam.to_dict())
        assert (HParam.from_dict(hparam.to_dict()) ==
                hparam)

    def test_linear_tabular_policy(self) -> None:
        """
        Tests creation and dict conversion of the LinearTabularPolicy DAO

        :return: None
        """

        actions = Action(id=1, descr="test")
        states = State(id=1, name="test", descr="test1", state_type=StateType.TERMINAL)
        hparams = dict()
        hparams["test"] = HParam(value=1, name="test", descr="test")
        experiment_config = ExperimentConfig(
            output_dir="test", title="test2", random_seeds=[1, 2], agent_type=AgentType.HSVI, hparams=hparams,
            log_every=10, player_type=PlayerType.DEFENDER, player_idx=12)
        stopping_policy = LinearThresholdStoppingPolicy(
            [0.1], simulation_name="test", L=1, states=[states], player_type=PlayerType.SELF_PLAY,
            actions=[actions], experiment_config=experiment_config, avg_R=0.2, agent_type=AgentType.RANDOM)
        action_policy = TabularPolicy(
            player_type=PlayerType.DEFENDER, actions=[actions], lookup_table=[[0.1]], agent_type=AgentType.HSVI,
            simulation_name="test1", avg_R=0.5)
        linear_tabular_policy = LinearTabularPolicy(
            stopping_policy=stopping_policy, action_policy=action_policy, player_type=PlayerType.DEFENDER,
            actions=[actions], avg_R=0.1, agent_type=AgentType.T_SPSA,
            states=[states], simulation_name="test2", experiment_config=experiment_config)

        assert isinstance(linear_tabular_policy.to_dict(), dict)
        assert isinstance(LinearTabularPolicy.from_dict(linear_tabular_policy.to_dict()),
                          LinearTabularPolicy)
        assert (LinearTabularPolicy.from_dict(linear_tabular_policy.to_dict()).to_dict() ==
                linear_tabular_policy.to_dict())
        assert (LinearTabularPolicy.from_dict(linear_tabular_policy.to_dict()) ==
                linear_tabular_policy)

    def test_linear_threshold_stopping_policy(self) -> None:
        """
        Tests creation and dict conversion of the LinearThresholdStoppingPolicy DAO

        :return: None
        """

        actions = Action(id=1, descr="test")
        states = State(id=1, name="test", descr="test1", state_type=StateType.TERMINAL)
        hparams = dict()
        hparams["test"] = HParam(value=1, name="test", descr="test")
        experiment_config = ExperimentConfig(
            output_dir="test", title="test2", random_seeds=[1, 2], agent_type=AgentType.HSVI, hparams=hparams,
            log_every=10, player_type=PlayerType.DEFENDER, player_idx=12)
        linear_threshold_stopping_policy = LinearThresholdStoppingPolicy(
            [0.1], simulation_name="test", L=1, states=[states], player_type=PlayerType.SELF_PLAY,
            actions=[actions], experiment_config=experiment_config, avg_R=0.2, agent_type=AgentType.RANDOM)

        assert isinstance(linear_threshold_stopping_policy.to_dict(), dict)
        assert isinstance(LinearThresholdStoppingPolicy.from_dict(linear_threshold_stopping_policy.to_dict()),
                          LinearThresholdStoppingPolicy)
        assert (LinearThresholdStoppingPolicy.from_dict(linear_threshold_stopping_policy.to_dict()).to_dict() ==
                linear_threshold_stopping_policy.to_dict())
        assert (LinearThresholdStoppingPolicy.from_dict(linear_threshold_stopping_policy.to_dict()) ==
                linear_threshold_stopping_policy)

    def test_mixed_linear_tabular(self) -> None:
        """
        Tests creation and dict conversion of the MixedLinearTabularPolicy DAO

        :return: None
        """

        hparams = dict()
        hparams["test"] = HParam(value=1, name="test", descr="test")
        experiment_config = ExperimentConfig(
            output_dir="test", title="test2", random_seeds=[1, 2], agent_type=AgentType.HSVI, hparams=hparams,
            log_every=10, player_type=PlayerType.DEFENDER, player_idx=12)
        states = State(id=1, name="test", descr="test1", state_type=StateType.TERMINAL)
        actions = Action(id=1, descr="test")
        mixed_linear_tabular_policy = MixedLinearTabularPolicy(
            simulation_name="test", player_type=PlayerType.DEFENDER, states=[states],
            actions=[actions], experiment_config=experiment_config, avg_R=0.9)

        assert isinstance(mixed_linear_tabular_policy.to_dict(), dict)
        assert isinstance(MixedLinearTabularPolicy.from_dict(mixed_linear_tabular_policy.to_dict()),
                          MixedLinearTabularPolicy)
        assert (MixedLinearTabularPolicy.from_dict(mixed_linear_tabular_policy.to_dict()).to_dict() ==
                mixed_linear_tabular_policy.to_dict())
        assert (MixedLinearTabularPolicy.from_dict(mixed_linear_tabular_policy.to_dict()) ==
                mixed_linear_tabular_policy)
