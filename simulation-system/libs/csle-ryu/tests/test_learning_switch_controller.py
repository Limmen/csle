import pytest_mock
from csle_ryu.controllers.learning_switch_controller import LearningSwitchController
from csle_ryu.dao.ryu_controller_type import RYUControllerType


class TestLearningSwitchControllerSuite:
    """
    Test suite for learning_switch_controller.py
    """

    def test_init(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests initialization of a LearningSwitchController

        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        wsgi = mocker.MagicMock()
        controller = LearningSwitchController(wsgi=wsgi)
        assert controller.mac_to_port == {}
        assert controller.controller_type == RYUControllerType.LEARNING_SWITCH
