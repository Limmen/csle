from csle_common.dao.training.alpha_vectors_policy import AlphaVectorsPolicy
from csle_common.dao.training.dqn_policy import DQNPolicy
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.fnn_with_softmax_policy import FNNWithSoftmaxPolicy
from csle_common.dao.training.linear_tabular_policy import LinearTabularPolicy
from csle_common.dao.training.linear_threshold_stopping_policy import LinearThresholdStoppingPolicy
from csle_common.dao.training.tabular_policy import TabularPolicy
from csle_common.dao.training.mixed_linear_tabular import MixedLinearTabularPolicy
from csle_common.dao.training.mixed_ppo_policy import MixedPPOPolicy
from csle_common.dao.training.ppo_policy import PPOPolicy
from csle_common.dao.training.random_policy import RandomPolicy
from csle_common.dao.training.vector_policy import VectorPolicy
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.mixed_multi_threshold_stopping_policy import MixedMultiThresholdStoppingPolicy
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy


class TestTrainingDaoSuite:
    """
    Test suite for training data access objects (DAOs)
    """

    def test_alpha_vectors_policy(self, example_alpha_vectors_policy: AlphaVectorsPolicy) -> None:
        """
        Tests creation and dict conversion of the AlphaVectorsPolicy DAO

        :param example_alpha_vectors_policy: an example AlphaVectorsPolicy
        :return: None
        """
        assert isinstance(example_alpha_vectors_policy.to_dict(), dict)
        assert isinstance(AlphaVectorsPolicy.from_dict(example_alpha_vectors_policy.to_dict()), AlphaVectorsPolicy)
        assert (AlphaVectorsPolicy.from_dict(example_alpha_vectors_policy.to_dict()).to_dict() ==
                example_alpha_vectors_policy.to_dict())
        assert AlphaVectorsPolicy.from_dict(example_alpha_vectors_policy.to_dict()) == example_alpha_vectors_policy

    def test_dqn_policy(self, example_dqn_policy: DQNPolicy) -> None:
        """
        Tests creation and dict conversion of the DQNPolicy DAO

        :param example_dqn_policy: an example DQNPolicy
        :return: None
        """
        assert isinstance(example_dqn_policy.to_dict(), dict)
        assert isinstance(DQNPolicy.from_dict(example_dqn_policy.to_dict()), DQNPolicy)
        assert DQNPolicy.from_dict(example_dqn_policy.to_dict()).to_dict() == example_dqn_policy.to_dict()
        assert DQNPolicy.from_dict(example_dqn_policy.to_dict()) == example_dqn_policy

    def test_experiment_config(self, example_experiment_config: ExperimentConfig) -> None:
        """
        Tests creation and dict conversion of the ExperimentConfig DAO

        :param example_experiment_config: an example ExperimentConfig
        :return: None
        """
        assert isinstance(example_experiment_config.to_dict(), dict)
        assert isinstance(ExperimentConfig.from_dict(example_experiment_config.to_dict()), ExperimentConfig)
        assert ExperimentConfig.from_dict(example_experiment_config.to_dict()).to_dict() == \
               example_experiment_config.to_dict()
        assert ExperimentConfig.from_dict(example_experiment_config.to_dict()) == example_experiment_config

    def test_experiment_execution(self, example_experiment_execution: ExperimentExecution) -> None:
        """
        Tests creation and dict conversion of the ExperimentExecution DAO

        :param example_experiment_execution: an example ExperimentExecution
        :return: None
        """
        assert isinstance(example_experiment_execution.to_dict(), dict)
        assert isinstance(ExperimentExecution.from_dict(example_experiment_execution.to_dict()), ExperimentExecution)
        assert (ExperimentExecution.from_dict(example_experiment_execution.to_dict()).to_dict() ==
                example_experiment_execution.to_dict())
        assert ExperimentExecution.from_dict(example_experiment_execution.to_dict()) == example_experiment_execution

    def test_experiment_result(self, example_experiment_result: ExperimentResult) -> None:
        """
        Tests creation and dict conversion of the ExperimentResult DAO

        :param example_experiment_result: an example ExperimentResult
        :return: None
        """
        assert isinstance(example_experiment_result.to_dict(), dict)
        assert isinstance(ExperimentResult.from_dict(example_experiment_result.to_dict()), ExperimentResult)
        assert ExperimentResult.from_dict(example_experiment_result.to_dict()).to_dict() \
               == example_experiment_result.to_dict()
        assert ExperimentResult.from_dict(example_experiment_result.to_dict()) == example_experiment_result

    def test_fnn_with_softmax_policy(self, example_fnn_with_softmax_policy: FNNWithSoftmaxPolicy) -> None:
        """
        Tests creation and dict conversion of the FNNWithSoftmaxPolicy DAO

        :param example_fnn_with_softmax_policy: an example FNNWithSoftmaxPolicy
        :return: None
        """
        assert isinstance(example_fnn_with_softmax_policy.to_dict(), dict)
        assert isinstance(FNNWithSoftmaxPolicy.from_dict(example_fnn_with_softmax_policy.to_dict()),
                          FNNWithSoftmaxPolicy)
        assert (FNNWithSoftmaxPolicy.from_dict(example_fnn_with_softmax_policy.to_dict()).to_dict() ==
                example_fnn_with_softmax_policy.to_dict())
        assert FNNWithSoftmaxPolicy.from_dict(example_fnn_with_softmax_policy.to_dict()) == \
               example_fnn_with_softmax_policy

    def test_hparam(self, example_hparam: HParam) -> None:
        """
        Tests creation and dict conversion of the HParam DAO

        :param example_hparam: an example y
        :return: None
        """
        assert isinstance(example_hparam.to_dict(), dict)
        assert isinstance(HParam.from_dict(example_hparam.to_dict()), HParam)
        assert HParam.from_dict(example_hparam.to_dict()).to_dict() == example_hparam.to_dict()
        assert HParam.from_dict(example_hparam.to_dict()) == example_hparam

    def test_tabular_policy(self, example_tabular_policy: TabularPolicy) -> None:
        """
        Tests creation and dict conversion of the TabularPolicy DAO

        :param example_tabular_policy: an example TabularPolicy
        :return: None
        """
        assert isinstance(example_tabular_policy.to_dict(), dict)
        assert isinstance(TabularPolicy.from_dict(example_tabular_policy.to_dict()), TabularPolicy)
        assert TabularPolicy.from_dict(example_tabular_policy.to_dict()).to_dict() == example_tabular_policy.to_dict()
        assert TabularPolicy.from_dict(example_tabular_policy.to_dict()) == example_tabular_policy

    def test_linear_threshold_stopping_policy(
            self, example_linear_threshold_stopping_policy: LinearThresholdStoppingPolicy) -> None:
        """
        Tests creation and dict conversion of the LinearThresholdStoppingPolicy DAO

        :param example_linear_threshold_stopping_policy: an example LinearThresholdStoppingPolicy
        :return: None
        """
        assert isinstance(example_linear_threshold_stopping_policy.to_dict(), dict)
        assert isinstance(LinearThresholdStoppingPolicy.from_dict(example_linear_threshold_stopping_policy.to_dict()),
                          LinearThresholdStoppingPolicy)
        assert (LinearThresholdStoppingPolicy.from_dict(example_linear_threshold_stopping_policy.to_dict()).to_dict() ==
                example_linear_threshold_stopping_policy.to_dict())
        assert (LinearThresholdStoppingPolicy.from_dict(example_linear_threshold_stopping_policy.to_dict()) ==
                example_linear_threshold_stopping_policy)

    def test_linear_tabular_policy(self, example_linear_tabular_policy: LinearTabularPolicy) -> None:
        """
        Tests creation and dict conversion of the LinearTabularPolicy DAO

        :param example_linear_tabular_policy: an example LinearTabularPolicy
        :return: None
        """
        assert isinstance(example_linear_tabular_policy.to_dict(), dict)
        assert isinstance(LinearTabularPolicy.from_dict(example_linear_tabular_policy.to_dict()), LinearTabularPolicy)
        assert (LinearTabularPolicy.from_dict(example_linear_tabular_policy.to_dict()).to_dict() ==
                example_linear_tabular_policy.to_dict())
        assert LinearTabularPolicy.from_dict(example_linear_tabular_policy.to_dict()) == example_linear_tabular_policy

    def test_mixed_linear_tabular(self, example_mixed_linear_tabular: MixedLinearTabularPolicy) -> None:
        """
        Tests creation and dict conversion of the MixedLinearTabularPolicy DAO

        :param example_mixed_linear_tabular: an example MixedLinearTabularPolicy
        :return: None
        """
        assert isinstance(example_mixed_linear_tabular.to_dict(), dict)
        assert isinstance(MixedLinearTabularPolicy.from_dict(example_mixed_linear_tabular.to_dict()),
                          MixedLinearTabularPolicy)
        assert (MixedLinearTabularPolicy.from_dict(example_mixed_linear_tabular.to_dict()).to_dict() ==
                example_mixed_linear_tabular.to_dict())
        assert (MixedLinearTabularPolicy.from_dict(example_mixed_linear_tabular.to_dict()) ==
                example_mixed_linear_tabular)

    def test_mixed_multi_threshold_stopping_policy(
            self, example_mixed_multi_threshold_stopping_policy: MixedMultiThresholdStoppingPolicy) -> None:
        """
        Tests creation and dict conversion of the MixedMultiThresholdStoppingPolicy DAO

        :param example_mixed_multi_threshold_stopping_policy: an example MixedMultiThresholdStoppingPolicy
        :return: None
        """
        assert isinstance(example_mixed_multi_threshold_stopping_policy.to_dict(), dict)
        assert isinstance(MixedMultiThresholdStoppingPolicy.from_dict(
            example_mixed_multi_threshold_stopping_policy.to_dict()),
            MixedMultiThresholdStoppingPolicy)
        assert (MixedMultiThresholdStoppingPolicy.from_dict(example_mixed_multi_threshold_stopping_policy.to_dict()) ==
                example_mixed_multi_threshold_stopping_policy)

    def test_mixed_ppo_policy(self, example_mixed_ppo_policy: MixedPPOPolicy) -> None:
        """
        Tests creation and dict conversion of the MixedPPOPolicy DAO

        :param example_mixed_ppo_policy: an example MixedPPOPolicy
        :return: None
        """
        assert isinstance(example_mixed_ppo_policy.to_dict(), dict)
        assert isinstance(MixedPPOPolicy.from_dict(example_mixed_ppo_policy.to_dict()),
                          MixedPPOPolicy)
        assert MixedPPOPolicy.from_dict(example_mixed_ppo_policy.to_dict()).to_dict() == \
               example_mixed_ppo_policy.to_dict()
        assert MixedPPOPolicy.from_dict(example_mixed_ppo_policy.to_dict()) == example_mixed_ppo_policy

    def test_multi_threshold_stopping_policy(
            self, example_multi_threshold_stopping_policy: MultiThresholdStoppingPolicy) -> None:
        """
        Tests creation and dict conversion of the MultiThresholdStoppingPolicy DAO

        :param example_multi_threshold_stopping_policy: an example MultiThresholdStoppingPolicy
        :return: None
        """
        assert isinstance(example_multi_threshold_stopping_policy.to_dict(), dict)
        assert isinstance(MultiThresholdStoppingPolicy.from_dict(example_multi_threshold_stopping_policy.to_dict()),
                          MultiThresholdStoppingPolicy)
        assert (MultiThresholdStoppingPolicy.from_dict(example_multi_threshold_stopping_policy.to_dict()) ==
                example_multi_threshold_stopping_policy)

    def test_ppo_policy(self, example_ppo_policy: PPOPolicy) -> None:
        """
        Tests creation and dict conversion of the PPOPolicy DAO

        :param example_ppo_policy: an example PPOPolicy
        :return: None
        """
        assert isinstance(example_ppo_policy.to_dict(), dict)
        assert isinstance(PPOPolicy.from_dict(example_ppo_policy.to_dict()), PPOPolicy)
        assert PPOPolicy.from_dict(example_ppo_policy.to_dict()).to_dict() == example_ppo_policy.to_dict()
        assert PPOPolicy.from_dict(example_ppo_policy.to_dict()) == example_ppo_policy

    def test_random_policy(self, example_random_policy: RandomPolicy) -> None:
        """
        Tests creation and dict conversion of the RandomPolicy DAO

        :param example_random_policy: an example example_random_policy
        :return: None
        """
        assert isinstance(example_random_policy.to_dict(), dict)
        assert isinstance(RandomPolicy.from_dict(example_random_policy.to_dict()), RandomPolicy)
        assert RandomPolicy.from_dict(example_random_policy.to_dict()).to_dict() == example_random_policy.to_dict()
        assert RandomPolicy.from_dict(example_random_policy.to_dict()) == example_random_policy

    def test_vector_policy(self, example_vector_policy: VectorPolicy) -> None:
        """
        Tests creation and dict conversion of the VectorPolicy DAO

        :param example_vector_policy: an example VectorPolicy
        :return: None
        """
        assert isinstance(example_vector_policy.to_dict(), dict)
        assert isinstance(VectorPolicy.from_dict(example_vector_policy.to_dict()), VectorPolicy)
        assert VectorPolicy.from_dict(example_vector_policy.to_dict()).to_dict() == example_vector_policy.to_dict()
        assert VectorPolicy.from_dict(example_vector_policy.to_dict()) == example_vector_policy
