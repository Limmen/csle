import json
from typing import List, Tuple, Union
import pytest
import pytest_mock
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.cluster_config import ClusterConfig
from csle_common.dao.emulation_config.cluster_node import ClusterNode
from csle_common.dao.emulation_config.config import Config
from csle_common.dao.management.management_user import ManagementUser

import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesUsersSuite:
    """
    Test suite for /users resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def management_users(self, mocker: pytest_mock.MockFixture):
        """
        Fixture for mocking the list of management users in the database

        :param mocker: the pytest mocker object
        :return: fixture for mocking the users in the database
        """

        def list_management_users() -> List[ManagementUser]:
            users = [
                TestResourcesUsersSuite.example_admin_user(),
                TestResourcesUsersSuite.example_guest_user()
            ]
            return users

        list_management_users_mock = mocker.MagicMock(side_effect=list_management_users)
        return list_management_users_mock

    @pytest.fixture
    def management_ids(self, mocker: pytest_mock.MockFixture):
        """
        Fixture for mocking the management user ids

        :param mocker: the pytest mocker object
        :return: fixture for mocking the management user ids
        """

        def list_management_users_ids() -> List[Tuple[int]]:
            return [(1,), (2,)]

        list_management_users_ids_mock = mocker.MagicMock(side_effect=list_management_users_ids)
        return list_management_users_ids_mock

    @staticmethod
    def example_admin_user() -> ManagementUser:
        """
        Help function that returns an example admin user

        :return: the example admin user
        """
        admin_user = ManagementUser(username="admin", password="admin", email="admin@CSLE.com", admin=True,
                                    first_name="Admin", last_name="Adminson", organization="CSLE", salt="123")
        admin_user.id = 11
        return admin_user

    @staticmethod
    def example_guest_user() -> ManagementUser:
        """
        Help function that returns an example guest user

        :return: the example guest user
        """
        guest_user = ManagementUser(username="guest", password="guest", email="guest@CSLE.com", admin=False,
                                    first_name="Guest", last_name="Guestson", organization="CSLE", salt="123")
        guest_user.id = 235
        return guest_user

    @pytest.fixture
    def management_config(self, mocker: pytest_mock.MockFixture):
        """
        Fixture for mocking the get_management_user_config function of the MetastoreFacade

        :param mocker: the pytest mocker object
        :return: fixture for mocking the get_management_user_config function of the MetastoreFacade
        """

        def get_management_user_config(id: int) -> Union[None, ManagementUser]:
            admin_user = TestResourcesUsersSuite.example_admin_user()
            guest_user = TestResourcesUsersSuite.example_guest_user()
            if id == admin_user.id:
                return admin_user
            elif id == guest_user.id:
                return guest_user
            else:
                return None

        get_management_user_config_mock = mocker.MagicMock(side_effect=get_management_user_config)
        return get_management_user_config_mock

    @pytest.fixture
    def update(self, mocker: pytest_mock.MockFixture):
        """
        Fixture for mocking the update_management_user of the MetastoreFacade

        :param mocker: the pytest mocker object
        :return: fixture for mocking the update_management_user of the MetastoreFacade
        """

        def update_management_user(management_user: ManagementUser, id: int) -> None:
            return None

        update_management_user_mock = mocker.MagicMock(side_effect=update_management_user)
        return update_management_user_mock

    @pytest.fixture
    def remove(self, mocker: pytest_mock.MockFixture):
        """
        Fixture for mocking the remove_management_user function of the Metastore

        :param mocker: the pytest mocker object
        :return: fixture for mocking the remove_management_user function of the Metastore
        """

        def remove_management_user(management_user: ManagementUser):
            return None

        remove_management_user_mock = mocker.MagicMock(side_effect=remove_management_user)
        return remove_management_user_mock

    @pytest.fixture
    def save(self, mocker: pytest_mock.MockFixture):
        """
        Fixture for mocking the save_management_user function in the MetastoreFacade

        :param mocker: the pytest mocker object
        :return: fixture for mocking the save_management_user function in the MetastoreFacade
        """

        def save_management_user(management_user: ManagementUser) -> int:
            return 1

        save_management_user_mock = mocker.MagicMock(side_effect=save_management_user)
        return save_management_user_mock

    def test_users_get(self, flask_app, mocker: pytest_mock.MockFixture, logged_in_as_admin, management_users,
                       not_logged_in, management_ids, logged_in) -> None:
        """
        Tests the GET HTTPS method /users resource for listing management user accounts

        :param flask_app: the flask app representing the web server
        :param mocker: the mocker object for mocking functions
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param management_users: the management_users fixture
        :param not_logged_in: the not_logged_in fixture
        :param management_ids: the management_ids fixture
        :param remove: the remove fixture
        :param logged_in: the logged_in fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_management_users",
                     side_effect=management_users)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        guest_user = TestResourcesUsersSuite.example_guest_user()
        admin_user = TestResourcesUsersSuite.example_admin_user()
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.USERS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert len(response_data_list) == 2
        users = list(map(lambda x: ManagementUser.from_dict(x), response_data_list))
        assert users[0].username == admin_user.username
        assert users[0].password == ""
        assert users[0].email == admin_user.email
        assert users[0].admin is admin_user.admin
        assert users[0].first_name == admin_user.first_name
        assert users[0].last_name == admin_user.last_name
        assert users[0].salt == ""
        assert users[0].organization == admin_user.organization
        assert users[1].username == guest_user.username
        assert users[1].password == ""
        assert users[1].email == guest_user.email
        assert users[1].admin is guest_user.admin
        assert users[1].first_name == guest_user.first_name
        assert users[1].last_name == guest_user.last_name
        assert users[1].salt == ""
        assert users[1].organization == guest_user.organization
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_management_users_ids",
                     side_effect=management_ids)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert len(response_data_list) == 2
        assert response_data_list[0][api_constants.MGMT_WEBAPP.ID_PROPERTY] == 1
        assert response_data_list[1][api_constants.MGMT_WEBAPP.ID_PROPERTY] == 2
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.USERS_RESOURCE)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert len(response_data_list) == 0
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.USERS_RESOURCE)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert len(response_data_list) == 0

    def test_users_delete(self, flask_app, mocker: pytest_mock.MockFixture, logged_in_as_admin, management_users,
                          not_logged_in, remove, logged_in) -> None:
        """
        Test the DELETE method on /users

        :param flask_app: the flask app for making the requests
        :param mocker: the mocker object from pytest
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param management_users: the management_users fixture
        :param not_logged_in: the not_logged_in fixture
        :param remove: the remove fixture
        :param logged_in: the logged_in fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_management_users",
                     side_effect=management_users)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_management_user",
                     side_effect=remove)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.USERS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.USERS_RESOURCE)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert len(response_data_list) == 0
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.USERS_RESOURCE)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert len(response_data_list) == 0

    def test_users_id_get(self, flask_app, mocker: pytest_mock.MockFixture, management_users, not_logged_in, logged_in,
                          authorized, unauthorized, management_config) -> None:
        """
        Testing the GET HTTPS method for the /users/id resource

        :param flask_app: the flask app representing the web server
        :param mocker: the mocker object for mocking functions
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param management_users: the management_users fixture
        :param not_logged_in: the not_logged_in fixture
        :param management_config: the management_config fixture
        :param remove: the remove fixture
        :param logged_in: the logged_in fixture
        :param authorized: the athourized fixture
        :param unauthorized: the unathourized fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_management_users",
                     side_effect=management_users)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_management_user_config",
                     side_effect=management_config)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_edit_is_authorized", side_effect=authorized)
        guest_user = TestResourcesUsersSuite.example_guest_user()
        admin_user = TestResourcesUsersSuite.example_admin_user()
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
                                               f"{constants.COMMANDS.SLASH_DELIM}{admin_user.id}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert len(response_data_list) == 9
        assert response_data_list[api_constants.MGMT_WEBAPP.ADMIN_PROPERTY] is admin_user.admin
        assert response_data_list[api_constants.MGMT_WEBAPP.EMAIL_PROPERTY] == admin_user.email
        assert response_data_list[api_constants.MGMT_WEBAPP.FIRST_NAME_PROPERTY] == admin_user.first_name
        assert response_data_list[api_constants.MGMT_WEBAPP.LAST_NAME_PROPERTY] == admin_user.last_name
        assert response_data_list[api_constants.MGMT_WEBAPP.ID_PROPERTY] == admin_user.id
        assert response_data_list[api_constants.MGMT_WEBAPP.ORGANIZATION_PROPERTY] == admin_user.organization
        assert response_data_list[api_constants.MGMT_WEBAPP.PASSWORD_PROPERTY] == ""
        assert response_data_list[api_constants.MGMT_WEBAPP.SALT_PROPOERTY] == ""
        assert response_data_list[api_constants.MGMT_WEBAPP.USERNAME_PROPERTY] == admin_user.username
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
                                               f"{constants.COMMANDS.SLASH_DELIM}{guest_user.id}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert len(response_data_list) == 9
        assert response_data_list[api_constants.MGMT_WEBAPP.ADMIN_PROPERTY] is guest_user.admin
        assert response_data_list[api_constants.MGMT_WEBAPP.EMAIL_PROPERTY] == guest_user.email
        assert response_data_list[api_constants.MGMT_WEBAPP.FIRST_NAME_PROPERTY] == guest_user.first_name
        assert response_data_list[api_constants.MGMT_WEBAPP.LAST_NAME_PROPERTY] == guest_user.last_name
        assert response_data_list[api_constants.MGMT_WEBAPP.ID_PROPERTY] == guest_user.id
        assert response_data_list[api_constants.MGMT_WEBAPP.ORGANIZATION_PROPERTY] == guest_user.organization
        assert response_data_list[api_constants.MGMT_WEBAPP.PASSWORD_PROPERTY] == ""
        assert response_data_list[api_constants.MGMT_WEBAPP.SALT_PROPOERTY] == ""
        assert response_data_list[api_constants.MGMT_WEBAPP.USERNAME_PROPERTY] == guest_user.username
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
                                               f"{constants.COMMANDS.SLASH_DELIM}999")
        response_data = response.data.decode("utf-8")
        response_data = json.loads(response_data)
        assert response.status_code == constants.HTTPS.NOT_FOUND_STATUS_CODE
        assert response_data == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_edit_is_authorized", side_effect=unauthorized)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
                                               f"{constants.COMMANDS.SLASH_DELIM}{admin_user.id}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert len(response_data_list) == 0
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE

    def test_users_id_put(self, flask_app, mocker: pytest_mock.MockFixture, management_users, not_logged_in,
                          logged_in, authorized, unauthorized, management_config, update) -> None:
        """
        Testing the PUT HTTPS method for the /users/id resource

        :param flask_app: the flask app representing the web server
        :param mocker: the mocker object for mocking functions
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param management_users: the management_users fixture
        :param not_logged_in: the not_logged_in fixture
        :param management_config: the management_config fixture
        :param remove: the remove fixture
        :param logged_in: the logged_in fixture
        :param authorized: the athourized fixture
        :param unauthorized: the unauthorized fixture
        :param update: the update fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.update_management_user",
                     side_effect=update)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_management_users",
                     side_effect=management_users)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_management_user_config",
                     side_effect=management_config)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_edit_is_authorized", side_effect=authorized)
        guest_user = TestResourcesUsersSuite.example_guest_user()
        guest_data_test = guest_user.to_dict()
        response = flask_app.test_client().put(f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
                                               f"{constants.COMMANDS.SLASH_DELIM}{guest_user.id}",
                                               data=json.dumps(guest_data_test))
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert len(response_data_list) == 9
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        bad_guest_data_test = guest_user.to_dict()
        del bad_guest_data_test[api_constants.MGMT_WEBAPP.USERNAME_PROPERTY]
        response = flask_app.test_client().put(f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
                                               f"{constants.COMMANDS.SLASH_DELIM}{guest_user.id}",
                                               data=json.dumps(bad_guest_data_test))
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert len(response_data_list) < 9
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_edit_is_authorized", side_effect=unauthorized)
        response = flask_app.test_client().put(f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
                                               f"{constants.COMMANDS.SLASH_DELIM}{guest_user.id}",
                                               data=json.dumps(guest_data_test))
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert len(response_data_list) == 0
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE

    def test_users_id_delete(self, flask_app, mocker: pytest_mock.MockFixture, management_users, not_logged_in,
                             remove, logged_in, authorized, unauthorized, management_config) -> None:
        """
        Testing the DELETE HTTPS method for the /users/id resource

        :param flask_app: the flask app representing the web server
        :param mocker: the mocker object for mocking functions
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param management_users: the management_users fixture
        :param not_logged_in: the not_logged_in fixture
        :param management_config: the management_config fixture
        :param remove: the remove fixture
        :param logged_in: the logged_in fixture
        :param authorized: the athourized fixture
        :param unauthorized: the unathourized fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_management_users",
                     side_effect=management_users)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_management_user_config",
                     side_effect=management_config)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_edit_is_authorized", side_effect=authorized)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_management_user",
                     side_effect=remove)
        guest_user = TestResourcesUsersSuite.example_guest_user()
        admin_user = TestResourcesUsersSuite.example_admin_user()
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
                                                  f"{constants.COMMANDS.SLASH_DELIM}{guest_user.id}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
                                                  f"{constants.COMMANDS.SLASH_DELIM}{admin_user.id}")
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_edit_is_authorized", side_effect=unauthorized)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
                                                  f"{constants.COMMANDS.SLASH_DELIM}{guest_user.id}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
                                                  f"{constants.COMMANDS.SLASH_DELIM}{admin_user.id}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}

    def test_create(self, flask_app, mocker: pytest_mock.MockFixture, save, management_users) -> None:
        """
        Testing the POST HTTPS method for the /users/id resource

        :param flask_app: the flask app representing the web server
        :param mocker: the mocker object for mocking functions
        :param management_users: the management_users fixture
        :param save: the save fixture
        :return: None
        """
        guest_user = TestResourcesUsersSuite.example_guest_user()
        admin_user = TestResourcesUsersSuite.example_admin_user()
        c_node = ClusterNode(ip="12.345.67.89", leader=True, cpus=1, gpus=2, RAM=3)
        constants.CONFIG_FILE.PARSED_CONFIG = Config(
            management_admin_username_default="null",
            management_admin_password_default="null",
            management_admin_first_name_default="null",
            management_admin_last_name_default="null",
            management_admin_email_default="null",
            management_admin_organization_default="null",
            management_guest_username_default="null",
            management_guest_password_default="null",
            management_guest_first_name_default="null",
            management_guest_last_name_default="null",
            management_guest_email_default="null",
            management_guest_organization_default="null",
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
            version="0.8.0",
            localhost=False,
            recovery_ai=False,
            recovery_ai_output_dir="",
            recovery_ai_examples_path=""
        )
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_management_users",
                     side_effect=management_users)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.save_management_user", side_effect=save)
        bad_guest_user_1 = ManagementUser.from_dict(guest_user.to_dict())
        bad_guest_user_1.password = ""
        bad_guest_data_test_1 = bad_guest_user_1.to_dict()
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
                                                f"{constants.COMMANDS.SLASH_DELIM}"
                                                f"{api_constants.MGMT_WEBAPP.CREATE_SUBRESOURCE}",
                                                data=json.dumps(bad_guest_data_test_1))
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        bad_guest_user_2 = ManagementUser.from_dict(guest_user.to_dict())
        bad_guest_user_2.username = ""
        bad_guest_data_test_2 = bad_guest_user_2.to_dict()
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
                                                f"{constants.COMMANDS.SLASH_DELIM}"
                                                f"{api_constants.MGMT_WEBAPP.CREATE_SUBRESOURCE}",
                                                data=json.dumps(bad_guest_data_test_2))
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        create_user = ManagementUser(username="jdoe", password="jdoe", email="jdoe@CSLE.com", admin=False,
                                     first_name="John", last_name="Doe", organization="CSLE", salt="123")
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
                                                f"{constants.COMMANDS.SLASH_DELIM}"
                                                f"{api_constants.MGMT_WEBAPP.CREATE_SUBRESOURCE}",
                                                data=json.dumps(create_user.to_dict()))
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list[api_constants.MGMT_WEBAPP.ADMIN_PROPERTY] is create_user.admin
        assert response_data_list[api_constants.MGMT_WEBAPP.EMAIL_PROPERTY] == create_user.email
        assert response_data_list[api_constants.MGMT_WEBAPP.FIRST_NAME_PROPERTY] == create_user.first_name
        assert response_data_list[api_constants.MGMT_WEBAPP.LAST_NAME_PROPERTY] == create_user.last_name
        assert response_data_list[api_constants.MGMT_WEBAPP.ID_PROPERTY] == -1
        assert response_data_list[api_constants.MGMT_WEBAPP.ORGANIZATION_PROPERTY] == create_user.organization
        assert response_data_list[api_constants.MGMT_WEBAPP.USERNAME_PROPERTY] == create_user.username
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
                                                f"{constants.COMMANDS.SLASH_DELIM}"
                                                f"{api_constants.MGMT_WEBAPP.CREATE_SUBRESOURCE}",
                                                data=json.dumps({}))
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
                                                f"{constants.COMMANDS.SLASH_DELIM}"
                                                f"{api_constants.MGMT_WEBAPP.CREATE_SUBRESOURCE}",
                                                data=json.dumps(admin_user.to_dict()))
        assert response.status_code == constants.HTTPS.CONFLICT_STATUS_CODE
        constants.CONFIG_FILE.PARSED_CONFIG = None
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
                                                f"{constants.COMMANDS.SLASH_DELIM}"
                                                f"{api_constants.MGMT_WEBAPP.CREATE_SUBRESOURCE}",
                                                data=json.dumps(admin_user.to_dict()))
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
