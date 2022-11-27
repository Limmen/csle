"""
Routes and sub-resources for the /emulation-traces resource
"""
from flask import Blueprint, jsonify, request
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_common.metastore.metastore_facade import MetastoreFacade
import csle_rest_api.util.rest_api_util as rest_api_util

# Creates a blueprint "sub application" of the main REST app
emulation_traces_bp = Blueprint(
    api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}")


@emulation_traces_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                        api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def emulation_traces():
    """
    The /emulation-traces resource.

    :return: A list of emulation traces or a list of ids of the traces or deletes the traces
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
        # Check if ids query parameter is True, then only return the ids and not the whole list of emulation traces
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return emulation_traces_ids()

        emulation_trcs = MetastoreFacade.list_emulation_traces()
        traces_dicts = list(map(lambda x: x.to_dict(), emulation_trcs))
        response = jsonify(traces_dicts)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        traces = MetastoreFacade.list_emulation_traces()
        for trace in traces:
            MetastoreFacade.remove_emulation_trace(trace)
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE


def emulation_traces_ids():
    """
    :return: An HTTP response with all emulation ids
    """
    ids_emulations = MetastoreFacade.list_emulation_traces_ids()
    response_dicts = []
    for tup in ids_emulations:
        response_dicts.append({
            api_constants.MGMT_WEBAPP.ID_PROPERTY: tup[0],
            api_constants.MGMT_WEBAPP.EMULATION_PROPERTY: tup[1]
        })
    response = jsonify(response_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@emulation_traces_bp.route("/<trace_id>", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                                   api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def emulation_trace(trace_id: int):
    """
    The /emulation-traces/id resource.

    :param trace_id: the id of the trace

    :return: The given trace or delets the trace
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    trace = MetastoreFacade.get_emulation_trace(id=trace_id)
    response = jsonify({})
    if trace is not None:
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            response = jsonify(trace.to_dict())
        else:
            MetastoreFacade.remove_emulation_trace(trace)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
