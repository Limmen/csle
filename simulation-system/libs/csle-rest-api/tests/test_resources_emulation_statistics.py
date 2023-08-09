from typing import List, Tuple
import json
import pytest
import pytest_mock
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesEmulationsStatisticsSuite:
    """
    Test suite for /emulations-statistics resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def em_stat_ids(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_emulation_statistics_ids method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def list_emulation_statistics_ids() -> List[Tuple[int, int]]:
            return [(1, 1)]
        list_emulation_statistics_ids_mocker = mocker.MagicMock(side_effect=list_emulation_statistics_ids)
        return list_emulation_statistics_ids_mocker

    @pytest.fixture
    def remove(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the remove_emulation_statistic method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def remove_emulation_statistic(stat: EmulationStatistics) -> None:
            return None
        remove_emulation_statistic_mocker = mocker.MagicMock(side_effect=remove_emulation_statistic)
        return remove_emulation_statistic_mocker

    @pytest.fixture
    def em_stat(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_emulation_statistics function

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def list_emulation_statistics() -> List[EmulationStatistics]:
            em_stat = TestResourcesEmulationsStatisticsSuite.get_ex_em_stat()
            return [em_stat]
        list_emulation_statistics_mocker = mocker.MagicMock(side_effect=list_emulation_statistics)
        return list_emulation_statistics_mocker

    @pytest.fixture
    def get_em_stat(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_emulation_statistic method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def get_emulation_statistic(id: int) -> EmulationStatistics:
            em_stat = TestResourcesEmulationsStatisticsSuite.get_ex_em_stat()
            return em_stat
        get_emulation_statistic_mocker = mocker.MagicMock(side_effect=get_emulation_statistic)
        return get_emulation_statistic_mocker

    @pytest.fixture
    def get_em_stat_none(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_emulation_statistic method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def get_emulation_statistic(id: int) -> None:
            return None
        get_emulation_statistic_mocker = mocker.MagicMock(side_effect=get_emulation_statistic)
        return get_emulation_statistic_mocker

    @staticmethod
    def get_ex_em_stat() -> EmulationStatistics:
        """
        Static help method for returning an Emulationstatistic object

        :return: an EmulationsSatistics object
        """
        em_stat = EmulationStatistics(emulation_name="JohnDoe", descr="null")
        return em_stat

    def test_emulation_statistics_get(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                      logged_in_as_admin, em_stat_ids, em_stat) -> None:
        """
        Testing the GET HTTPS method for the /emulation-statistics resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param em_stat_ids: the em_stat_ids fixture
        :param em_stat: the em_stat fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulation_statistics_ids",
                     side_effect=em_stat_ids)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulation_statistics",
                     side_effect=em_stat)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 1
        assert response_data_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == 1
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        ex_em_stat = TestResourcesEmulationsStatisticsSuite.get_ex_em_stat()
        ex_em_stat_dict = ex_em_stat.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_em_stat_dict[k]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 1
        assert response_data_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == 1
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        ex_em_stat = TestResourcesEmulationsStatisticsSuite.get_ex_em_stat()
        ex_em_stat_dict = ex_em_stat.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_em_stat_dict[k]

    def test_emulation_statistics_delete(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                         logged_in_as_admin, em_stat, remove) -> None:
        """
        Testing the DELETE HTTPS method for the /emulation-statistics resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param em_stat_ids: the em_stat_ids fixture
        :param em_stat: the em_stat fixture
        :param remove: the remove fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulation_statistics",
                     side_effect=em_stat)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_emulation_statistic",
                     side_effect=remove)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_statistics_ids_get(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                          logged_in_as_admin, get_em_stat, get_em_stat_none) -> None:
        """
        Testing the GET HTTPS method for the /emulation-statistics/id resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param em_stat_ids: the em_stat_ids fixture
        :param em_stat: the em_stat fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_statistic",
                     side_effect=get_em_stat)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        ex_em_stat = TestResourcesEmulationsStatisticsSuite.get_ex_em_stat()
        ex_em_stat_dict = ex_em_stat.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_em_stat_dict[k]
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_statistic",
                     side_effect=get_em_stat_none)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        ex_em_stat = TestResourcesEmulationsStatisticsSuite.get_ex_em_stat()
        ex_em_stat_dict = ex_em_stat.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_em_stat_dict[k]
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_statistic",
                     side_effect=get_em_stat_none)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE

    def test_emulation_statistics_ids_delete(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                             logged_in_as_admin, get_em_stat, get_em_stat_none, remove) -> None:
        """
        Testing the DELETE HTTPS method for the /emulation-statistics/id resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param em_stat_ids: the em_stat_ids fixture
        :param em_stat: the em_stat fixture
        :param remove: the remove fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_statistic",
                     side_effect=get_em_stat)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_emulation_statistic",
                     side_effect=remove)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict == {}
