from csle_common.dao.system_identification.empirical_conditional import EmpiricalConditional
from csle_common.dao.system_identification.empirical_system_model import EmpiricalSystemModel


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
