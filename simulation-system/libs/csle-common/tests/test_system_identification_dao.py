from csle_common.dao.system_identification.empirical_conditional import EmpiricalConditional
from csle_common.dao.system_identification.empirical_system_model import EmpiricalSystemModel
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_common.dao.system_identification.gaussian_mixture_conditional import GaussianMixtureConditional
from csle_common.dao.system_identification.gaussian_mixture_system_model import GaussianMixtureSystemModel
from csle_common.dao.system_identification.gp_conditional import GPConditional


class TestSystemIdentificationDaoSuite:
    """
    Test suite for management data access objects (DAOs)
    """

    def test_empirical_conditional(self) -> None:
        """
        Tests creation and dict conversion of the EmpiricalConditional DAO

        :return: None
        """

        empirical_condition = EmpiricalConditional(conditional_name="test", metric_name="test2", sample_space=[1, 2, 3],
                                                   probabilities=[0.2, 0.8])

        assert isinstance(empirical_condition.to_dict(), dict)
        assert isinstance(EmpiricalConditional.from_dict(empirical_condition.to_dict()),
                          EmpiricalConditional)
        assert (EmpiricalConditional.from_dict(empirical_condition.to_dict()).to_dict() ==
                empirical_condition.to_dict())
        assert (EmpiricalConditional.from_dict(empirical_condition.to_dict()) ==
                empirical_condition)

    def test_empirical_system_model(self) -> None:
        """
        Tests creation and dict conversion of the EmpiricalSystemModel DAO

        :return: None
        """

        empirical_condition1 = EmpiricalConditional(conditional_name="test", metric_name="test2",
                                                    sample_space=[1, 2, 3], probabilities=[0.2, 0.8])
        empirical_condition2 = EmpiricalConditional(conditional_name="test", metric_name="test2",
                                                    sample_space=[1, 2, 3],
                                                    probabilities=[0.4, 0.6])
        empirical_system_model = EmpiricalSystemModel(
            emulation_env_name="test", emulation_statistic_id=1,
            conditional_metric_distributions=[[empirical_condition1], [empirical_condition2]], descr="test1")

        assert isinstance(empirical_system_model.to_dict(), dict)
        assert isinstance(EmpiricalSystemModel.from_dict(empirical_system_model.to_dict()),
                          EmpiricalSystemModel)
        assert (EmpiricalSystemModel.from_dict(empirical_system_model.to_dict()).to_dict() ==
                empirical_system_model.to_dict())
        assert (EmpiricalSystemModel.from_dict(empirical_system_model.to_dict()) ==
                empirical_system_model)

    def test_emulation_statistics(self) -> None:
        """
        Tests creation and dict conversion of the EmulationStatistics DAO

        :return: None
        """

        emulation_statistics = EmulationStatistics(emulation_name="test")

        assert isinstance(emulation_statistics.to_dict(), dict)
        assert isinstance(EmulationStatistics.from_dict(emulation_statistics.to_dict()),
                          EmulationStatistics)
        assert (EmulationStatistics.from_dict(emulation_statistics.to_dict()).to_dict() ==
                emulation_statistics.to_dict())
        assert (EmulationStatistics.from_dict(emulation_statistics.to_dict()) ==
                emulation_statistics)

    def test_gaussian_mixture_conditional(self) -> None:
        """
        Tests creation and dict conversion of the GaussianMixtureConditional DAO

        :return: None
        """

        gaussian_mixture_conditional = GaussianMixtureConditional(
            conditional_name="test", metric_name="test1", num_mixture_components=2, dim=2,
            mixtures_means=[[0.4], [0.7]], mixtures_covariance_matrix=[[[0.5]]], mixture_weights=[0.6, 0.3],
            sample_space=[2, 5])

        assert isinstance(gaussian_mixture_conditional.to_dict(), dict)
        assert isinstance(GaussianMixtureConditional.from_dict(gaussian_mixture_conditional.to_dict()),
                          GaussianMixtureConditional)
        assert (GaussianMixtureConditional.from_dict(gaussian_mixture_conditional.to_dict()).to_dict() ==
                gaussian_mixture_conditional.to_dict())
        assert (GaussianMixtureConditional.from_dict(gaussian_mixture_conditional.to_dict()) ==
                gaussian_mixture_conditional)

    def test_gaussian_mixture_system_model(self) -> None:
        """
        Tests creation and dict conversion of the GaussianMixtureSystemModel DAO

        :return: None
        """

        gaussian_mixture_conditional = GaussianMixtureConditional(
            conditional_name="test", metric_name="test1", num_mixture_components=2, dim=2,
            mixtures_means=[[0.4], [0.7]], mixtures_covariance_matrix=[[[0.5]]], mixture_weights=[0.6, 0.3],
            sample_space=[2, 5])
        gaussian_mixture_system_model = GaussianMixtureSystemModel(
            emulation_env_name="test", emulation_statistic_id=2,
            conditional_metric_distributions=[[gaussian_mixture_conditional]], descr="test3")

        assert isinstance(gaussian_mixture_system_model.to_dict(), dict)
        assert isinstance(GaussianMixtureSystemModel.from_dict(gaussian_mixture_system_model.to_dict()),
                          GaussianMixtureSystemModel)
        assert (GaussianMixtureSystemModel.from_dict(gaussian_mixture_system_model.to_dict()).to_dict() ==
                gaussian_mixture_system_model.to_dict())
        assert (GaussianMixtureSystemModel.from_dict(gaussian_mixture_system_model.to_dict()) ==
                gaussian_mixture_system_model)

    def test_gp_conditional(self) -> None:
        """
        Tests creation and dict conversion of the GPConditional DAO

        :return: None
        """

        gp_conditional = GPConditional(
            conditional_name="test", metric_name="test1", sample_space=[1, 2, 3], observed_x=[1, 2],
            observed_y=[1.5, 3.4], scale_parameter=5.5, noise_parameter=3.2)

        assert isinstance(gp_conditional.to_dict(), dict)
        assert isinstance(GPConditional.from_dict(gp_conditional.to_dict()),
                          GPConditional)
        assert (GPConditional.from_dict(gp_conditional.to_dict()).to_dict() ==
                gp_conditional.to_dict())
        assert (GPConditional.from_dict(gp_conditional.to_dict()) ==
                gp_conditional)
