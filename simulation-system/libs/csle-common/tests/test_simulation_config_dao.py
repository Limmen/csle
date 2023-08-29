from csle_common.dao.simulation_config.action import Action


class TestSimulationConfigDaoSuite:
    """
    Test suite for simulation config data access objects (DAOs)
    """

    def test_action(self) -> None:
        """
        Tests creation and dict conversion of the Action DAO

        :return: None
        """

        action = Action(id=1, descr="test")

        assert isinstance(action.to_dict(), dict)
        assert isinstance(Action.from_dict(action.to_dict()),
                          Action)
        assert (Action.from_dict(action.to_dict()).to_dict() ==
                action.to_dict())
        assert (Action.from_dict(action.to_dict()) ==
                action)
