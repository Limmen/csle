import json
import logging

import csle_common.constants.constants as constants
import pytest
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
    def logged_in(self, mocker):
        """
        :param mocker: the pytest mocker object
        :return: the logged in fixture for mocking the logged in check
        """

        def check_if_user_is_authorized(request, requires_admin):
            return None

        check_if_user_is_authorized_mock = mocker.MagicMock(
            side_effect=check_if_user_is_authorized
        )
        # pytest.logger.info(check_if_user_is_authorized)
        return check_if_user_is_authorized_mock

    @pytest.fixture
    def not_logged_in(self, mocker):
        """
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
        :param mocker: the pytest mocker object
        :return: fixture for mocking the users in the database
        """

        def list_management_users():
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
        def list_management_users_ids():
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
            users[0].id = 1
            users[1].id = 2
            return [users[0].id, users[1].id]

        list_management_users_ids_mock = mocker.MagicMock(
            side_effect=list_management_users_ids
        )
        return list_management_users_ids_mock

    @pytest.fixture
    def management_config(self, mocker):
        def get_management_user_config(id):
            user = (
                ManagementUser(
                    username="jdoe",
                    password="jdoe",
                    email="jdoe@CSLE.com",
                    admin=True,
                    first_name="John",
                    last_name="Doe",
                    organization="CSLE",
                    salt="123",
                ),
            )
            user.id = 1
            return user

        get_management_user_config_mock = mocker.MagicMock(
            side_effect=get_management_user_config
        )
        return get_management_user_config_mock

    @pytest.fixture
    def update(self, mocker):
        def update_management_user(management_user, id):
            return True

        update_management_user_mock = mocker.MagicMock(
            side_effect=update_management_user
        )
        return update_management_user_mock

    @pytest.fixture
    def remove(self, mocker):
        def remove_management_user(management_user):
            return None

        remove_management_user_mock = mocker.MagicMock(
            side_effect=remove_management_user
        )
        return remove_management_user_mock

    @pytest.fixture
    def save(self, mocker):
        def save_management_user(management_user):
            return True

        save_management_user_mock = mocker.MagicMock(side_effect=save_management_user)

        return save_management_user_mock

    @pytest.fixture
    def authorized(self, mocker):
        def check_if_user_edit_is_authorized(request, user):
            return None

        check_if_user_edit_is_authorized_mock = mocker.MagicMock(
            side_effect=check_if_user_edit_is_authorized
        )

        return check_if_user_edit_is_authorized_mock

    @pytest.fixture
    def unauthorized(self, mocker):
        def check_if_user_edit_is_authorized(request, user):
            return [], constants.HTTPS.UNAUTHORIZED_STATUS_CODE

        check_if_user_edit_is_authorized_mock = mocker.MagicMock(
            side_effect=check_if_user_edit_is_authorized
        )
        return check_if_user_edit_is_authorized_mock

    def test_list_users(
        self, flask_app, mocker, logged_in, management_users, not_logged_in
    ) -> None:
        """
        Tests the /users resource for listing management user accounts

        :param flask_app: the flask app representing the web server
        :param mocker: the mocker object for mocking functions
        :param logged_in: the logged_in fixture
        :param management_users: the management_users fixture
        :param not_logged_in: the not_logged_in fixture
        :return: None
        """
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.list_management_users",
            side_effect=management_users,
        )
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.USERS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert len(response_data_list) == 2
        pytest.logger.info(response_data_list)
        users = list(map(lambda x: ManagementUser.from_dict(x), response_data_list))
        pytest.logger.info(users[0])
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
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.USERS_RESOURCE)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert len(response_data_list) == 0

    def test_list_user_ids(
        self,
        flask_app,
        mocker,
        logged_in,
        management_users,
        not_logged_in,
        management_ids,
    ) -> None:
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.list_management_users",
            side_effect=management_users,
        )
        mocker.patch(
            "csle_common.metastore.metastore_facade.MetastoreFacade.list_management_users_ids",
            side_effect=management_ids,
        )
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )

        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.USERS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        pytest.logger.info(response_data_list)
