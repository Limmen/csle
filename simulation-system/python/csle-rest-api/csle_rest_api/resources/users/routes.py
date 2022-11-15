"""
Routes and sub-resources for the /users resource
"""
from flask import Blueprint, jsonify, request
import json
import bcrypt
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_common.metastore.metastore_facade import MetastoreFacade
import csle_rest_api.util.rest_api_util as rest_api_util
from csle_common.dao.management.management_user import ManagementUser


# Creates a blueprint "sub application" of the main REST app
users_bp = Blueprint(
    api_constants.MGMT_WEBAPP.USERS_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.USERS_RESOURCE}")


@users_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                             api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def users():
    """
    The /users resource.

    :return: A list of management users or a list of ids of the users or deletes all users
    """
    requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
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
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        users = MetastoreFacade.list_management_users()
        for user in users:
            MetastoreFacade.remove_management_user(management_user=user)
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE


def users_ids():
    """
    :return: An HTTP response with all user ids
    """
    user_ids = MetastoreFacade.list_management_users_ids()
    response_dicts = []
    for tup in user_ids:
        response_dicts.append({
            api_constants.MGMT_WEBAPP.ID_PROPERTY: tup[0]
        })
    response = jsonify(response_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@users_bp.route("/<user_id>", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                       api_constants.MGMT_WEBAPP.HTTP_REST_DELETE,
                                       api_constants.MGMT_WEBAPP.HTTP_REST_PUT])
def user(user_id: int):
    """
    The /users/id resource.

    :param user_id: the id of the user

    :return: The given user or deletes the user
    """
    requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    user = MetastoreFacade.get_management_user_config(id=user_id)
    response = jsonify({})
    if user is not None:
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            response = jsonify(user.to_dict())
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_PUT:
            new_user = json.loads(request.data)[api_constants.MGMT_WEBAPP.USER_PROPERTY]
            new_user = ManagementUser.from_dict(new_user)
            if new_user.password == "":
                new_user.password = user.password
                new_user.salt = user.salt
            else:
                byte_pwd = user.password.encode('utf-8')
                salt = bcrypt.gensalt()
                pw_hash = bcrypt.hashpw(byte_pwd, salt)
                new_user.salt = salt.decode("utf-8")
                new_user.password = pw_hash.decode("utf-8")
            MetastoreFacade.update_management_user(management_user=new_user, id=user_id)
            new_user.salt = ""
            new_user.password = ""
            response = jsonify(user.to_dict())
        else:
            MetastoreFacade.remove_management_user(management_user=user)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@users_bp.route("/create", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def create_user():
    """
    The /users/create resource.

    :return: creates a new user
    """
    response = jsonify({})
    if request.data is not None and api_constants.MGMT_WEBAPP.USERNAME_PROPERTY in json.loads(request.data) \
            and api_constants.MGMT_WEBAPP.PASSWORD_PROPERTY in json.loads(request.data):
        username = json.loads(request.data)[api_constants.MGMT_WEBAPP.USERNAME_PROPERTY]
        password = json.loads(request.data)[api_constants.MGMT_WEBAPP.PASSWORD_PROPERTY]
        if password == "" or username == "":
            return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
        else:
            byte_pwd = password.encode('utf-8')
            salt = bcrypt.gensalt()
            pw_hash = bcrypt.hashpw(byte_pwd, salt)
            user = ManagementUser(username=username,
                                  password=pw_hash.decode("utf-8"), admin=False,
                                  salt=salt.decode("utf-8"))
            MetastoreFacade.save_management_user(management_user=user)
            response = jsonify(user.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
