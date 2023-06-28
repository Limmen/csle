import json
import logging
from typing import List, Tuple, Union

import csle_common.constants.constants as constants
import pytest
from csle_common.dao.emulation_config.cluster_config import ClusterConfig
from csle_common.dao.emulation_config.cluster_node import ClusterNode
from csle_common.dao.emulation_config.config import Config
from csle_common.dao.management.management_user import ManagementUser
from flask import jsonify

import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesUsersSuite(object):
    """
    Test suite for /users resource
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
            return [], constants.HTTPS.UNAUTHORIZED_STATUS_CODE

        check_if_user_is_authorized_mock = mocker.MagicMock(
            side_effect=check_if_user_is_authorized
        )
        return check_if_user_is_authorized_mock

    @pytest.fixture
    def management_users(self, mocker):
        """
        Fixture for mocking the list of management users in the database

        :param mocker: the pytest mocker object
        :return: fixture for mocking the users in the database
        """

        def list_management_users() -> List[ManagementUser]:
            users = [
                ManagementUser(
                    username="admin",
                    password="admin",
                    email="admin@CSLE.com",
                    admin=True,
                    first_name="Admin",
                    last_name="Adminson",
                    organization="CSLE",
                    salt="123",
                ),
                ManagementUser(
                    username="guest",
                    password="guest",
                    email="guest@CSLE.com",
                    admin=False,
                    first_name="Guest",
                    last_name="Guestson",
                    organization="CSLE",
                    salt="123",
                ),
            ]
            return users

        list_management_users_mock = mocker.MagicMock(side_effect=list_management_users)
        return list_management_users_mock

    @pytest.fixture
    def management_ids(self, mocker):
        """
        Fixture for mocking the management user ids

        :param mocker: the pytest mocker object
        :return: fixture for mocking the management user ids
        """

        def list_management_users_ids() -> List[Tuple]:
            return [(1,), (2,)]

        list_management_users_ids_mock = mocker.MagicMock(
            side_effect=list_management_users_ids
        )
        return list_management_users_ids_mock

    @pytest.fixture
    def management_config(self, mocker):
        """
        Fixture for mocking the get_management_user_config function of the MetastoreFacade

        :param mocker: the pytest mocker object
        :return: fixture for mocking the get_management_user_config function of the MetastoreFacade
        """

        def get_management_user_config(id: int) -> Union[None, ManagementUser]:
            admin_user = ManagementUser(
                username="admin",
                password="admin",
                email="admin@CSLE.com",
                admin=True,
                first_name="Admin",
                last_name="Adminson",
                organization="CSLE",
                salt="123",
            )
            admin_user.id = 11
            guest_user = ManagementUser(
                username="guest",
                password="guest",
                email="guest@CSLE.com",
                admin=False,
                first_name="Guest",
                last_name="Guestson",
                organization="CSLE",
                salt="123",
            )
            guest_user.id = 235
            if id == 11:
                return admin_user
            elif id == 235:
                return guest_user
            else:
                return None

        get_management_user_config_mock = mocker.MagicMock(
            side_effect=get_management_user_config
        )
        return get_management_user_config_mock

    @pytest.fixture
    def update(self, mocker):
        """
        Fixture for mocking the update_management_user of the MetastoreFacade

        :param mocker: the pytest mocker object
        :return: fixture for mocking the update_management_user of the MetastoreFacade
        """

        def update_management_user(management_user: ManagementUser, id: int) -> None:
            return None

        update_management_user_mock = mocker.MagicMock(
            side_effect=update_management_user
        )
        return update_management_user_mock

    @pytest.fixture
    def remove(self, mocker):
        """
        Fixture for mocking the remove_management_user function of the Metastore

        :param mocker: the pytest mocker object
        :return: fixture for mocking the remove_management_user function of the Metastore
        """

        def remove_management_user(management_user: ManagementUser):
            return None

        remove_management_user_mock = mocker.MagicMock(
            side_effect=remove_management_user
        )
        return remove_management_user_mock

    @pytest.fixture
    def save(self, mocker):
        """
        Fixture for mocking the save_management_user function in the MetastoreFacade

        :param mocker: the pytest mocker object
        :return: fixture for mocking the save_management_user function in the MetastoreFacade
        """

        def save_management_user(management_user: ManagementUser) -> int:
            return 1

        save_management_user_mock = mocker.MagicMock(side_effect=save_management_user)
        return save_management_user_mock

    @pytest.fixture
    def authorized(self, mocker):
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
    def unauthorized(self, mocker):
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

    def test_users(
            self,
            flask_app,
            mocker,
            logged_in_as_admin,
            management_users,
            not_logged_in,
            management_ids,
            remove,
            logged_in,
    ) -> None:
        """
        Tests the /users resource for listing management user accounts

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
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.list_management_users",
            side_effect=management_users,
        )
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.USERS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert len(response_data_list) == 2
        users = list(map(lambda x: ManagementUser.from_dict(x), response_data_list))
        assert users[0].username == "admin"
        assert users[0].password == ""
        assert users[0].email == "admin@CSLE.com"
        assert users[0].admin is True
        assert users[0].first_name == "Admin"
        assert users[0].last_name == "Adminson"
        assert users[0].salt == ""
        assert users[0].organization == "CSLE"
        assert users[1].username == "guest"
        assert users[1].password == ""
        assert users[1].email == "guest@CSLE.com"
        assert users[1].admin is False
        assert users[1].first_name == "Guest"
        assert users[1].last_name == "Guestson"
        assert users[1].salt == ""
        assert users[1].organization == "CSLE"
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.list_management_users_ids",
            side_effect=management_ids,
        )
        response = flask_app.test_client().get(
            f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
            f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert len(response_data_list) == 2
        assert response_data_list[0][api_constants.MGMT_WEBAPP.ID_PROPERTY] == 1
        assert response_data_list[1][api_constants.MGMT_WEBAPP.ID_PROPERTY] == 2
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.USERS_RESOURCE)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert len(response_data_list) == 0
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.USERS_RESOURCE)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert len(response_data_list) == 0
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.remove_management_user",
            side_effect=remove,
        )
        response = flask_app.test_client().delete(
            api_constants.MGMT_WEBAPP.USERS_RESOURCE
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}

    def test_users_id(
            self,
            flask_app,
            mocker,
            management_users,
            not_logged_in,
            remove,
            logged_in,
            authorized,
            unauthorized,
            management_config,
    ) -> None:
        """
        Testing the /users/id
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
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.list_management_users",
            side_effect=management_users,
        )
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.get_management_user_config",
            side_effect=management_config,
        )
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_edit_is_authorized",
            side_effect=authorized,
        )
        response = flask_app.test_client().get(
            f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
            f"{constants.COMMANDS.SLASH_DELIM}11"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert len(response_data_list) == 9
        assert response_data_list["admin"] is True
        assert response_data_list["email"] == "admin@CSLE.com"
        assert response_data_list["first_name"] == "Admin"
        assert response_data_list["last_name"] == "Adminson"
        assert response_data_list["id"] == 11
        assert response_data_list["organization"] == "CSLE"
        assert response_data_list["password"] == "admin"
        assert response_data_list["salt"] == "123"
        assert response_data_list["username"] == "admin"
        response = flask_app.test_client().get(
            f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
            f"{constants.COMMANDS.SLASH_DELIM}235"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert len(response_data_list) == 9
        assert response_data_list["admin"] is False
        assert response_data_list["email"] == "guest@CSLE.com"
        assert response_data_list["first_name"] == "Guest"
        assert response_data_list["last_name"] == "Guestson"
        assert response_data_list["id"] == 235
        assert response_data_list["organization"] == "CSLE"
        assert response_data_list["password"] == "guest"
        assert response_data_list["salt"] == "123"
        assert response_data_list["username"] == "guest"
        response = flask_app.test_client().get(
            f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
            f"{constants.COMMANDS.SLASH_DELIM}999"
        )
        response_data = response.data.decode("utf-8")
        response_data = json.loads(response_data)
        assert response.status_code == constants.HTTPS.NOT_FOUND_STATUS_CODE
        assert response_data == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_edit_is_authorized",
            side_effect=unauthorized,
        )

        response = flask_app.test_client().get(
            f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
            f"{constants.COMMANDS.SLASH_DELIM}11"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert len(response_data_list) == 0
        assert response_data_list == []
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE

        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )

        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_edit_is_authorized",
            side_effect=authorized,
        )
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.remove_management_user",
            side_effect=remove,
        )
        response = flask_app.test_client().delete(
            f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
            f"{constants.COMMANDS.SLASH_DELIM}235"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}
        response = flask_app.test_client().delete(
            f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
            f"{constants.COMMANDS.SLASH_DELIM}11"
        )
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )

        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_edit_is_authorized",
            side_effect=unauthorized,
        )
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.remove_management_user",
            side_effect=remove,
        )
        response = flask_app.test_client().delete(
            f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
            f"{constants.COMMANDS.SLASH_DELIM}235"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == []
        response = flask_app.test_client().delete(
            f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
            f"{constants.COMMANDS.SLASH_DELIM}11"
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == []
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_edit_is_authorized",
            side_effect=authorized,
        )
        guest_user = ManagementUser(
            username="guest",
            password="guest",
            email="guest@CSLE.com",
            admin=False,
            first_name="Guest",
            last_name="Guestson",
            organization="CSLE",
            salt="123",
        )
        guest_data_test = guest_user.to_dict()
        response = flask_app.test_client().put(
            f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
            f"{constants.COMMANDS.SLASH_DELIM}235",
            data=json.dumps(guest_data_test),
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)

        assert len(response_data_list) == 9
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE

        bad_guest_user = ManagementUser(
            username="blablaba",
            password="guest",
            email="guest@CSLE.com",
            admin=False,
            first_name="Guest",
            last_name="Guestson",
            organization="CSLE",
            salt="123",
        )
        bad_guest_data_test = bad_guest_user.to_dict()
        del bad_guest_data_test[api_constants.MGMT_WEBAPP.USERNAME_PROPERTY]

        response = flask_app.test_client().put(
            f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
            f"{constants.COMMANDS.SLASH_DELIM}235",
            data=json.dumps(bad_guest_data_test),
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)

        assert len(response_data_list) < 9
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE

    def test_create(
            self,
            flask_app,
            mocker,
            save,
            management_users,
    ):
        """
        Testing the /users/id
        :param flask_app: the flask app representing the web server
        :param mocker: the mocker object for mocking functions

        :param management_users: the management_users fixture
        :param save: the save fixture
        :return: None
        """
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
        )
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.list_management_users",
            side_effect=management_users,
        )
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.save_management_user",
            side_effect=save,
        )
        bad_guest_user_1 = ManagementUser(
            username="guest",
            password="",
            email="guest@CSLE.com",
            admin=False,
            first_name="Guest",
            last_name="Guestson",
            organization="CSLE",
            salt="123",
        )
        bad_guest_data_test_1 = bad_guest_user_1.to_dict()
        response = flask_app.test_client().post(
            f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
            f"{constants.COMMANDS.SLASH_DELIM}"
            f"{api_constants.MGMT_WEBAPP.CREATE_SUBRESOURCE}",
            data=json.dumps(bad_guest_data_test_1),
        )
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        bad_guest_user_2 = ManagementUser(
            username="",
            password="guest",
            email="guest@CSLE.com",
            admin=False,
            first_name="Guest",
            last_name="Guestson",
            organization="CSLE",
            salt="123",
        )
        bad_guest_data_test_2 = bad_guest_user_2.to_dict()
        response = flask_app.test_client().post(
            f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
            f"{constants.COMMANDS.SLASH_DELIM}"
            f"{api_constants.MGMT_WEBAPP.CREATE_SUBRESOURCE}",
            data=json.dumps(bad_guest_data_test_2),
        )
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        guest_user = ManagementUser(
            username="jdoe",
            password="jdoe",
            email="jdoe@CSLE.com",
            admin=False,
            first_name="John",
            last_name="Doe",
            organization="CSLE",
            salt="123",
        )
        guest_data_test = guest_user.to_dict()
        response = flask_app.test_client().post(
            f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
            f"{constants.COMMANDS.SLASH_DELIM}"
            f"{api_constants.MGMT_WEBAPP.CREATE_SUBRESOURCE}",
            data=json.dumps(guest_data_test),
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list["admin"] is False
        assert response_data_list["email"] == "jdoe@CSLE.com"
        assert response_data_list["first_name"] == "John"
        assert response_data_list["last_name"] == "Doe"
        assert response_data_list["id"] == -1
        assert response_data_list["organization"] == "CSLE"
        assert response_data_list["username"] == "jdoe"
        response = flask_app.test_client().post(
            f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
            f"{constants.COMMANDS.SLASH_DELIM}"
            f"{api_constants.MGMT_WEBAPP.CREATE_SUBRESOURCE}",
            data=jsonify({}),
        )
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response_data = json.loads(response_data)
        assert response_data == {}
        guest_user = ManagementUser(
            username="admin",
            password="admin",
            email="admin@CSLE.com",
            admin=True,
            first_name="Admin",
            last_name="Adminson",
            organization="CSLE",
            salt="123",
        )
        guest_data_test = guest_user.to_dict()
        response = flask_app.test_client().post(
            f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
            f"{constants.COMMANDS.SLASH_DELIM}"
            f"{api_constants.MGMT_WEBAPP.CREATE_SUBRESOURCE}",
            data=json.dumps(guest_data_test),
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.CONFLICT_STATUS_CODE
        assert response_data_list == {
            "reason": "A user with that username already exists"
        }
        constants.CONFIG_FILE.PARSED_CONFIG = None
        response = flask_app.test_client().post(
            f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
            f"{constants.COMMANDS.SLASH_DELIM}"
            f"{api_constants.MGMT_WEBAPP.CREATE_SUBRESOURCE}",
            data=json.dumps(guest_data_test),
        )
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
