"""
Routes and sub-resources for the /users resource
"""
from typing import Tuple
import json
import bcrypt
import csle_common.constants.constants as constants
from csle_common.dao.management.management_user import ManagementUser
from csle_common.metastore.metastore_facade import MetastoreFacade
from flask import Blueprint, jsonify, request, Response
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util

# Creates a blueprint "sub application" of the main REST app
users_bp = Blueprint(api_constants.MGMT_WEBAPP.USERS_RESOURCE, __name__,
                     url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.USERS_RESOURCE}")


@users_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def users() -> Tuple[Response, int]:
    """
    The /users resource.

    :return: A list of management users or a list of ids of the users or deletes all users
    """
    requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(
        request=request, requires_admin=requires_admin
    )
    if authorized is not None:
        return authorized

    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
        # Check if ids query parameter is True, then only return the ids and not the whole list of users
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return users_ids()
        users = MetastoreFacade.list_management_users()
        for i in range(len(users)):
            users[i].password = ""
            users[i].salt = ""
        users_dicts = list(map(lambda x: x.to_dict(), users))

        response = jsonify(users_dicts)
        response.headers.add(
            api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*"
        )
        return response, constants.HTTPS.OK_STATUS_CODE
    elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        users = MetastoreFacade.list_management_users()
        for user in users:
            MetastoreFacade.remove_management_user(management_user=user)
        response = jsonify({})
        response.headers.add(
            api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*"
        )
        return response, constants.HTTPS.OK_STATUS_CODE
    return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: "HTTP method not supported"}),
            constants.HTTPS.BAD_REQUEST_STATUS_CODE)


def users_ids() -> Tuple[Response, int]:
    """
    Gets the user ids

    :return: An HTTP response with all user ids
    """
    user_ids = MetastoreFacade.list_management_users_ids()
    response_dicts = []
    for tup in user_ids:
        response_dicts.append({api_constants.MGMT_WEBAPP.ID_PROPERTY: tup[0]})
    response = jsonify(response_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@users_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<user_id>", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                                                       api_constants.MGMT_WEBAPP.HTTP_REST_DELETE,
                                                                       api_constants.MGMT_WEBAPP.HTTP_REST_PUT])
