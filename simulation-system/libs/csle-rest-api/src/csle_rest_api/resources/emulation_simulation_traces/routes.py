"""
Routes and sub-resources for the /emulation-simulation-traces resource
"""
from typing import Tuple
from flask import Blueprint, jsonify, request, Response
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_common.metastore.metastore_facade import MetastoreFacade
import csle_rest_api.util.rest_api_util as rest_api_util

# Creates a blueprint "sub application" of the main REST app
emulation_simulation_traces_bp = Blueprint(
    api_constants.MGMT_WEBAPP.EMULATION_SIMULATION_TRACES_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.EMULATION_SIMULATION_TRACES_RESOURCE}")


@emulation_simulation_traces_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                                   api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def emulation_simulation_traces() -> Tuple[Response, int]:
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
        # Check if ids query parameter is True, then only return the ids and not the whole list of emulation-simulation
        # traces
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return emulation_simulation_traces_ids()
        demo_traces = [
            {
                "attacker_found_nodes": [[], [], [], [], [],
                                         ["n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9", "n10", "n11", ],
                                         ["n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9", "n10", "n11"],
                                         ["n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9", "n10", "n11", "n12",
                                          "switch1"],
                                         ["n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9", "n10", "n11", "n12",
                                          "switch1"],
                                         ["n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9", "n10", "n11", "n12",
                                          "switch1",
                                          "n13", "n14", "n15", "n16"],
                                         ["n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9", "n10", "n11", "n12",
                                          "switch1",
                                          "n13", "n14", "n15", "n16"],
                                         ["n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9", "n10", "n11", "n12",
                                          "switch1",
                                          "n13", "n14", "n15", "n16", "switch2", "n17", "n18"],
                                         ["n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9", "n10", "n11", "n12",
                                          "switch1",
                                          "n13", "n14", "n15", "n16", "switch2", "n17", "n18"],
                                         ["n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9", "n10", "n11", "n12",
                                          "switch1",
                                          "n13", "n14", "n15", "n16", "switch2", "n17", "n18", "switch3", "n19",
                                          "n20", "n21", "n22", "n23", "n24"],
                                         ["n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9", "n10", "n11", "n12",
                                          "switch1",
                                          "n13", "n14", "n15", "n16", "switch2", "n17", "n18", "switch3", "n19",
                                          "n20", "n21", "n22", "n23", "n24"],
                                         ["n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9", "n10", "n11", "n12",
                                          "switch1",
                                          "n13", "n14", "n15", "n16", "switch2", "n17", "n18", "switch3", "n19",
                                          "n20", "n21", "n22", "n23", "n24", "n25", "n26", "switch4"]],
                "attacker_compromised_nodes": [[], [], [], [], [], [],
                                               ["n2"], ["n2"], ["n2", "n12"], ["n2", "n12"], ["n2", "n12", "n4"],
                                               ["n2", "n12", "n4"], ["n2", "n12", "n4", "n17"],
                                               ["n2", "n12", "n4", "n17"], ["n2", "n12", "n4", "n17", "n18"],
                                               ["n2", "n12", "n4", "n17", "n18"]],
                "attacker_actions": [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                "defender_actions": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "defender_stop_probabilities": [0, 0.02, 0.05, 0.06, 0.05, 0.06, 0.08, 0.25, 0.55, 0.79, 0.95, 0.99,
                                                0.99, 0.99, 0.99, 0.99, 0.99, 0.99],
                "defender_beliefs": [0, 0.02, 0.05, 0.06, 0.05, 0.06, 0.08, 0.25, 0.33, 0.45, 0.48, 0.51,
                                     0.55, 0.6, 0.62, 0.73, 0.78, 0.86],
                "defender_observations": [[39, 48, 52], [101, 2, 4], [30, 51, 28], [9, 12, 3], [45, 10, 19],
                                          [61, 20, 12],
                                          [41, 59, 61], [161, 80, 122], [120, 60, 59], [190, 40, 90], [121, 29, 56],
                                          [100, 31, 45], [161, 80, 20], [119, 67, 5], [67, 51, 9], [167, 105, 98],
                                          [147, 51, 78]],
                "intrusion_start_index": 7,
                "name": "demo"
            }
        ]
        response = jsonify(demo_traces)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        traces = MetastoreFacade.list_emulation_simulation_traces()
        for trace in traces:
            MetastoreFacade.remove_emulation_simulation_trace(trace)
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: "HTTP method not supported"}),
            constants.HTTPS.BAD_REQUEST_STATUS_CODE)


def emulation_simulation_traces_ids() -> Tuple[Response, int]:
    """
    :return: An HTTP response with all emulation ids
    """
    ids_emulations = MetastoreFacade.list_emulation_simulation_traces_ids()
    response_dicts = []
    for tup in ids_emulations:
        response_dicts.append({
            api_constants.MGMT_WEBAPP.ID_PROPERTY: tup[0]
        })
    response = jsonify(response_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@emulation_simulation_traces_bp.route("/<trace_id>", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                                              api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def emulation_trace(trace_id: int) -> Tuple[Response, int]:
    """
    The /emulation-traces/id resource.

    :param trace_id: the id of the trace

    :return: The given trace or delets the trace
    """
    trace = MetastoreFacade.get_emulation_trace(id=trace_id)
    response = jsonify({})
    if trace is not None:
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            response = jsonify(trace.to_dict())
        else:
            MetastoreFacade.remove_emulation_trace(trace)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
