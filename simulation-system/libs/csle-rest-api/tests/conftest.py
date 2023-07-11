
from typing import List

import csle_common.constants.constants as constants
import pytest
from csle_cluster.cluster_manager.cluster_manager_pb2 import (
    NodeStatusDTO,
    OperationOutcomeDTO,
)
from csle_common.dao.emulation_config.cluster_config import ClusterConfig
from csle_common.dao.emulation_config.cluster_node import ClusterNode
from csle_common.dao.emulation_config.config import Config
from csle_common.dao.management.management_user import ManagementUser
from flask import jsonify

import csle_rest_api.constants.constants as api_constants


@pytest.fixture
def pid_false(mocker):
    """
    Pytest fixture for mocking the check_pid function
    :param mocker: The pytest mocker object
    :return: A mocker object with the mocked function
    """
    def check_pid(ip: str, port: int, pid: int) -> OperationOutcomeDTO:
        op_outcome = OperationOutcomeDTO(outcome=False)
        return op_outcome
    check_pid_mocker = mocker.MagicMock(side_effect=check_pid)

    return check_pid_mocker


@pytest.fixture
def pid_true(mocker):
    """
    Pytest fixture for mocking the check_pid function
    :param mocker: The pytest mocker object
    :return: a mocker object with the mocked function
    """
    def check_pid(ip: str, port: int, pid: int) -> OperationOutcomeDTO:
        op_outcome = OperationOutcomeDTO(outcome=True)
        return op_outcome
    check_pid_mocker = mocker.MagicMock(side_effect=check_pid)

    return check_pid_mocker


@pytest.fixture
def stop(mocker) -> None:
    """
    Pytest fixture mocking the stop_pid functio

    :param mocker: the pytest mocker object
    :return: a mock object with the mocked function

    """
    def stop_pid(ip: str, port: int, pid: int) -> None:
        return None
    stop_pid_mocker = mocker.MagicMock(side_effect=stop_pid)
    return stop_pid_mocker


@pytest.fixture
def example_config():
    """
    Help function that returns a config class when making
    fixtures and testing
    :return: Config class
    """
    c_node = ClusterNode(ip="123.456.78.99", leader=True, cpus=1, gpus=2, RAM=3)
    config = Config(
        management_admin_username_default="admin",
        management_admin_password_default="admin",
        management_admin_first_name_default="Admin",
        management_admin_last_name_default="Adminson",
        management_admin_email_default="admin@CSLE.com",
        management_admin_organization_default="CSLE",
        management_guest_username_default="guest",
        management_guest_password_default="guest",
        management_guest_first_name_default="Guest",
        management_guest_last_name_default="Guestson",
        management_guest_email_default="guest@CSLE.com",
        management_guest_organization_default="CSLE",
        ssh_admin_username="null",
        ssh_admin_password="null",
        ssh_agent_username="null",
        ssh_agent_password="null",
        metastore_user="null",
        metastore_password="null",
        metastore_database_name="null",
        metastore_ip="null",
        node_exporter_port=1,
        grafana_port=1,
        management_system_port=1,
        cadvisor_port=1,
        prometheus_port=1,
        node_exporter_pid_file="null",
        pgadmin_port=1,
        csle_mgmt_webapp_pid_file="null",
        docker_stats_manager_log_file="null",
        docker_stats_manager_log_dir="null",
        docker_stats_manager_port=1,
        docker_stats_manager_max_workers=1,
        docker_stats_manager_outfile="null",
        docker_stats_manager_pidfile="null",
        prometheus_pid_file="null",
        prometheus_log_file="null",
        prometheus_config_file="null",
        default_log_dir="null",
        cluster_config=ClusterConfig([c_node]),
        node_exporter_log_file="null",
        allow_registration=True,
        grafana_username="null",
        grafana_password="null",
        pgadmin_username="null",
        pgadmin_password="null",
        postgresql_log_dir="null",
        nginx_log_dir="null",
        flask_log_file="null",
        cluster_manager_log_file="null",
    )
    return config