def user(user_id: int) -> Tuple[Response, int]:
    """
    The /users/id resource.

    :param user_id: the id of the user
    :return: The given user or deletes the user
    """

    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=False)

    if authorized is not None:
        return authorized
    # Check if user is admin or is editing his/hers own account
    user = MetastoreFacade.get_management_user_config(id=int(user_id))

    if user is None:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.NOT_FOUND_STATUS_CODE

    request_user = rest_api_util.check_if_user_edit_is_authorized(request=request, user=user)
    if not isinstance(request_user, ManagementUser):
        if request_user is not None:
            return request_user
        else:
            return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: f"User: {user} not found"}),
                    constants.HTTPS.BAD_REQUEST_STATUS_CODE)

    response = jsonify({})

    if user is not None:
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            user.password = ""
            user.salt = ""
            response = jsonify(user.to_dict())
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_PUT:
            new_user = json.loads(request.data)
            if not (
                    api_constants.MGMT_WEBAPP.USERNAME_PROPERTY in new_user
                    and api_constants.MGMT_WEBAPP.PASSWORD_PROPERTY in new_user
                    and api_constants.MGMT_WEBAPP.FIRST_NAME_PROPERTY in new_user
                    and api_constants.MGMT_WEBAPP.LAST_NAME_PROPERTY in new_user
                    and api_constants.MGMT_WEBAPP.ORGANIZATION_PROPERTY in new_user
                    and api_constants.MGMT_WEBAPP.ID_PROPERTY in new_user
                    and api_constants.MGMT_WEBAPP.EMAIL_PROPERTY in new_user
                    and api_constants.MGMT_WEBAPP.ADMIN_PROPERTY in new_user
            ):
                if api_constants.MGMT_WEBAPP.PASSWORD_PROPERTY in new_user:
                    new_user[api_constants.MGMT_WEBAPP.PASSWORD_PROPERTY] = ""
                if api_constants.MGMT_WEBAPP.SALT_PROPOERTY in new_user:
                    new_user[api_constants.MGMT_WEBAPP.SALT_PROPOERTY] = ""
                response = jsonify(new_user)
                return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE

            new_user = ManagementUser.from_dict(new_user)
            if new_user.password == "":
                new_user.password = user.password
                new_user.salt = user.salt
            else:
                byte_pwd = new_user.password.encode("utf-8")
                salt = bcrypt.gensalt()
                pw_hash = bcrypt.hashpw(byte_pwd, salt)
                new_user.salt = salt.decode("utf-8")
                new_user.password = pw_hash.decode("utf-8")

            # A user cannot be given admin rights by a non-admin user
            if not request_user.admin:
                new_user.admin = False

            # An admin user cannot remove its own admin rights
            if request_user.admin and user.admin and request_user.username == user.username:
                new_user.admin = True
            MetastoreFacade.update_management_user(management_user=new_user, id=user_id)
            new_user.salt = ""
            new_user.password = ""
            user.salt = ""
            user.password = ""
            response = jsonify(user.to_dict())
        else:
            MetastoreFacade.remove_management_user(management_user=user)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@users_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.CREATE_SUBRESOURCE}",
                methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def create_user() -> Tuple[Response, int]:
    """
    The /users/create resource.

    :return: creates a new user
    """
    response = jsonify({})
    if constants.CONFIG_FILE.PARSED_CONFIG is not None and constants.CONFIG_FILE.PARSED_CONFIG.allow_registration:
        json_data = json.loads(request.data)
        if (api_constants.MGMT_WEBAPP.USERNAME_PROPERTY in json_data
                and api_constants.MGMT_WEBAPP.PASSWORD_PROPERTY in json_data
                and api_constants.MGMT_WEBAPP.FIRST_NAME_PROPERTY in json_data
                and api_constants.MGMT_WEBAPP.LAST_NAME_PROPERTY in json_data
                and api_constants.MGMT_WEBAPP.EMAIL_PROPERTY in json_data
                and api_constants.MGMT_WEBAPP.ORGANIZATION_PROPERTY in json_data
                and api_constants.MGMT_WEBAPP.ADMIN_PROPERTY in json_data):
            username = json_data[api_constants.MGMT_WEBAPP.USERNAME_PROPERTY]
            password = json_data[api_constants.MGMT_WEBAPP.PASSWORD_PROPERTY]
            first_name = json_data[api_constants.MGMT_WEBAPP.FIRST_NAME_PROPERTY]
            last_name = json_data[api_constants.MGMT_WEBAPP.LAST_NAME_PROPERTY]
            organization = json_data[
                api_constants.MGMT_WEBAPP.ORGANIZATION_PROPERTY
            ]
            email = json_data[api_constants.MGMT_WEBAPP.EMAIL_PROPERTY]
            if password == "" or username == "":
                error_reason = "Password or username cannot be empty."
                response = jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: error_reason})
                return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
            else:
                usernames = list(map(lambda x: x.username, MetastoreFacade.list_management_users()))
                if username in usernames:
                    error_reason = "A user with that username already exists"
                    response = jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: error_reason})
                    return response, constants.HTTPS.CONFLICT_STATUS_CODE
                byte_pwd = password.encode("utf-8")
                salt = bcrypt.gensalt()
                pw_hash = bcrypt.hashpw(byte_pwd, salt)
                user = ManagementUser(username=username, password=pw_hash.decode("utf-8"), admin=False,
                                      salt=salt.decode("utf-8"), first_name=first_name, last_name=last_name,
                                      organization=organization, email=email)
                MetastoreFacade.save_management_user(management_user=user)
                user.salt = ""
                user.password = ""
                response = jsonify(user.to_dict())
            response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
            return response, constants.HTTPS.OK_STATUS_CODE
        else:
            return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
    else:
        return response, constants.HTTPS.UNAUTHORIZED_STATUS_CODE
