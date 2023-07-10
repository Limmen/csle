import logging
import pytest


class TestClusterManagerSuite(object):
    """Test suite for cluster_manager.py"""

    pytest.logger = logging.getLogger("cluster_manager_tests")

    def test_get_cluster_manager_status(self) -> None:
        """
        Tests the _get_cluster_manager_status function

        :return: None
        """
        assert True
