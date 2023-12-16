import json
from typing import List

import csle_common.constants.constants as constants
import pytest
import pytest_mock
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType

import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesTrainingjobsSuite:
    """
    Test suite for /training-jobs resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(
            static_folder="../../../../../management-system/csle-mgmt-webapp/build"
        )

    @pytest.fixture
    def list_jobs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_training_jobs function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """

        def list_training_jobs() -> List[TrainingJobConfig]:
            policy = TestResourcesTrainingjobsSuite.get_example_job()
            return [policy]

        list_training_jobs_mocker = mocker.MagicMock(side_effect=list_training_jobs)
        return list_training_jobs_mocker

    @pytest.fixture
    def remove(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the remove_training_job function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """

        def remove_training_job(training_job: TrainingJobConfig) -> None:
            return None

        remove_training_job_mocker = mocker.MagicMock(side_effect=remove_training_job)
        return remove_training_job_mocker

    @pytest.fixture
    def start(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for the start_training_job_in_background function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """

        def start_training_job_in_background(training_job: TrainingJobConfig) -> None:
            return None

        start_training_job_in_background_mocker = mocker.MagicMock(
            side_effect=start_training_job_in_background
        )
        return start_training_job_in_background_mocker

    @pytest.fixture
    def get_job_config(self, mocker: pytest_mock.MockFixture) -> TrainingJobConfig:
        """
        Pytest fixture for mocking the get_training_job_config function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """

        def get_training_job_config(id: int) -> TrainingJobConfig:
            policy = TestResourcesTrainingjobsSuite.get_example_job()
            return policy

        get_training_job_config_mocker = mocker.MagicMock(
            side_effect=get_training_job_config
        )
        return get_training_job_config_mocker

    @staticmethod
    def get_example_job() -> TrainingJobConfig:
        """
        Utility function for getting an example instance of a PPOPolicy

        :return: an example isntance of a PPOPOlicy
        """
        e_config_class = ExperimentConfig(
            output_dir="output_directory",
            title="title",
            random_seeds=[1, 2, 3],
            agent_type=AgentType(1),
            hparams={"element": HParam(10, name="John", descr="Doe")},
            log_every=10,
            player_type=PlayerType(1),
            player_idx=10,
            br_log_every=10,
        )
        obj = TrainingJobConfig(
            simulation_env_name="JohnDoeSimulation",
            experiment_config=e_config_class,
            progress_percentage=20.5,
            pid=5,
            experiment_result=ExperimentResult(),
            emulation_env_name="JDoe_env",
            simulation_traces=[SimulationTrace(simulation_env="JDoe_env")],
            num_cached_traces=10,
            log_file_path="JohnDoeLog",
            descr="null",
            physical_host_ip="123.456.78.99",
        )
        return obj

    def test_training_jobs_get(
        self,
        flask_app,
        mocker,
        list_jobs,
        logged_in,
        not_logged_in,
        logged_in_as_admin,
        pid_true,
        pid_false,
    ) -> None:
        """
        Testing for the GET HTTPS method in the /training-jobs resource

        :param flask_app: the flask app for making the test requests
        :param mocker: the pytest mocker object
        :param list_ppo: the list_ppo fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param list_ppo_ids: the list_ppo_ids fixture
        :return: None
        """
        mocker.patch("time.sleep", return_value=None)
        test_job = TestResourcesTrainingjobsSuite.get_example_job()
        test_job_dict = test_job.to_dict()
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.list_training_jobs",
            side_effect=list_jobs,
        )
        mocker.patch(
            "csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
            side_effect=pid_true,
        )
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().get(
            api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        response = flask_app.test_client().get(
            api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        tjob_data = TrainingJobConfig.from_dict(response_data_list[0])
        tjob_data_dict = tjob_data.to_dict()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in tjob_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert tjob_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert tjob_data.running is True
        assert test_job.running is False
        assert tjob_data.running != test_job.running
        response = flask_app.test_client().get(
            f"{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}"
            f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        tjob_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert (
            tjob_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY]
            == test_job.emulation_env_name
        )
        assert tjob_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == test_job.id
        assert tjob_dict[api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is True
        assert test_job.running is False
        assert (
            tjob_dict[api_constants.MGMT_WEBAPP.SIMULATION_PROPERTY]
            == test_job.simulation_env_name
        )
        mocker.patch(
            "csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
            side_effect=pid_false,
        )
        response = flask_app.test_client().get(
            api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        tjob_data = TrainingJobConfig.from_dict(response_data_list[0])
        tjob_data_dict = tjob_data.to_dict()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in tjob_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert tjob_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert tjob_data.running is False
        assert test_job.running is False
        assert tjob_data.running == test_job.running
        response = flask_app.test_client().get(
            f"{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}"
            f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        tjob_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert (
            tjob_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY]
            == test_job.emulation_env_name
        )
        assert tjob_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == test_job.id
        assert tjob_dict[api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is False
        assert test_job.running is False
        assert tjob_dict[api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] == test_job.running
        assert (
            tjob_dict[api_constants.MGMT_WEBAPP.SIMULATION_PROPERTY]
            == test_job.simulation_env_name
        )
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )
        mocker.patch(
            "csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
            side_effect=pid_true,
        )
        response = flask_app.test_client().get(
            api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        tjob_data = TrainingJobConfig.from_dict(response_data_list[0])
        tjob_data_dict = tjob_data.to_dict()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in tjob_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert tjob_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert tjob_data.running is True
        assert test_job.running is False
        assert tjob_data.running != test_job.running
        response = flask_app.test_client().get(
            f"{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}"
            f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        tjob_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert (
            tjob_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY]
            == test_job.emulation_env_name
        )
        assert tjob_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == test_job.id
        assert tjob_dict[api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is True
        assert test_job.running is False
        assert tjob_dict[api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] != test_job.running
        assert (
            tjob_dict[api_constants.MGMT_WEBAPP.SIMULATION_PROPERTY]
            == test_job.simulation_env_name
        )
        mocker.patch(
            "csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
            side_effect=pid_false,
        )
        response = flask_app.test_client().get(
            api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        tjob_data = TrainingJobConfig.from_dict(response_data_list[0])
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        tjob_data_dict = tjob_data.to_dict()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in tjob_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert tjob_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert tjob_data.running is False
        assert test_job.running is False
        assert tjob_data.running == test_job.running
        response = flask_app.test_client().get(
            f"{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}"
            f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        tjob_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert (
            tjob_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY]
            == test_job.emulation_env_name
        )
        assert tjob_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == test_job.id
        assert tjob_dict[api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is False
        assert test_job.running is False
        assert tjob_dict[api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] == test_job.running
        assert tjob_dict[api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] == test_job.running
        assert (
            tjob_dict[api_constants.MGMT_WEBAPP.SIMULATION_PROPERTY]
            == test_job.simulation_env_name
        )

    def test_training_jobs_delete(
        self,
        flask_app,
        mocker: pytest_mock.MockFixture,
        list_jobs,
        logged_in,
        not_logged_in,
        logged_in_as_admin,
        remove,
        stop,
    ) -> None:
        """
        Tests the HTTP DELETE method on the /training-jobs resource

        :param flask_app: the flask app for making the test requests
        :param mocker: the pytest mocker object
        :param list_ppo: the list_ppo fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param remove: the remove fixture
        :return: None
        """
        mocker.patch("time.sleep", return_value=None)
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.list_training_jobs",
            side_effect=list_jobs,
        )
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.remove_training_job",
            side_effect=remove,
        )
        mocker.patch(
            "csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_pid",
            side_effect=stop,
        )
        response = flask_app.test_client().delete(
            api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().delete(
            api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )
        response = flask_app.test_client().delete(
            api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}

    def test_training_jobs_id_get(
        self,
        flask_app,
        mocker: pytest_mock.MockFixture,
        logged_in,
        not_logged_in,
        logged_in_as_admin,
        get_job_config,
        pid_true,
        pid_false,
    ) -> None:
        """
        Tests the HTTPS GET method for the /trianing-jobs/id resource

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
        mocker.patch("time.sleep", return_value=None)
        test_job = TestResourcesTrainingjobsSuite.get_example_job()
        test_job_dict = test_job.to_dict()
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.get_training_job_config",
            side_effect=get_job_config,
        )
        mocker.patch(
            "csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
            side_effect=pid_true,
        )
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().get(
            f"{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}" f"/10"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        response = flask_app.test_client().get(
            f"{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}" f"/10"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        tjob_data = TrainingJobConfig.from_dict(response_data_list)
        tjob_data_dict = tjob_data.to_dict()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in tjob_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert tjob_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert tjob_data.running is True
        assert test_job.running is False
        assert tjob_data.running != test_job.running
        mocker.patch(
            "csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
            side_effect=pid_false,
        )
        response = flask_app.test_client().get(
            f"{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}" f"/10"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        tjob_data = TrainingJobConfig.from_dict(response_data_list)
        tjob_data_dict = tjob_data.to_dict()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in tjob_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert tjob_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert tjob_data.running is False
        assert test_job.running is False
        assert tjob_data.running == test_job.running
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )
        mocker.patch(
            "csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
            side_effect=pid_true,
        )
        response = flask_app.test_client().get(
            f"{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}" f"/10"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        tjob_data = TrainingJobConfig.from_dict(response_data_list)
        tjob_data_dict = tjob_data.to_dict()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in tjob_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert tjob_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert tjob_data.running is True
        assert test_job.running is False
        assert tjob_data.running != test_job.running
        mocker.patch(
            "csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
            side_effect=pid_false,
        )
        response = flask_app.test_client().get(
            f"{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}" f"/10"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        tjob_data = TrainingJobConfig.from_dict(response_data_list)
        tjob_data_dict = tjob_data.to_dict()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in tjob_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert tjob_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert tjob_data.running is False
        assert test_job.running is False
        assert tjob_data.running == test_job.running

    def test_training_jobs_id_delete(
        self,
        flask_app,
        mocker: pytest_mock.MockFixture,
        logged_in_as_admin,
        logged_in,
        not_logged_in,
        get_job_config,
        remove,
        stop,
    ) -> None:
        """
        Tests the HTTPS DELETE method for the /training-jobs-id resource

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
        mocker.patch("time.sleep", return_value=None)
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.get_training_job_config",
            side_effect=get_job_config,
        )
        mocker.patch(
            "csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_pid",
            side_effect=stop,
        )
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.remove_training_job",
            side_effect=remove,
        )
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().delete(
            f"{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}/10"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        response = flask_app.test_client().delete(
            f"{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}" f"/10"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )
        response = flask_app.test_client().delete(
            f"{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}" f"/10"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}

    def test_training_jobs_id_post(
        self,
        flask_app,
        mocker: pytest_mock.MockFixture,
        logged_in_as_admin,
        logged_in,
        not_logged_in,
        get_job_config,
        stop,
        start,
    ) -> None:
        """
        Tests the HTTPS POST method for the /training-jobs-id resource

        :param flask_app: the flask app for making the tests requests
        :param mocker: the pytest mocker object
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param start: the start fixture
        :param stop: the stop fixture
        :param get_job_config: the get_job_config fixture
        :return: None
        """
        mocker.patch("time.sleep", return_value=None)
        mocker.patch(
            "csle_agents.job_controllers.training_job_manager.TrainingJobManager."
            "start_training_job_in_background",
            side_effect=start,
        )
        mocker.patch(
            "csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_pid",
            side_effect=stop,
        )
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.get_training_job_config",
            side_effect=get_job_config,
        )
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().post(
            f"{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}/10"
            f"?{api_constants.MGMT_WEBAPP.STOP_QUERY_PARAM}=true"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        response = flask_app.test_client().post(
            f"{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}"
            f"/10"
            f"?{api_constants.MGMT_WEBAPP.STOP_QUERY_PARAM}=true"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        response = flask_app.test_client().post(
            f"{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}"
            f"/10"
            f"?{api_constants.MGMT_WEBAPP.STOP_QUERY_PARAM}=false"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )
        response = flask_app.test_client().post(
            f"{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}"
            f"/10"
            f"?{api_constants.MGMT_WEBAPP.STOP_QUERY_PARAM}=true"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}
        response = flask_app.test_client().post(
            f"{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}"
            f"/10"
            f"?{api_constants.MGMT_WEBAPP.STOP_QUERY_PARAM}=false"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}
