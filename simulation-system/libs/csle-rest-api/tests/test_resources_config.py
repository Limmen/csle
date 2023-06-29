import json
import logging

import csle_common.constants.constants as constants
import pytest
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
    def save(self, mocker):
        """
        Fixture for mocking the save side effect
        param: config
        return: None
        """
        def save_config_file(config) -> None:
            return None
        save_config_file_mocker = mocker.MagicMock(
            side_effect=save_config_file
        )
        return save_config_file_mocker

    @pytest.fixture
    def from_config_file(self, mocker):
        """
        Fixture for mocking the from_config_file side effect
        params:
        return: None
        """
        def set_config_parameters_from_config_file() -> None:
            return None

        set_config_parameters_from_config_file_mocker = mocker.MagicMock(
            side_effect=set_config_parameters_from_config_file
        )
        return set_config_parameters_from_config_file_mocker

    @pytest.fixture
    def config_read(self, mocker):
        """
        Fixture for mocking the config_read side effect.

        :param mocker: the pytest mocker object
        :return: the Config fixture for mocking read_config_file
        """
        def read_config_file() -> Config:
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
        read_config_file_mock = mocker.MagicMock(
            side_effect=read_config_file
        )
        return read_config_file_mock

    @pytest.fixture
    def failed_config_read(self, mocker):
        """
        Fixture for mocking the config_read side effect when generating error.

        :param mocker: the pytest mocker object
        :return: the Config fixture for mocking read_config_file
        """
        def read_config_file():
            c_node = "This is clearly the wrong datatype for cluster"
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
        read_failed_config_file_mock = mocker.MagicMock(
            side_effect=read_config_file
        )
        return read_failed_config_file_mock

    def test_config(
            self,
            flask_app,
            mocker,
            logged_in,
            logged_in_as_admin,
            not_logged_in,
            config_read,
            failed_config_read,
            save, from_config_file,):
        """
        Tests the /config resource for listing management user accounts

        :param : flask_app: the flask app representing the web server
        :param : mocker: the mocker object for mocking functions
        :param : logged_in_as_admin: the logged_in_as_admin fixture
        :param : logged_in: the logged_in fixture
        :param : not_logged_in: the not_logged_in fixture
        :param : config_read: the config_read fixture
        :param : failed_config_read : the failed_config_read fixture
        :param : save : the save fixture
        :param : from_config_file: the from_config_file fixture
        :return : None
        """
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )

        mocker.patch(
            "csle_common.dao.emulation_config.config.Config.read_config_file",
            side_effect=failed_config_read,
        )
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.CONFIG_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.INTERNAL_SERVER_ERROR_STATUS_CODE
        mocker.patch(
            "csle_common.dao.emulation_config.config.Config.read_config_file",
            side_effect=config_read,
        )
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.CONFIG_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        config = Config.from_param_dict(response_data_list)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert config.management_admin_username_default == "admin"
        assert config.management_admin_password_default == "admin"
        assert config.management_admin_first_name_default == "Admin"
        assert config.management_admin_last_name_default == "Adminson"
        assert config.management_admin_email_default == "admin@CSLE.com"
        assert config.management_admin_organization_default == "CSLE"
        assert config.ssh_admin_username == "null"
        assert config.ssh_admin_password == "null"
        assert config.ssh_agent_username == "null"
        assert config.ssh_agent_password == "null"
        assert config.management_guest_username_default == "guest"
        assert config.management_guest_password_default == "guest"
        assert config.management_guest_first_name_default == "Guest"
        assert config.management_guest_last_name_default == "Guestson"
        assert config.management_guest_email_default == "guest@CSLE.com"
        assert config.management_guest_organization_default == "CSLE"
        assert config.metastore_user == "null"
        assert config.metastore_password == "null"
        assert config.metastore_ip == "null"
        assert config.metastore_database_name == "null"
        assert config.node_exporter_pid_file == "null"
        assert config.node_exporter_log_file == "null"
        assert config.csle_mgmt_webapp_pid_file == "null"
        assert config.grafana_username == "null"
        assert config.grafana_password == "null"
        assert config.node_exporter_port == 1
        assert config.grafana_port == 1
        assert config.management_system_port == 1
        assert config.prometheus_port == 1
        assert config.node_exporter_port == 1
        assert config.cadvisor_port == 1
        assert config.docker_stats_manager_log_dir == "null"
        assert config.docker_stats_manager_log_file == "null"
        assert config.docker_stats_manager_max_workers == 1
        assert config.docker_stats_manager_outfile == "null"
        assert config.docker_stats_manager_pidfile == "null"
        assert config.docker_stats_manager_port == 1
        assert config.cluster_config.cluster_nodes[0].ip == "12.345.67.89"
        assert config.cluster_config.cluster_nodes[0].leader is True
        assert config.cluster_config.cluster_nodes[0].cpus == 1
        assert config.cluster_config.cluster_nodes[0].gpus == 2
        assert config.cluster_config.cluster_nodes[0].RAM == 3
        assert config.allow_registration is True
        assert config.id == 1
        assert config.pgadmin_username == "null"
        assert config.pgadmin_password == "null"
        assert config.postgresql_log_dir == "null"
        assert config.nginx_log_dir == "null"
        assert config.flask_log_file == "null"
        assert config.cluster_manager_log_file == "null"
        pytest.logger.info(config.cluster_config.to_dict()['cluster_nodes'][0]['ip'])
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.CONFIG_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE

        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.CONFIG_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE

        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )
        mocker.patch(
            "csle_common.dao.emulation_config.config.Config.save_config_file",
            side_effect=save,
        )
        mocker.patch(
            "csle_common.util.cluster_util.ClusterUtil.set_config_parameters_from_config_file",
            side_effect=from_config_file,
        )
        response = flask_app.test_client().put(api_constants.MGMT_WEBAPP.CONFIG_RESOURCE,
                                               data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_list == {}
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
        config_dict = Config.to_param_dict(config)
        response = flask_app.test_client().put(api_constants.MGMT_WEBAPP.CONFIG_RESOURCE,
                                               data=json.dumps({"config": config_dict}))
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        config = Config.from_param_dict(response_data_list)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert config.management_admin_username_default == "admin"
        assert config.management_admin_password_default == "admin"
        assert config.management_admin_first_name_default == "Admin"
        assert config.management_admin_last_name_default == "Adminson"
        assert config.management_admin_email_default == "admin@CSLE.com"
        assert config.management_admin_organization_default == "CSLE"
        assert config.ssh_admin_username == "null"
        assert config.ssh_admin_password == "null"
        assert config.ssh_agent_username == "null"
        assert config.ssh_agent_password == "null"
        assert config.management_guest_username_default == "guest"
        assert config.management_guest_password_default == "guest"
        assert config.management_guest_first_name_default == "Guest"
        assert config.management_guest_last_name_default == "Guestson"
        assert config.management_guest_email_default == "guest@CSLE.com"
        assert config.management_guest_organization_default == "CSLE"
        assert config.metastore_user == "null"
        assert config.metastore_password == "null"
        assert config.metastore_ip == "null"
        assert config.metastore_database_name == "null"
        assert config.node_exporter_pid_file == "null"
        assert config.node_exporter_log_file == "null"
        assert config.csle_mgmt_webapp_pid_file == "null"
        assert config.grafana_username == "null"
        assert config.grafana_password == "null"
        assert config.node_exporter_port == 1
        assert config.grafana_port == 1
        assert config.management_system_port == 1
        assert config.prometheus_port == 1
        assert config.node_exporter_port == 1
        assert config.cadvisor_port == 1
        assert config.docker_stats_manager_log_dir == "null"
        assert config.docker_stats_manager_log_file == "null"
        assert config.docker_stats_manager_max_workers == 1
        assert config.docker_stats_manager_outfile == "null"
        assert config.docker_stats_manager_pidfile == "null"
        assert config.docker_stats_manager_port == 1
        assert config.cluster_config.cluster_nodes[0].ip == "12.345.67.89"
        assert config.cluster_config.cluster_nodes[0].leader is True
        assert config.cluster_config.cluster_nodes[0].cpus == 1
        assert config.cluster_config.cluster_nodes[0].gpus == 2
        assert config.cluster_config.cluster_nodes[0].RAM == 3
        assert config.allow_registration is True
        assert config.id == 1
        assert config.pgadmin_username == "null"
        assert config.pgadmin_password == "null"
        assert config.postgresql_log_dir == "null"
        assert config.nginx_log_dir == "null"
        assert config.flask_log_file == "null"
        assert config.cluster_manager_log_file == "null"
        del config_dict["parameters"][0]
        response = flask_app.test_client().put(api_constants.MGMT_WEBAPP.CONFIG_RESOURCE,
                                               data=json.dumps({"config": config_dict}))
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE

    def test_registration_allowed(self, flask_app,):
        """
        Testing the config/registration-allowed resource
        :param : self
        :param : flask_app
        :return : None
        """
        c_node = ClusterNode(ip="12.345.67.89", leader=True, cpus=1, gpus=2, RAM=3)
        constants.CONFIG_FILE.PARSED_CONFIG = Config(
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
        response = flask_app.test_client().get(
            f"{api_constants.MGMT_WEBAPP.CONFIG_RESOURCE}"
            f"{constants.COMMANDS.SLASH_DELIM}"
            f"{api_constants.MGMT_WEBAPP.REGISTRATION_ALLOWED_SUBRESOURCE}",)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
