"""
Routes and sub-resources for the /users resource
"""
from flask import Blueprint, jsonify, request
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_common.metastore.metastore_facade import MetastoreFacade
import csle_rest_api.util.rest_api_util as rest_api_util


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
        print(f"tup: {tup}")
        response_dicts.append({
            api_constants.MGMT_WEBAPP.ID_PROPERTY: tup[0]
        })
    response = jsonify(response_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@users_bp.route("/<user_id>", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                         api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
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
        else:
            MetastoreFacade.remove_management_user(management_user=user)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