@pytest.fixture
def example_node_status() -> NodeStatusDTO:
    """
    Help function that returns an example node status

    :return: the example node status
    """
    node_status = NodeStatusDTO(
        ip="123.456.78.99",
        leader=True,
        cAdvisorRunning=True,
        prometheusRunning=True,
        grafanaRunning=True,
        pgAdminRunning=True,
        nginxRunning=True,
        flaskRunning=True,
        dockerStatsManagerRunning=True,
        nodeExporterRunning=True,
        postgreSQLRunning=True,
        dockerEngineRunning=True
    )
    return node_status


@pytest.fixture
def authorized(mocker):
    """
    Fixture for mocking the check_if_user_edit_is_authorized function

    :param mocker: the pytest mocker object
    :return: fixture for mocking the check_if_user_edit_is_authorized function
    """

    def check_if_user_edit_is_authorized(request, user: ManagementUser):
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token != "":
            return user
        response = jsonify({})
        response.headers.add(
            api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*"
        )
        return response, constants.HTTPS.UNAUTHORIZED_STATUS_CODE

    check_if_user_edit_is_authorized_mock = mocker.MagicMock(
        side_effect=check_if_user_edit_is_authorized
    )
    return check_if_user_edit_is_authorized_mock


@pytest.fixture
def unauthorized(mocker):
    """
    Fixture for mocking the check_if_user_edit_is_authorized function

    :param mocker: the pytest mocker object
    :return: fixture for mocking the check_if_user_edit_is_authorized function
    """

    def check_if_user_edit_is_authorized(request, user: ManagementUser):
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token == "":
            response = jsonify({})
            response.headers.add(
                api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*"
            )
            return response, constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        return user

    check_if_user_edit_is_authorized_mock = mocker.MagicMock(
        side_effect=check_if_user_edit_is_authorized
    )
    return check_if_user_edit_is_authorized_mock


@pytest.fixture
def logged_in_as_admin(mocker):
    """
    Fixture for mocking the logged-in-as-admin side effect

    :param mocker: the pytest mocker object
    :return: the logged in as admin fixture for mocking the logged in check
    """

    def check_if_user_is_authorized(request, requires_admin):
        return None

    check_if_user_is_authorized_mock = mocker.MagicMock(
        side_effect=check_if_user_is_authorized
    )
    return check_if_user_is_authorized_mock


@pytest.fixture
def logged_in(mocker):
    """
    Fixture for mocking the logged-in side effect

    :param mocker: the pytest mocker object
    :return: the logged in fixture for mocking the logged in check
    """

    def check_if_user_is_authorized(request, requires_admin):
        if requires_admin:
            response = jsonify({})
            response.headers.add(
                api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*"
            )
            return response, constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        return None

    check_if_user_is_authorized_mock = mocker.MagicMock(
        side_effect=check_if_user_is_authorized
    )
    return check_if_user_is_authorized_mock


@pytest.fixture
def not_logged_in(mocker):
    """
    Fixture for mocking the not-logged-in side effect

    :param mocker: the pytest mocker object
    :return: the not-logged-in fixture for mocking the logged in check
    """

    def check_if_user_is_authorized(request, requires_admin):
        response = jsonify({})
        return response, constants.HTTPS.UNAUTHORIZED_STATUS_CODE

    check_if_user_is_authorized_mock = mocker.MagicMock(
        side_effect=check_if_user_is_authorized
    )
    return check_if_user_is_authorized_mock


