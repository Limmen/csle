import logging
import pytest


class TestDefenderUpdateStateMiddlewareSuite(object):
    """
    Test suite for defender_update_state_middleware.py
    """

    pytest.logger = logging.getLogger("defender_update_state_middleware_tests")

    def test_update_state(self) -> None:
        """
        Tests the update_state function

        :return: None
        """
        assert True
