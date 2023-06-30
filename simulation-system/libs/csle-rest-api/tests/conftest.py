
import csle_common.constants.constants as constants
import pytest
from csle_common.dao.management.management_user import ManagementUser
from flask import jsonify

import csle_rest_api.constants.constants as api_constants


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
