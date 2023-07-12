import json
import pytest
import pytest_mock
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.config import Config
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesConfigSuite:
    """
    Test suite for /config resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def save(self, mocker: pytest_mock.MockFixture):
        """
        Fixture for mocking the save side effect

        param: mocker the pytest mocker object
        return: the mock
        """

        def save_config_file(config: Config) -> None:
            return None

        save_config_file_mocker = mocker.MagicMock(
            side_effect=save_config_file
        )
        return save_config_file_mocker

    @pytest.fixture
    def from_config_file(self, mocker: pytest_mock.MockFixture):
        """
        Fixture for mocking the from_config_file side effect

        param: mocker the pytest mocker object
        return: the mock
        """
        def set_config_parameters_from_config_file() -> None:
            return None
        set_config_parameters_from_config_file_mocker = mocker.MagicMock(
            side_effect=set_config_parameters_from_config_file
        )
        return set_config_parameters_from_config_file_mocker

    @pytest.fixture
    def config_read(self, mocker: pytest_mock.MockFixture, example_config):
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
    def failed_config_read(self, mocker: pytest_mock.MockFixture):
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

    def test_config_get(self, flask_app, mocker: pytest_mock.MockFixture, logged_in, logged_in_as_admin,
                        not_logged_in, config_read, failed_config_read, save, from_config_file, example_config):
        """
        Tests the GET HTTPS method for the /config resource for listing management user accounts

        :param flask_app: the flask app representing the web server
        :param mocker: the mocker object for mocking functions
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param config_read: the config_read fixture
        :param failed_config_read : the failed_config_read fixture
        :param save : the save fixture
        :param from_config_file: the from_config_file fixture
        :param example_config: the example_config fixture
        :return : None
        """
        example_c: Config = example_config
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        mocker.patch("csle_common.dao.emulation_config.config.Config.read_config_file", side_effect=failed_config_read)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.CONFIG_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.INTERNAL_SERVER_ERROR_STATUS_CODE
        mocker.patch("csle_common.dao.emulation_config.config.Config.read_config_file", side_effect=config_read)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.CONFIG_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        config = Config.from_param_dict(response_data_list)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert config.management_admin_username_default == example_c.management_admin_username_default
        assert config.management_admin_password_default == example_c.management_admin_password_default
        assert config.management_admin_first_name_default == example_c.management_admin_first_name_default
        assert config.management_admin_last_name_default == example_c.management_admin_last_name_default
        assert config.management_admin_email_default == example_c.management_admin_email_default
        assert config.management_admin_organization_default == example_c.management_admin_organization_default
        assert config.ssh_admin_username == example_c.ssh_admin_username
        assert config.ssh_admin_password == example_c.ssh_admin_password
        assert config.ssh_agent_username == example_c.ssh_agent_username
        assert config.ssh_agent_password == example_c.ssh_agent_password
        assert config.management_guest_username_default == example_c.management_guest_username_default
        assert config.management_guest_password_default == example_c.management_guest_password_default
        assert config.management_guest_first_name_default == example_c.management_guest_first_name_default
        assert config.management_guest_last_name_default == example_c.management_guest_last_name_default
        assert config.management_guest_email_default == example_c.management_guest_email_default
        assert config.management_guest_organization_default == example_c.management_guest_organization_default
        assert config.metastore_user == example_c.metastore_user
        assert config.metastore_password == example_c.metastore_password
        assert config.metastore_ip == example_c.metastore_ip
        assert config.metastore_database_name == example_c.metastore_database_name
        assert config.node_exporter_pid_file == example_c.node_exporter_pid_file
        assert config.node_exporter_log_file == example_c.node_exporter_log_file
        assert config.csle_mgmt_webapp_pid_file == example_c.csle_mgmt_webapp_pid_file
        assert config.grafana_username == example_c.grafana_username
        assert config.grafana_password == example_c.grafana_password
        assert config.node_exporter_port == example_c.node_exporter_port
        assert config.grafana_port == example_c.grafana_port
        assert config.management_system_port == example_c.management_system_port
        assert config.prometheus_port == example_c.prometheus_port
        assert config.node_exporter_port == example_c.node_exporter_port
        assert config.cadvisor_port == example_c.cadvisor_port
        assert config.docker_stats_manager_log_dir == example_c.docker_stats_manager_log_dir
        assert config.docker_stats_manager_log_file == example_c.docker_stats_manager_log_file
        assert config.docker_stats_manager_max_workers == example_c.docker_stats_manager_max_workers
        assert config.docker_stats_manager_outfile == example_c.docker_stats_manager_outfile
        assert config.docker_stats_manager_pidfile == example_c.docker_stats_manager_pidfile
        assert config.docker_stats_manager_port == example_c.docker_stats_manager_port
        assert config.cluster_config.cluster_nodes[0].ip == example_c.cluster_config.cluster_nodes[0].ip
        assert config.cluster_config.cluster_nodes[0].leader == example_c.cluster_config.cluster_nodes[0].leader
        assert config.cluster_config.cluster_nodes[0].cpus == example_c.cluster_config.cluster_nodes[0].cpus
        assert config.cluster_config.cluster_nodes[0].gpus == example_c.cluster_config.cluster_nodes[0].gpus
        assert config.cluster_config.cluster_nodes[0].RAM == example_c.cluster_config.cluster_nodes[0].RAM
        assert config.allow_registration == example_c.allow_registration
        assert config.id == example_c.id
        assert config.pgadmin_username == example_c.pgadmin_username
        assert config.pgadmin_password == example_c.pgadmin_password
        assert config.postgresql_log_dir == example_c.postgresql_log_dir
        assert config.nginx_log_dir == example_c.nginx_log_dir
        assert config.flask_log_file == example_c.flask_log_file
        assert config.cluster_manager_log_file == example_c.cluster_manager_log_file
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.CONFIG_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.CONFIG_RESOURCE)
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        mocker.patch("csle_common.dao.emulation_config.config.Config.save_config_file", side_effect=save)
        mocker.patch("csle_common.util.cluster_util.ClusterUtil.set_config_parameters_from_config_file",
                     side_effect=from_config_file)

    def test_config_put(self, flask_app, mocker: pytest_mock.MockFixture, logged_in_as_admin, config_read,
                        failed_config_read, save, from_config_file, example_config) -> None:
        """
        Tests the PUT HTTPS method for the /config resource for listing management user accounts

        :param flask_app: the flask app representing the web server
        :param mocker: the mocker object for mocking functions
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param config_read: the config_read fixture
        :param failed_config_read : the failed_config_read fixture
        :param save : the save fixture
        :param from_config_file: the from_config_file fixture
        :param example_config: the example_config fixture
        :return None
        """
        mocker.patch("csle_common.dao.emulation_config.config.Config.read_config_file", side_effect=config_read)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        mocker.patch("csle_common.dao.emulation_config.config.Config.save_config_file", side_effect=save)
        mocker.patch("csle_common.util.cluster_util.ClusterUtil.set_config_parameters_from_config_file",
                     side_effect=from_config_file)
        response = flask_app.test_client().put(api_constants.MGMT_WEBAPP.CONFIG_RESOURCE,
                                               data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_list
        config = example_config
        config_dict = Config.to_param_dict(config)
        response = flask_app.test_client().put(
            api_constants.MGMT_WEBAPP.CONFIG_RESOURCE,
            data=json.dumps({api_constants.MGMT_WEBAPP.CONFIG_PROPERTY: config_dict}))
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        config = Config.from_param_dict(response_data_list)
        example_c = example_config
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert config.management_admin_username_default == example_c.management_admin_username_default
        assert config.management_admin_password_default == example_c.management_admin_password_default
        assert config.management_admin_first_name_default == example_c.management_admin_first_name_default
        assert config.management_admin_last_name_default == example_c.management_admin_last_name_default
        assert config.management_admin_email_default == example_c.management_admin_email_default
        assert config.management_admin_organization_default == example_c.management_admin_organization_default
        assert config.ssh_admin_username == example_c.ssh_admin_username
        assert config.ssh_admin_password == example_c.ssh_admin_password
        assert config.ssh_agent_username == example_c.ssh_agent_username
        assert config.ssh_agent_password == example_c.ssh_agent_password
        assert config.management_guest_username_default == example_c.management_guest_username_default
        assert config.management_guest_password_default == example_c.management_guest_password_default
        assert config.management_guest_first_name_default == example_c.management_guest_first_name_default
        assert config.management_guest_last_name_default == example_c.management_guest_last_name_default
        assert config.management_guest_email_default == example_c.management_guest_email_default
        assert config.management_guest_organization_default == example_c.management_guest_organization_default
        assert config.metastore_user == example_c.metastore_user
        assert config.metastore_password == example_c.metastore_password
        assert config.metastore_ip == example_c.metastore_ip
        assert config.metastore_database_name == example_c.metastore_database_name
        assert config.node_exporter_pid_file == example_c.node_exporter_pid_file
        assert config.node_exporter_log_file == example_c.node_exporter_log_file
        assert config.csle_mgmt_webapp_pid_file == example_c.csle_mgmt_webapp_pid_file
        assert config.grafana_username == example_c.grafana_username
        assert config.grafana_password == example_c.grafana_password
        assert config.node_exporter_port == example_c.node_exporter_port
        assert config.grafana_port == example_c.grafana_port
        assert config.management_system_port == example_c.management_system_port
        assert config.prometheus_port == example_c.prometheus_port
        assert config.node_exporter_port == example_c.node_exporter_port
        assert config.cadvisor_port == example_c.cadvisor_port
        assert config.docker_stats_manager_log_dir == example_c.docker_stats_manager_log_dir
        assert config.docker_stats_manager_log_file == example_c.docker_stats_manager_log_file
        assert config.docker_stats_manager_max_workers == example_c.docker_stats_manager_max_workers
        assert config.docker_stats_manager_outfile == example_c.docker_stats_manager_outfile
        assert config.docker_stats_manager_pidfile == example_c.docker_stats_manager_pidfile
        assert config.docker_stats_manager_port == example_c.docker_stats_manager_port
        assert config.cluster_config.cluster_nodes[0].ip == example_c.cluster_config.cluster_nodes[0].ip
        assert config.cluster_config.cluster_nodes[0].leader == example_c.cluster_config.cluster_nodes[0].leader
        assert config.cluster_config.cluster_nodes[0].cpus == example_c.cluster_config.cluster_nodes[0].cpus
        assert config.cluster_config.cluster_nodes[0].gpus == example_c.cluster_config.cluster_nodes[0].gpus
        assert config.cluster_config.cluster_nodes[0].RAM == example_c.cluster_config.cluster_nodes[0].RAM
        assert config.allow_registration == example_c.allow_registration
        assert config.id == example_c.id
        assert config.pgadmin_username == example_c.pgadmin_username
        assert config.pgadmin_password == example_c.pgadmin_password
        assert config.postgresql_log_dir == example_c.postgresql_log_dir
        assert config.nginx_log_dir == example_c.nginx_log_dir
        assert config.flask_log_file == example_c.flask_log_file
        assert config.cluster_manager_log_file == example_c.cluster_manager_log_file
        del config_dict[api_constants.MGMT_WEBAPP.PARAMETERS_PROPERTY][0]
        response = flask_app.test_client().put(api_constants.MGMT_WEBAPP.CONFIG_RESOURCE,
                                               data=json.dumps(
                                                   {api_constants.MGMT_WEBAPP.CONFIG_PROPERTY: config_dict}))
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE

    def test_registration_allowed(self, flask_app, example_config) -> None:
        """
        Testing the config/registration-allowed resource

        :param flask_app the flask app for making requests
        :param example_config: the example_config fixture
        :return None
        """
        constants.CONFIG_FILE.PARSED_CONFIG = example_config
        response = flask_app.test_client().get(
            f"{api_constants.MGMT_WEBAPP.CONFIG_RESOURCE}"
            f"{constants.COMMANDS.SLASH_DELIM}"
            f"{api_constants.MGMT_WEBAPP.REGISTRATION_ALLOWED_SUBRESOURCE}")
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
