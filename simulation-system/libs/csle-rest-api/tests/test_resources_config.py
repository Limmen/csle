import json
import logging

import csle_common.constants.constants as constants
import pytest
from csle_common.dao.emulation_config.config import Config

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
    def config_read(self, mocker, example_config):
        """
        Fixture for mocking the config_read side effect.

        :param mocker: the pytest mocker object
        :return: the Config fixture for mocking read_config_file
        """

        def read_config_file() -> Config:
            return example_config

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
            raise ValueError("Test")

        read_failed_config_file_mock = mocker.MagicMock(
            side_effect=read_config_file
        )
        return read_failed_config_file_mock

    @pytest.mark.usefixtures("logged_in", "logged_in_as_admin", "not_logged_in")
    def test_config_get(
            self,
            flask_app,
            mocker,
            logged_in,
            logged_in_as_admin,
            not_logged_in,
            config_read,
            failed_config_read,
            save, from_config_file, ):
        """
        Tests the GET HTTPS method for the /config resource for listing management user accounts

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
        assert config.cluster_config.cluster_nodes[0].ip == "123.456.78.99"
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

    def test_config_put(
            self,
            flask_app,
            mocker,
            logged_in_as_admin,
            config_read,
            failed_config_read,
            save, from_config_file, example_config):
        """
        Tests the PUT HTTPS method for the /config resource for listing management user accounts

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
            "csle_common.dao.emulation_config.config.Config.read_config_file",
            side_effect=config_read,
        )
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
        config = example_config
        config_dict = Config.to_param_dict(config)
        response = flask_app.test_client().put(
            api_constants.MGMT_WEBAPP.CONFIG_RESOURCE,
            data=json.dumps({api_constants.MGMT_WEBAPP.CONFIG_PROPERTY: config_dict}))
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
        assert config.cluster_config.cluster_nodes[0].ip == "123.456.78.99"
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
        del config_dict[api_constants.MGMT_WEBAPP.PARAMETERS_PROPERTY][0]
        response = flask_app.test_client().put(api_constants.MGMT_WEBAPP.CONFIG_RESOURCE,
                                               data=json.dumps(
                                                   {api_constants.MGMT_WEBAPP.CONFIG_PROPERTY: config_dict}))
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE

    def test_registration_allowed(self, flask_app, example_config):
        """
        Testing the config/registration-allowed resource
        :param : self
        :param : flask_app
        :return : None
        """
        constants.CONFIG_FILE.PARSED_CONFIG = example_config
        response = flask_app.test_client().get(
            f"{api_constants.MGMT_WEBAPP.CONFIG_RESOURCE}"
            f"{constants.COMMANDS.SLASH_DELIM}"
            f"{api_constants.MGMT_WEBAPP.REGISTRATION_ALLOWED_SUBRESOURCE}")
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