@pytest.fixture
def cluster_node_status(example_config: Config,
                        example_node_status: NodeStatusDTO) -> List[dict]:
    """
    Staticmethod that reurns an example cluster node status, that is
    to be tested against the mocking ofthe API
    :param example_config: an example Config class
    :param exmaple_node_status: an example node status class
    :return: a list of a dict containing an example cluster node status
    """
    config = example_config
    cluster_statuses = []
    for node in config.cluster_config.cluster_nodes:
        node_status = example_node_status
        cluster_status_dict = {
            api_constants.MGMT_WEBAPP.CADVISOR_RUNNING_PROPERTY: node_status.cAdvisorRunning,
            api_constants.MGMT_WEBAPP.GRAFANA_RUNNING_PROPERTY: node_status.grafanaRunning,
            api_constants.MGMT_WEBAPP.POSTGRESQL_RUNNING_PROPERTY: node_status.postgreSQLRunning,
            api_constants.MGMT_WEBAPP.NODE_EXPORTER_RUNNING_PROPERTY: node_status.nodeExporterRunning,
            api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY: node_status.dockerEngineRunning,
            api_constants.MGMT_WEBAPP.NGINX_RUNNING_PROPERTY: node_status.nginxRunning,
            api_constants.MGMT_WEBAPP.FLASK_RUNNING_PROPERTY: node_status.flaskRunning,
            api_constants.MGMT_WEBAPP.PROMETHEUS_RUNNING_PROPERTY: node_status.prometheusRunning,
            api_constants.MGMT_WEBAPP.PGADMIN_RUNNING_PROPERTY: node_status.pgAdminRunning,
            api_constants.MGMT_WEBAPP.CADVISOR_URL_PROPERTY:
            f"http://{node.ip}:{constants.COMMANDS.CADVISOR_PORT}/",
            api_constants.MGMT_WEBAPP.GRAFANA_URL_PROPERTY: f"http://{node.ip}:{constants.COMMANDS.GRAFANA_PORT}/",
            api_constants.MGMT_WEBAPP.NODE_EXPORTER_URL_PROPERTY: f"http://{node.ip}:"
            f"{constants.COMMANDS.NODE_EXPORTER_PORT}/",
            api_constants.MGMT_WEBAPP.FLASK_URL_PROPERTY: f"http://{node.ip}:{constants.COMMANDS.FLASK_PORT}/",
            api_constants.MGMT_WEBAPP.PROMETHEUS_URL_PROPERTY: f"http://{node.ip}:"
                                                            f"{constants.COMMANDS.PROMETHEUS_PORT}/",
            api_constants.MGMT_WEBAPP.PGADMIN_URL_PROPERTY: f"http://{node.ip}:{constants.COMMANDS.PGADMIN_PORT}/",
            api_constants.MGMT_WEBAPP.CADVISOR_PORT_PROPERTY: constants.COMMANDS.CADVISOR_PORT,
            api_constants.MGMT_WEBAPP.GRAFANA_PORT_PROPERTY: constants.COMMANDS.GRAFANA_PORT,
            api_constants.MGMT_WEBAPP.NODE_EXPORTER_PORT_PROPERTY: constants.COMMANDS.NODE_EXPORTER_PORT,
            api_constants.MGMT_WEBAPP.FLASK_PORT_PROPERTY: constants.COMMANDS.FLASK_PORT,
            api_constants.MGMT_WEBAPP.PROMETHEUS_PORT_PROPERTY: constants.COMMANDS.PROMETHEUS_PORT,
            api_constants.MGMT_WEBAPP.PGADMIN_PORT_PROPERTY: constants.COMMANDS.PGADMIN_PORT,
            api_constants.MGMT_WEBAPP.IP_PROPERTY: node.ip,
            api_constants.MGMT_WEBAPP.CPUS_PROPERTY: node.cpus,
            api_constants.MGMT_WEBAPP.GPUS_PROPERTY: node.gpus,
            api_constants.MGMT_WEBAPP.RAM_PROPERTY: node.RAM,
            api_constants.MGMT_WEBAPP.LEADER_PROPERTY: node.leader
        }
        cluster_statuses.append(cluster_status_dict)
    return cluster_statuses
