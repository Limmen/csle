"""
Routes and sub-resources for the /vector-policies resource
"""
from typing import Tuple
import csle_common.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from flask import Blueprint, jsonify, request, Response
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util

# Creates a blueprint "sub application" of the main REST app
vector_policies_bp = Blueprint(
    api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE}")


@vector_policies_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                       api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def vector_policies() -> Tuple[Response, int]:
    """
    The /vector-policies resource.

    :return: A list of vector-policies or a list of ids of the policies or deletes the policies
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
        # Check if ids query parameter is True, then only return the ids and not the whole list of vector policies
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return vector_policies_ids()
        vector_policies = MetastoreFacade.list_vector_policies()
        vector_policies_dicts = list(map(lambda x: x.to_dict(), vector_policies))
        response = jsonify(vector_policies_dicts)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        policies = MetastoreFacade.list_vector_policies()
        for policy in policies:
            MetastoreFacade.remove_vector_policy(vector_policy=policy)
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: "HTTP method not supported"}),
            constants.HTTPS.BAD_REQUEST_STATUS_CODE)


def vector_policies_ids() -> Tuple[Response, int]:
    """
    :return: An HTTP response with all vector policies ids
    """
    vector_policies_ids = MetastoreFacade.list_vector_policies_ids()
    response_dicts = []
    for tup in vector_policies_ids:
        response_dicts.append({
            api_constants.MGMT_WEBAPP.ID_PROPERTY: tup[0],
            api_constants.MGMT_WEBAPP.SIMULATION_PROPERTY: tup[1]
        })
    response = jsonify(response_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@vector_policies_bp.route("/<policy_id>", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                                   api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def vector_policy(policy_id: int) -> Tuple[Response, int]:
    """
    The /vector-policies/id resource.

    :param policy_id: the id of the policy

    :return: The given policy or deletes the policy
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    policy = MetastoreFacade.get_vector_policy(id=policy_id)
    response = jsonify({})
    if policy is not None:
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            response = jsonify(policy.to_dict())
        else:
            MetastoreFacade.remove_vector_policy(vector_policy=policy)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
