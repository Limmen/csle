import logging
import pytest


class TestLearningSwitchControllerSuite(object):
    """
    Test suite for learning_switch_controller.py
    """

    pytest.logger = logging.getLogger("learning_switch_controller_tests")

    def test_add_flow(self) -> None:
        """
        Tests the add_flow function

        :return: None
        """
        assert True
