from typing import List, Tuple
import json
import pytest
import pytest_mock
from csle_common.dao.datasets.statistics_dataset import StatisticsDataset
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesStatisticsDataSetsSuite:
    """
    Test suite for /statistics-datasets resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def list_stat_ds(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_statistics_datasets method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def list_statistics_datasets() -> List[StatisticsDataset]:
            stat_ds = TestResourcesStatisticsDataSetsSuite.get_ex_stat_ds()
            return [stat_ds]
        list_statistics_datasets_mocker = mocker.MagicMock(side_effect=list_statistics_datasets)
        return list_statistics_datasets_mocker

    @pytest.fixture
    def list_stat_ds_ids(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_statistics_datasets_ids method
        
        :param mocker the pytest mocker object
        :return: the mocked function
        """
        def list_statistics_datasets_ids() -> List[Tuple[int, str]]:
            return [(1, "JDoeStatistics")]
        list_statistics_datasets_ids_mocker = mocker.MagicMock(side_effect=list_statistics_datasets_ids)
        return list_statistics_datasets_ids_mocker

    @pytest.fixture
    def remove(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the remove_statistics_dataset method
        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def remove_statistics_dataset(statistics_dataset: StatisticsDataset) -> None:
            return None
        remove_statistics_dataset_mocker = mocker.MagicMock(side_effect=remove_statistics_dataset)
        return remove_statistics_dataset_mocker

    @pytest.fixture
    def get_stat_ds(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_statistics_dataset_metadata

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def get_statistics_dataset_metadata(id: int) -> StatisticsDataset:
            sim_tr = TestResourcesStatisticsDataSetsSuite.get_ex_stat_ds()
            return sim_tr
        get_statistics_dataset_metadata_mocker = mocker.MagicMock(side_effect=get_statistics_dataset_metadata)
        return get_statistics_dataset_metadata_mocker

    @pytest.fixture
    def update(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the update_statistics_dataset method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def update_statistics_dataset(statistics_dataset: StatisticsDataset, id: int) -> None:
            return None
        update_statistics_dataset_mocker = mocker.MagicMock(side_effect=update_statistics_dataset)
        return update_statistics_dataset_mocker

    @staticmethod
    def get_ex_stat_ds():
        """
        Static help method for obtainng a SimulationTrace object
        
        :return: A SimulationTrace object
        """
        sim_trace = StatisticsDataset(name="JohnDoe", description="null", download_count=1, file_path="null",
                                      url="null", date_added="null", num_measurements=1, num_metrics=1,
                                      size_in_gb=1.0, compressed_size_in_gb=0.5, citation="null",
                                      num_files=4, file_format="null", added_by="JDoe", conditions="null",
                                      metrics="null", num_conditions=1)
        return sim_trace

    def test_statistics_datasets_get(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                     logged_in_as_admin, list_stat_ds, list_stat_ds_ids) -> None:
        """
        Testing the GET HTTPS for the /statistics-datasets resource
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param list_stat_ds: the list_stat_ds fixture
        :param list_stat_ds_ids: the list_stat_ds_ids fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_statistics_datasets",
                     side_effect=list_stat_ds)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_statistics_datasets_ids",
                     side_effect=list_stat_ds_ids)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 1
        assert response_data_dict[api_constants.MGMT_WEBAPP.STATISTICS_DATASET_PROPERTY] == "JDoeStatistics"
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        ex_st_ds = TestResourcesStatisticsDataSetsSuite.get_ex_stat_ds()
        ex_st_ds_dict = ex_st_ds.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_st_ds_dict[k]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 1
        assert response_data_dict[api_constants.MGMT_WEBAPP.STATISTICS_DATASET_PROPERTY] == "JDoeStatistics"
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        ex_st_ds = TestResourcesStatisticsDataSetsSuite.get_ex_stat_ds()
        ex_st_ds_dict = ex_st_ds.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_st_ds_dict[k]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 1
        assert response_data_dict[api_constants.MGMT_WEBAPP.STATISTICS_DATASET_PROPERTY] == "JDoeStatistics"
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        ex_st_ds = TestResourcesStatisticsDataSetsSuite.get_ex_stat_ds()
        ex_st_ds_dict = ex_st_ds.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_st_ds_dict[k]

    def test_statistics_datasets_delete(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                        logged_in_as_admin, list_stat_ds, remove) -> None:
        """
        Testing the DELETE HTTPS for the /statistics-datasets resource
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param list_stat_ds: the list_stat_ds fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_statistics_datasets",
                     side_effect=list_stat_ds)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_statistics_dataset",
                     side_effect=remove)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE

    def test_satistics_datasets_ids_get(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                        logged_in_as_admin, get_stat_ds, update) -> None:
        """
        Testing the GET HTTPS for the /statistics-datasets/id resource
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_stat_ds: the get_stat_ds fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_statistics_dataset_metadata",
                     side_effect=get_stat_ds)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.update_statistics_dataset",
                     side_effect=update)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        ex_st_ds = TestResourcesStatisticsDataSetsSuite.get_ex_stat_ds()
        ex_st_ds_dict = ex_st_ds.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_st_ds_dict[k]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        ex_st_ds = TestResourcesStatisticsDataSetsSuite.get_ex_stat_ds()
        ex_st_ds_dict = ex_st_ds.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_st_ds_dict[k]

    def test_statistics_datasets_ids_delete(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                            logged_in_as_admin, get_stat_ds, remove) -> None:
        """
        Testing the DELETE HTTPS for the /statistics-datasets/id resource
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_stat_ds: the get_stat_ds fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_statistics_dataset_metadata",
                     side_effect=get_stat_ds)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_statistics_dataset",
                     side_effect=remove)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
