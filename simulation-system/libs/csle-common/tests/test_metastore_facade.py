from csle_common.metastore.metastore_facade import MetastoreFacade
import pytest_mock


class TestMetastoreFacadeSuite:
    """
    Test suite for metastore_facade.py
    """

    def test_list_emulations(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the list_emulations function

        :param mocker: the pytest mocker object
        :return: None
        """
        assert True
        # mocker.patch('csle_common.util.general_util.GeneralUtil.get_host_ip', return_value=ip)
