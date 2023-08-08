from typing import List
import json
import pytest
import pytest_mock
import csle_common.constants.constants as constants
from csle_common.dao.jobs.system_identification_job_config import SystemIdentificationJobConfig
from csle_common.dao.system_identification.gaussian_mixture_conditional import GaussianMixtureConditional
from csle_common.dao.system_identification.gaussian_mixture_system_model import GaussianMixtureSystemModel
from csle_common.dao.system_identification.system_identification_config import SystemIdentificationConfig
from csle_common.dao.system_identification.system_model_type import SystemModelType
from csle_common.dao.training.hparam import HParam
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesSystemIdentificationSuite:
    """
    Test suite for /system-identification-jobs resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def list_jobs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_system_identification_jobs function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """
        def list_system_identification_jobs() -> List[SystemIdentificationJobConfig]:
            s_i_job = TestResourcesSystemIdentificationSuite.get_example_job()
            return [s_i_job]
        list_system_identification_jobs_mocker = mocker.MagicMock(side_effect=list_system_identification_jobs)
        return list_system_identification_jobs_mocker

    @pytest.fixture
    def remove(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the remove_system_identification_job function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """
        def remove_system_identification_job(system_identification_job: SystemIdentificationJobConfig) -> None:
            return None
        remove_system_identification_job_mocker = mocker.MagicMock(side_effect=remove_system_identification_job)
        return remove_system_identification_job_mocker

    @pytest.fixture
    def start(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for the start_system_identification_job_in_background function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """
        def start_system_identification_job_in_background(system_identification_job:
                                                          SystemIdentificationJobConfig) -> None:
            return None
        start_system_identification_job_in_background_mocker = mocker.MagicMock(
            side_effect=start_system_identification_job_in_background)
        return start_system_identification_job_in_background_mocker

    @pytest.fixture
    def get_job_config(self, mocker: pytest_mock.MockFixture) -> SystemIdentificationJobConfig:
        """
        Pytest fixture for mocking the get_system_identification_job_config function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """
        def get_system_identification_job_config(id: int) -> SystemIdentificationJobConfig:
            s_i_job = TestResourcesSystemIdentificationSuite.get_example_job()
            return s_i_job
        get_system_identification_job_config_mocker = mocker.MagicMock(side_effect=get_system_identification_job_config)
        return get_system_identification_job_config_mocker

    @staticmethod
    def get_example_job() -> SystemIdentificationJobConfig:
        """
        Utility function for getting an example instance of a system-identification-job cofiguration

        :return: an example isntance of a system-identification-job cofiguration
        """
        gauss_cond = GaussianMixtureConditional(conditional_name="JohnDoeCond", metric_name="JohnDoeMetric",
                                                num_mixture_components=1, dim=1, mixtures_means=[[1.1]],
                                                mixtures_covariance_matrix=[[[1.1]]], mixture_weights=[1.1],
                                                sample_space=[10])
        sys_mod = GaussianMixtureSystemModel(emulation_env_name="JohnDoeEmulation", emulation_statistic_id=10,
                                             conditional_metric_distributions=[[gauss_cond]], descr="descr",)
        s_i_config = SystemIdentificationConfig(model_type=SystemModelType.GAUSSIAN_MIXTURE,
                                                hparams={"params": HParam(value=10, name="JohnDoe", descr="descr")},
                                                output_dir="null", title="JDoeTitle", log_every=10)
        obj = SystemIdentificationJobConfig(emulation_env_name="JohnDoeEmulation", emulation_statistics_id=10,
                                            progress_percentage=20.5, pid=10, log_file_path="null",
                                            system_identification_config=s_i_config,
                                            physical_host_ip="123.456.78.99",
                                            descr="null",
                                            system_model=sys_mod)
        return obj

    def test_s_i_jobs_get(self, flask_app, mocker: pytest_mock.MockFixture, list_jobs, logged_in, not_logged_in,
                          logged_in_as_admin, pid_true, pid_false,) -> None:
        """
        Testing for the GET HTTPS method in the /system-identification-jobs resource

        :param flask_app: the flask app for making the test requests
        :param mocker: the pytest mocker object
        :param list_ppo: the list_ppo fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param list_ppo_ids: the list_ppo_ids fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        test_job = TestResourcesSystemIdentificationSuite.get_example_job()
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_system_identification_jobs",
                     side_effect=list_jobs)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
                     side_effect=pid_true)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list[0][api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == test_job.emulation_env_name
        assert response_data_list[0][api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is True
        assert response_data_list[0][api_constants.MGMT_WEBAPP.ID_PROPERTY] == test_job.id
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        s_i_job_data = SystemIdentificationJobConfig.from_dict(response_data_list[0])
        s_i_job_data_dict = s_i_job_data.to_dict()
        test_job_dict = test_job.to_dict()
        for k in s_i_job_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert s_i_job_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert s_i_job_data.running is True
        assert test_job.running is False
        assert s_i_job_data != test_job.running
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
                     side_effect=pid_false)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list[0][api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == test_job.emulation_env_name
        assert response_data_list[0][api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is False
        assert response_data_list[0][api_constants.MGMT_WEBAPP.ID_PROPERTY] == test_job.id
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        s_i_job_data = SystemIdentificationJobConfig.from_dict(response_data_list[0])
        s_i_job_data_dict = s_i_job_data.to_dict()
        test_job_dict = test_job.to_dict()
        for k in s_i_job_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert s_i_job_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert s_i_job_data.running is False
        assert test_job.running is False
        assert s_i_job_data.running == test_job.running
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
                     side_effect=pid_true)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list[0][api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == test_job.emulation_env_name
        assert response_data_list[0][api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is True
        assert response_data_list[0][api_constants.MGMT_WEBAPP.ID_PROPERTY] == test_job.id
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        s_i_job_data = SystemIdentificationJobConfig.from_dict(response_data_list[0])
        s_i_job_data_dict = s_i_job_data.to_dict()
        test_job_dict = test_job.to_dict()
        for k in s_i_job_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert s_i_job_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert s_i_job_data.running is True
        assert test_job.running is False
        assert s_i_job_data.running != test_job.running
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
                     side_effect=pid_false)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        s_i_job_data = SystemIdentificationJobConfig.from_dict(response_data_list[0])
        s_i_job_data_dict = s_i_job_data.to_dict()
        test_job_dict = test_job.to_dict()
        for k in s_i_job_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert s_i_job_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert s_i_job_data.running is False
        assert test_job.running is False
        assert s_i_job_data.running == test_job.running
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list[0][api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == test_job.emulation_env_name
        assert response_data_list[0][api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is False
        assert response_data_list[0][api_constants.MGMT_WEBAPP.ID_PROPERTY] == test_job.id

    def test_s_i_jobs_delete(self, flask_app, mocker: pytest_mock.MockFixture, list_jobs, logged_in,
                             not_logged_in, logged_in_as_admin, remove, stop) -> None:
        """
        Tests the HTTP DELETE method on the /system-identification-jobs resource

        :param flask_app: the flask app for making the test requests
        :param mocker: the pytest mocker object
        :param list_ppo: the list_ppo fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param remove: the remove fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_system_identification_jobs",
                     side_effect=list_jobs)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_system_identification_job",
                     side_effect=remove)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_pid", side_effect=stop)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}

    def test_s_i_jobs_id_get(self, flask_app, mocker: pytest_mock.MockFixture, logged_in, not_logged_in,
                             logged_in_as_admin, get_job_config, pid_true, pid_false,) -> None:
        """
        Tests the HTTPS GET method for the /system-identification-jobs/id resource

        :param flask_app: the flask app for making the test requests
        :param mocker: the pytest mocker object
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_job_config: the get_job_config fixture
        :param pid_true: the pid_true fixture
        :param pid_false: the pid_false fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        test_job = TestResourcesSystemIdentificationSuite.get_example_job()
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_system_identification_job_config",
                     side_effect=get_job_config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
                     side_effect=pid_true)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        s_i_job_data = SystemIdentificationJobConfig.from_dict(response_data_list)
        s_i_job_data_dict = s_i_job_data.to_dict()
        test_job_dict = test_job.to_dict()
        for k in s_i_job_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert s_i_job_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert s_i_job_data.running is True
        assert test_job.running is False
        assert s_i_job_data != test_job.running
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
                     side_effect=pid_false)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        s_i_job_data = SystemIdentificationJobConfig.from_dict(response_data_list)
        s_i_job_data_dict = s_i_job_data.to_dict()
        test_job_dict = test_job.to_dict()
        for k in s_i_job_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert s_i_job_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert s_i_job_data.running is False
        assert test_job.running is False
        assert s_i_job_data.running == test_job.running
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
                     side_effect=pid_true)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        s_i_job_data = SystemIdentificationJobConfig.from_dict(response_data_list)
        s_i_job_data_dict = s_i_job_data.to_dict()
        test_job_dict = test_job.to_dict()
        for k in s_i_job_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert s_i_job_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert s_i_job_data.running is True
        assert test_job.running is False
        assert s_i_job_data.running != test_job.running
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
                     side_effect=pid_false)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        s_i_job_data = SystemIdentificationJobConfig.from_dict(response_data_list)
        s_i_job_data_dict = s_i_job_data.to_dict()
        test_job_dict = test_job.to_dict()
        for k in s_i_job_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert s_i_job_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert s_i_job_data.running is False
        assert test_job.running is False
        assert s_i_job_data.running == test_job.running

    def test_s_i_jobs_id_delete(self, flask_app, mocker: pytest_mock.MockFixture, logged_in_as_admin, logged_in,
                                not_logged_in, get_job_config, remove, stop) -> None:
        """
        Tests the HTTPS DELETE method for the /system-identification-jobs/id resource

        :param flask_app: the flask app for making the tests requests
        :param mocker: the pytest mocker object
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin:  the logged_in_as_admin fixure
        :param get_job_config: the get_job_config fixture
        :param remove: the remove fixture
        :param stop: the stop fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_system_identification_job_config",
                     side_effect=get_job_config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_pid", side_effect=stop)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_system_identification_job",
                     side_effect=remove)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}

    def test_s_i_jobs_id_post(self, flask_app, mocker: pytest_mock.MockFixture, logged_in_as_admin, logged_in,
                              not_logged_in, get_job_config, start, stop) -> None:
        """
        Tests the HTTPS DELETE method for the /system-identification-jobs/id resource

        :param flask_app: the flask app for making the tests requests
        :param mocker: the pytest mocker object
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin:  the logged_in_as_admin fixure
        :param get_job_config: the get_job_config fixture
        :param remove: the remove fixture
        :param stop: the stop fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_system_identification_job_config",
                     side_effect=get_job_config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_pid", side_effect=stop)
        mocker.patch("csle_system_identification.job_controllers.system_identification_job_manager."
                     "SystemIdentificationJobManager.start_system_identification_job_in_background", side_effect=start)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}"f"/10"
                                                f"?{api_constants.MGMT_WEBAPP.STOP_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}"f"/10"
                                                f"?{api_constants.MGMT_WEBAPP.STOP_QUERY_PARAM}=false")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}
