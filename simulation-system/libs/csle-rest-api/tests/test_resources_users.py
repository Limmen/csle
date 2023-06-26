from typing import Tuple, List, Union
import json
import logging
import csle_common.constants.constants as constants
import pytest
from flask import jsonify
from csle_common.dao.management.management_user import ManagementUser
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
                response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
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
        def update_management_user(management_user: ManagementUser, id : int) -> None:
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
        def check_if_user_edit_is_authorized(request, requires_admin: bool = False):
            token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
            if token != "":
                return None
            response = jsonify({})
            response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
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
                response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
                return response, constants.HTTPS.UNAUTHORIZED_STATUS_CODE
            return user

        check_if_user_edit_is_authorized_mock = mocker.MagicMock(
            side_effect=check_if_user_edit_is_authorized
        )
        return check_if_user_edit_is_authorized_mock

    def test_users(self, flask_app, mocker, logged_in_as_admin, management_users, not_logged_in, management_ids,
                   remove, logged_in) -> None:
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
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
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
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.USERS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}


