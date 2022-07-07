"""
Routes and sub-resources for the /multi-threshold-policies resource
"""
from flask import Blueprint, jsonify, request
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_common.metastore.metastore_facade import MetastoreFacade


# Creates a blueprint "sub application" of the main REST app
multi_threshold_policies_bp = Blueprint(
    api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE}")


@multi_threshold_policies_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                        api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def multi_threshold_policies():
    """
    The /multi-threshold-policies resource.

    :return: A list of multi-threshold-policies or a list of ids of the policies or deletes the policies
    """

    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
        # Check if ids query parameter is True, then only return the ids and not the whole dataset
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return multi_threshold_policies_ids()

        multi_threshold_stopping_policies = MetastoreFacade.list_multi_threshold_stopping_policies()
        multi_threshold_stopping_policies_dicts = list(map(lambda x: x.to_dict(), multi_threshold_stopping_policies))
        response = jsonify(multi_threshold_stopping_policies_dicts)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response
    elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        policies = MetastoreFacade.list_multi_threshold_stopping_policies()
        for policy in policies:
            MetastoreFacade.remove_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response


def multi_threshold_policies_ids():
    """
    :return: An HTTP response with all multi theshold policies ids
    """
    multi_threshold_stopping_policies_ids = MetastoreFacade.list_multi_threshold_stopping_policies_ids()
    response_dicts = []
    for tup in multi_threshold_stopping_policies_ids:
        response_dicts.append({
            api_constants.MGMT_WEBAPP.ID_PROPERTY: tup[0],
            api_constants.MGMT_WEBAPP.SIMULATION_PROPERTY: tup[1]
        })
    response = jsonify(response_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response


@multi_threshold_policies_bp.route("/<policy_id>", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                                   api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def multi_threshold_policy(policy_id: int):
    """
    The /multi-threshold-policies/id resource.

    :param policy_id: the id of the policy

    :return: The given policy or deletes the policy
    """
    policy = MetastoreFacade.get_multi_threshold_stopping_policy(id=policy_id)
    response = jsonify({})
    if policy is not None:
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            response = jsonify(policy.to_dict())
        else:
            MetastoreFacade.remove_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response

