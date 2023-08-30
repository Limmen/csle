from csle_common.dao.system_identification.empirical_conditional import EmpiricalConditional


class TestSystemIdentificationDaoSuite:
    """
    Test suite for management data access objects (DAOs)
    """

    def test_empirical_conditional_user(self) -> None:
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
