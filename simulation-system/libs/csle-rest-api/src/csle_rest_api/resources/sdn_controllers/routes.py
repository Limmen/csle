"""
Routes and sub-resources for the /sdn-controllers resource
"""
from typing import List, Tuple
from flask import Blueprint, jsonify, request, Response
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_cluster.cluster_manager.cluster_controller import ClusterController
import csle_rest_api.util.rest_api_util as rest_api_util


# Creates a blueprint "sub application" of the main REST app
sdn_controllers_bp = Blueprint(
    api_constants.MGMT_WEBAPP.SDN_CONTROLLERS_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.SDN_CONTROLLERS_RESOURCE}")


@sdn_controllers_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def sdn_controllers() -> Tuple[Response, int]:
    """
    The /sdn-controllers resource.

    :return: A list of emulation executions with sdn-controllers
             or a list of ids of the executions
    """
    requires_admin = False
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Check if ids query parameter is True, then only return the ids and not the whole list of SDN controllers
    ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
    if ids is not None and ids:
        return sdn_controllers_ids()

    all_executions = MetastoreFacade.list_emulation_executions()
    emulation_execution_dicts = []
    for exec in all_executions:
        if exec.emulation_env_config.sdn_controller_config is not None:
            emulation_execution_dicts.append(exec.to_dict())
    response = jsonify(emulation_execution_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


def sdn_controllers_ids() -> Tuple[Response, int]:
    """
    :return: An HTTP response with all sdn controllers ids
    """
    ex_ids = MetastoreFacade.list_emulation_execution_ids()
    running_emulation_names: List[str] = []
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        running_emulation_names = running_emulation_names + list(ClusterController.list_all_running_emulations(
            ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT
        ).runningEmulations)
    response_dicts = []
    for tup in ex_ids:
        if tup[1] in running_emulation_names:
            exec = MetastoreFacade.get_emulation_execution(ip_first_octet=tup[0], emulation_name=tup[1])
            if exec.emulation_env_config.sdn_controller_config is not None:
                response_dicts.append({
                    api_constants.MGMT_WEBAPP.ID_PROPERTY: tup[0],
                    api_constants.MGMT_WEBAPP.EMULATION_PROPERTY: tup[1],
                    api_constants.MGMT_WEBAPP.RUNNING_PROPERTY: True
                })
    response = jsonify(response_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
