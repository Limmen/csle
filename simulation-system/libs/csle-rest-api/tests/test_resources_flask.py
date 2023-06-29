import json
import logging

import csle_common.constants.constants as constants
import pytest
from csle_cluster.cluster_manager.cluster_manager_pb2 import NodeStatusDTO
from csle_common.dao.emulation_config.cluster_config import ClusterConfig
from csle_common.dao.emulation_config.cluster_node import ClusterNode
from csle_common.dao.emulation_config.config import Config
from flask import jsonify

import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesConfigSuite(object):
    """
        Test suite for /config resource
    """
    pytest.logger = logging.getLogger("resources_users_tests")

    @pytest.fixture
    def flask_app(self):
        """
        :return: the flask app fixture representing the webserver
        """
        return create_app(
            static_folder="../../../../../management-system/csle-mgmt-webapp/build"
        )

    @pytest.fixture
    def logged_in_as_admin(self, mocker):
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
    def logged_in(self, mocker):
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
    def not_logged_in(self, mocker):
        """
        Fixture for mocking the not-logged-in side effect

        :param mocker: the pytest mocker object
        :return: the not-logged-in fixture for mocking the logged in check
        """

        def check_if_user_is_authorized(request, requires_admin):
            response = jsonify({})
            response.headers.add(
                api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*"
            )
            return response, constants.HTTPS.UNAUTHORIZED_STATUS_CODE

        check_if_user_is_authorized_mock = mocker.MagicMock(
            side_effect=check_if_user_is_authorized
        )
        return check_if_user_is_authorized_mock

    @pytest.fixture
    def config(self, mocker):
        """
        Fixture for mocking the config side-effect
        """
        def get_config(id):

            c_node = ClusterNode(ip="12.345.67.89", leader=True, cpus=1, gpus=2, RAM=3)
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
        get_config_mock = mocker.MagicMock(side_effect=get_config)
        return get_config_mock
    @pytest.fixture
    def node_status(self, mocker):
        """Mock object for the node_status fixture
        :param :
        :return :
        """

        def get_node_status(ip, port):
            class MockedNodeStatusDTO():
                def __init__(self, ip="12.345.67.89", leader=True,
                            cAdvisorRunning=False, prometheusRunning=False,
                            grafanaRunning=False, pgAdminRunning=False,
                            nginxRunning=False, flaskRunning=False,
                            dockerStatsManagerRunning=False,
                            nodeExporterRunning=False, postgreSQLRunning=False,
                            dockerEngineRunning=False):
                    self.ip = ip
                    self.leader = leader
                    self.cAdvisorRunning = cAdvisorRunning
                    self.prometheusRunning = prometheusRunning
                    self.grafanaRunning = grafanaRunning
                    self.pgAdminRunning = pgAdminRunning
                    self.nginxRunning = nginxRunning
                    self.flaskRunning = flaskRunning
                    self.dockerStatsManagerRunning = dockerStatsManagerRunning
                    self.nodeExporterRunning = nodeExporterRunning
                    self.postgreSQLRunning = postgreSQLRunning
                    self.dockerEngineRunning = dockerEngineRunning
            return MockedNodeStatusDTO

        get_node_status_mock = mocker.MagicMock(side_effect=get_node_status)
        return get_node_status_mock

    def test_flask(self,
            flask_app,
            mocker,
            logged_in_as_admin,
            logged_in,
            not_logged_in,
            config,
            node_status
            ):
        """
        Testing the /flask url
        :param :
        :return : None
        """
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.FLASK_RESOURCE, 
                                                data=json.dumps({}))
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE

        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.get_config",
            side_effect=config,
        )
        mocker.patch(
            "csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO",
            side_effect=node_status,
        )

        c_node = ClusterNode(ip="12.345.67.89", leader=True, cpus=1, gpus=2, RAM=3)
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
        # pytest.logger.info(config)
        # pytest.logger.info(type(config.cluster_config.to_dict()['cluster_nodes'][0]))
        config_cluster_dict = config.cluster_config.to_dict()['cluster_nodes'][0]
        response = flask_app.test_client().post(api_constants.MGMT_WEBAPP.FLASK_RESOURCE,
                                                data=json.dumps(config_cluster_dict))
