from typing import List, Tuple
import json
import pytest
import pytest_mock
from csle_common.dao.datasets.traces_dataset import TracesDataset
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesTracesDataSetsSuite:
    """
    Test suite for /traces-datasets resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def list_traces_ds(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_traces_datasets method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def list_traces_datasets() -> List[TracesDataset]:
            stat_ds = TestResourcesTracesDataSetsSuite.get_ex_traces_ds()
            return [stat_ds]
        list_traces_datasets_mocker = mocker.MagicMock(side_effect=list_traces_datasets)
        return list_traces_datasets_mocker

    @pytest.fixture
    def list_traces_ds_ids(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_traces_datasets_ids method
        
        :param mocker the pytest mocker object
        :return: the mocked function
        """
        def list_traces_datasets_ids() -> List[Tuple[int, str]]:
            return [(1, "JDoeStatistics")]
        list_traces_datasets_ids_mocker = mocker.MagicMock(side_effect=list_traces_datasets_ids)
        return list_traces_datasets_ids_mocker

    @pytest.fixture
    def remove(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the remove_traces_dataset method
        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def remove_traces_dataset(statistics_dataset: TracesDataset) -> None:
            return None
        remove_traces_dataset_mocker = mocker.MagicMock(side_effect=remove_traces_dataset)
        return remove_traces_dataset_mocker

    @pytest.fixture
    def get_traces_ds(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_traces_dataset_metadata method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def get_traces_dataset_metadata(id: int) -> TracesDataset:
            sim_tr = TestResourcesTracesDataSetsSuite.get_ex_traces_ds()
            return sim_tr
        get_traces_dataset_metadata_mocker = mocker.MagicMock(side_effect=get_traces_dataset_metadata)
        return get_traces_dataset_metadata_mocker

    @pytest.fixture
    def update(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the update_traces_dataset method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def update_traces_dataset(statistics_dataset: TracesDataset, id: int) -> None:
            return None
        update_traces_dataset_mocker = mocker.MagicMock(side_effect=update_traces_dataset)
        return update_traces_dataset_mocker

    @staticmethod
    def get_ex_traces_ds():
        """
        Static help method for obtainng a TracesDataset object
        
        :return: A SimulationTrace object
        """
        sim_trace = TracesDataset(name="Johndoe", description="null", download_count=1, file_path="null", url="null",
                                  date_added="null", num_traces=1, num_attributes_per_time_step=10,
                                  size_in_gb=5.0, compressed_size_in_gb=1.0, citation="null", num_files=1,
                                  data_schema={"null": 1}, file_format="null", added_by="JohnDoe", columns="null")
        return sim_trace

    def test_traces_datasets_get(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                 logged_in_as_admin, list_traces_ds, list_traces_ds_ids) -> None:
        """
        Testing the GET HTTPS for the /traces-datasets resource
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param list_traces_ds: the list_traces_ds fixture
        :param list_traces_ds_ids: the list_traces_ds_ids fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_traces_datasets",
                     side_effect=list_traces_ds)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_traces_datasets_ids",
                     side_effect=list_traces_ds_ids)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 1
        assert response_data_dict[api_constants.MGMT_WEBAPP.TRACES_DATASET_PROPERTY] == "JDoeStatistics"
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        ex_tr_ds = TestResourcesTracesDataSetsSuite.get_ex_traces_ds()
        ex_tr_ds_dict = ex_tr_ds.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_tr_ds_dict[k]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 1
        assert response_data_dict[api_constants.MGMT_WEBAPP.TRACES_DATASET_PROPERTY] == "JDoeStatistics"
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        ex_tr_ds = TestResourcesTracesDataSetsSuite.get_ex_traces_ds()
        ex_tr_ds_dict = ex_tr_ds.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_tr_ds_dict[k]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 1
        assert response_data_dict[api_constants.MGMT_WEBAPP.TRACES_DATASET_PROPERTY] == "JDoeStatistics"
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        ex_tr_ds = TestResourcesTracesDataSetsSuite.get_ex_traces_ds()
        ex_tr_ds_dict = ex_tr_ds.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_tr_ds_dict[k]

    def test_traces_datasets_delete(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                    logged_in_as_admin, list_traces_ds, remove) -> None:
        """
        Testing the DELETE HTTPS for the /traces-datasets resource
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param list_traces_ds: the list_traces_ds fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_traces_datasets",
                     side_effect=list_traces_ds)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_traces_dataset",
                     side_effect=remove)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE

    def test_traces_datasets_ids_get(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                     logged_in_as_admin, get_traces_ds, update) -> None:
        """
        Testing the GET HTTPS for the /traces-datasets/id resource
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_traces_ds: the get_traces_ds fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_traces_dataset_metadata",
                     side_effect=get_traces_ds)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.update_traces_dataset",
                     side_effect=update)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        ex_tr_ds = TestResourcesTracesDataSetsSuite.get_ex_traces_ds()
        ex_tr_ds_dict = ex_tr_ds.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_tr_ds_dict[k]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        ex_tr_ds = TestResourcesTracesDataSetsSuite.get_ex_traces_ds()
        ex_tr_ds_dict = ex_tr_ds.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_tr_ds_dict[k]

    def test_traces_datasets_ids_delete(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                        logged_in_as_admin, get_traces_ds, remove) -> None:
        """
        Testing the DELETE HTTPS for the /traces-datasets/id resource
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_traces_ds: the get_traces_ds fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_traces_dataset_metadata",
                     side_effect=get_traces_ds)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_traces_dataset", side_effect=remove)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
