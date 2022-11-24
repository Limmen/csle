"""
Routes and sub-resources for the /emulation-statistics resource
"""
from flask import Blueprint, jsonify, request
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_common.metastore.metastore_facade import MetastoreFacade
import csle_rest_api.util.rest_api_util as rest_api_util

# Creates a blueprint "sub application" of the main REST app
emulation_statistics_bp = Blueprint(
    api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}")


@emulation_statistics_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                            api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def emulation_statistics():
    """
    The /emulation-statistics resource.

    :return: A list of emulation statistics or a list of ids of the statistics or deletes the statistics
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
        # Check if ids query parameter is True, then only return the ids and not the whole list of emulation statistics
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return emulation_statistics_ids()

        stats = MetastoreFacade.list_emulation_statistics()
        stats_dicts = list(map(lambda x: x.to_dict(), stats))
        response = jsonify(stats_dicts)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        statistics = MetastoreFacade.list_emulation_statistics()
        for stat in statistics:
            MetastoreFacade.remove_emulation_statistic(stat)
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE


def emulation_statistics_ids():
    """
    :return: An HTTP response with all emulation statistics ids
    """
    stats_ids = MetastoreFacade.list_emulation_statistics_ids()
    response_dicts = []
    for tup in stats_ids:
        response_dicts.append({
            api_constants.MGMT_WEBAPP.ID_PROPERTY: tup[0],
            api_constants.MGMT_WEBAPP.EMULATION_PROPERTY: tup[1]
        })
    response = jsonify(response_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@emulation_statistics_bp.route("/<statistics_id>", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                                            api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def emulation_statistic(statistics_id: int):
    """
    The /emulation-statistics/id resource.

    :param statistics_id: the id of the statistic

    :return: The given statistic or deletes the statistic
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    statistic = MetastoreFacade.get_emulation_statistic(id=statistics_id)
    response = jsonify({})
    if statistic is not None:
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            response = jsonify(statistic.to_dict())
        else:
            MetastoreFacade.remove_emulation_statistic(statistic)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
