import json
import logging
from typing import Any, Dict

import csle_common.constants.constants as constants
import pytest
import pytest_mock

import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesLogsSuite:
    """
    Test suite for /login resource
    """

    pytest.logger = logging.getLogger("resources_logs_tests")

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def csle_logs(self, mocker):
        """
        Pytest fixture for mocking the get_csle_log_files function
        :param mocker: The pytest mocker object
        :return: The mocked function
        """
        def get_csle_log_files(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.LOGS_RESOURCE}": 654321}
        get_csle_log_files_mocker = mocker.MagicMock(
            side_effect=get_csle_log_files)
        return get_csle_log_files_mocker

    @pytest.fixture
    def dsm_logs(self, mocker):
        """
        Pytest fixture for mocking the get_docker_statsmanager_logs function
        :param mocker: The pytest mocker object
        :return: The mocked function
        """
        def get_docker_statsmanager_logs(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MANAGER_SUBRESOURCE}":
                    654321}
        get_docker_statsmanager_logs_mocker = mocker.MagicMock(
            side_effect=get_docker_statsmanager_logs)
        return get_docker_statsmanager_logs_mocker

    @pytest.fixture
    def prom_logs(self, mocker):
        """
        Pytest fixture for mocking the get_prometheus_logs function
        :param mocker: The pytest mocker object
        :return: The mocked function
        """
        def get_prometheus_logs(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.PROMETHEUS_RESOURCE}":
                    654321}
        get_prometheus_logs_mocker = mocker.MagicMock(
            side_effect=get_prometheus_logs)
        return get_prometheus_logs_mocker

    @pytest.fixture
    def nginx_logs(self, mocker):
        """
        Pytest fixture for mocking the get_nginx_logs function
        :param mocker: The pytest mocker object
        :return: The mocked function
        """
        def get_nginx_logs(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.NGINX_RESOURCE}":
                    654321}
        get_nginx_logs_mocker = mocker.MagicMock(
            side_effect=get_nginx_logs)
        return get_nginx_logs_mocker

    @pytest.fixture
    def postgresql_logs(self, mocker):
        """
        Pytest fixture for mocking the get_postgresql_logs function
        :param mocker: The pytest mocker object
        :return: The mocked function
        """
        def get_postgresql_logs(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.POSTGRESQL_RESOURCE}":
                    654321}
        get_postgresql_logs_mocker = mocker.MagicMock(
            side_effect=get_postgresql_logs)
        return get_postgresql_logs_mocker

    @pytest.fixture
    def flask_logs(self, mocker):
        """
        Pytest fixture for mocking the get_flask_logs function
        :param mocker: The pytest mocker object
        :return: The mocked function
        """
        def get_flask_logs(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.FLASK_RESOURCE}":
                    654321}
        get_flask_logs_mocker = mocker.MagicMock(
            side_effect=get_flask_logs)
        return get_flask_logs_mocker

    @pytest.fixture
    def cluster_manager_logs(self, mocker):
        """
        Pytest fixture for mocking the get_cluster_manager_logs function
        :param mocker: The pytest mocker object
        :return: The mocked function
        """
        def get_cluster_manager_logs(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.CLUSTERMANAGER_RESOURCE}":
                    654321}
        get_cluster_manager_logs_mocker = mocker.MagicMock(
            side_effect=get_cluster_manager_logs)
        return get_cluster_manager_logs_mocker

    @pytest.fixture
    def docker_logs(self, mocker):
        """
        Pytest fixture for mocking the get_docker_logs function
        :param mocker: The pytest mocker object
        :return: The mocked function
        """
        def get_docker_logs(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.DOCKER_RESOURCE}":
                    654321}
        get_docker_logs_mocker = mocker.MagicMock(
            side_effect=get_docker_logs)
        return get_docker_logs_mocker

    @pytest.fixture
    def node_exporter_logs(self, mocker):
        """
        Pytest fixture for mocking the get_node_exporter_logs function
        :param mocker: The pytest mocker object
        :return: The mocked function
        """
        def get_node_exporter_logs(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE}":
                    654321}
        get_node_exporter_logs_mocker = mocker.MagicMock(
            side_effect=get_node_exporter_logs)
        return get_node_exporter_logs_mocker

    @pytest.fixture
    def cadvisor_logs(self, mocker):
        """
        Pytest fixture for mocking the get_cadvisor_logs function
        :param mocker: The pytest mocker object
        :return: The mocked function
        """
        def get_cadvisor_logs(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE}":
                    654321}
        get_cadvisor_logs_mocker = mocker.MagicMock(
            side_effect=get_cadvisor_logs)
        return get_cadvisor_logs_mocker

    @pytest.fixture
    def pgadmin_logs(self, mocker):
        """
        Pytest fixture for mocking the get_pgadmin_logs function
        :param mocker: The pytest mocker object
        :return: The mocked function
        """
        def get_pgadmin_logs(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.PGADMIN_RESOURCE}":
                    654321}
        get_pgadmin_logs_mocker = mocker.MagicMock(
            side_effect=get_pgadmin_logs)
        return get_pgadmin_logs_mocker

    @pytest.fixture
    def grafana_logs(self, mocker):
        """
        Pytest fixture for mocking the get_grafana_logs function
        :param mocker: The pytest mocker object
        :return: The mocked function
        """
        def get_grafana_logs(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.GRAFANA_RESOURCE}":
                    654321}
        get_grafana_logs_mocker = mocker.MagicMock(
            side_effect=get_grafana_logs)
        return get_grafana_logs_mocker

    def test_logs_post(self, flask_app, not_logged_in, logged_in,
                       logged_in_as_admin,
                       mocker: pytest_mock.MockFixture,
                       example_config, csle_logs,
                       dsm_logs, prom_logs, nginx_logs,
                       postgresql_logs, flask_logs,
                       cluster_manager_logs,
                       docker_logs, node_exporter_logs,
                       cadvisor_logs, pgadmin_logs,
                       grafana_logs,
                       ) -> None:
        """
        Tests the POST HTTPS method for the /logs resource

        :param flask_app: the flask app representing the web server
        :param mocker: the mocker object for mocking functions
        :param database: the database fixture
        :param token: the token fixture
        :param save: the save fixture
        :param update: the update fixture
        :return: None
        """
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "get_csle_log_files", side_effect=csle_logs)
        mocker_list = [dsm_logs, prom_logs, nginx_logs, postgresql_logs,
                       flask_logs, cluster_manager_logs, docker_logs,
                       node_exporter_logs, cadvisor_logs, pgadmin_logs,
                       grafana_logs]
        corr_func_names = ["get_docker_statsmanager_logs",
                           "get_prometheus_logs", "get_nginx_logs", "get_postgresql_logs",
                           "get_flask_logs", "get_cluster_manager_logs",
                           "get_docker_logs", "get_node_exporter_logs",
                           "get_cadvisor_logs", "get_pgadmin_logs",
                           "get_grafana_logs"]
        constants_list = [api_constants.MGMT_WEBAPP.DOCKER_STATS_MANAGER_SUBRESOURCE,
                          api_constants.MGMT_WEBAPP.PROMETHEUS_RESOURCE, api_constants.MGMT_WEBAPP.NGINX_RESOURCE,
                          api_constants.MGMT_WEBAPP.POSTGRESQL_RESOURCE, api_constants.MGMT_WEBAPP.FLASK_RESOURCE,
                          api_constants.MGMT_WEBAPP.CLUSTERMANAGER_RESOURCE, api_constants.MGMT_WEBAPP.DOCKER_RESOURCE,
                          api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE, api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE,
                          api_constants.MGMT_WEBAPP.PGADMIN_RESOURCE, api_constants.MGMT_WEBAPP.GRAFANA_RESOURCE,
                          ]
        for i in range(len(mocker_list)):
            mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                         side_effect=not_logged_in)
            path = \
                "csle_cluster.cluster_manager.cluster_controller.ClusterController."f"{corr_func_names[i]}"
            mocker.patch(path, side_effect=mocker_list[i])
            mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                         side_effect=logged_in)
            response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.LOGS_RESOURCE}"
                                                    f"{constants.COMMANDS.SLASH_DELIM}"
                                                    f"{constants_list[i]}",
                                                    data=json.dumps({}))
            response_data = response.data.decode("utf-8")
            response_data_dict = json.loads(response_data)
            assert response_data_dict == {}
            assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
            config = example_config
            config_cluster_dict = config.cluster_config.to_dict()['cluster_nodes'][0]
            mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                         side_effect=logged_in_as_admin)
            response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.LOGS_RESOURCE}"
                                                    f"{constants.COMMANDS.SLASH_DELIM}"
                                                    f"{constants_list[i]}",
                                                    data=json.dumps(config_cluster_dict))
            response_data = response.data.decode("utf-8")
            response_data_dict = json.loads(response_data)
            assert response.status_code == constants.HTTPS.OK_STATUS_CODE
            assert response_data_dict == {f"{constants_list[i]}": 654321}
            del config_cluster_dict["ip"]
            response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.LOGS_RESOURCE}"
                                                    f"{constants.COMMANDS.SLASH_DELIM}"
                                                    f"{constants_list[i]}",
                                                    data=json.dumps(config_cluster_dict))

            response_data = response.data.decode("utf-8")
            response_data_dict = json.loads(response_data)
            assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
            assert response_data_dict == {}
