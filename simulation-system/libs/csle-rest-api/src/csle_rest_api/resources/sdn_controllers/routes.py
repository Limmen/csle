"""
Routes and sub-resources for the /sdn-controllers resource
"""
from flask import Blueprint, jsonify, request
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.controllers.container_controller import ContainerController
import csle_rest_api.util.rest_api_util as rest_api_util


# Creates a blueprint "sub application" of the main REST app
sdn_controllers_bp = Blueprint(
    api_constants.MGMT_WEBAPP.SDN_CONTROLLERS_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.SDN_CONTROLLERS_RESOURCE}")


@sdn_controllers_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def sdn_controllers():
    """
    The /sdn-controllers resource.

    :return: A list of sdn-controllers or a list of ids of the policies or deletes the policies
    """
    requires_admin = False
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Check if ids query parameter is True, then only return the ids and not the whole list of SDN controllers
    ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
    if ids is not None and ids:
        return sdn_controllers_ids()

    emulations = MetastoreFacade.list_emulations()
    rc_emulations = ContainerController.list_running_emulations()
    response_dicts = []
    for em in emulations:
        if em.sdn_controller_config is not None:
            if em.name in rc_emulations:
                em.running = True
            response_dicts.append(em.to_dict())
    response = jsonify(response_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


def sdn_controllers_ids():
    """
    :return: An HTTP response with all sdn controllers ids
    """
    emulations = MetastoreFacade.list_emulations()
    rc_emulations = ContainerController.list_running_emulations()
    response_dicts = []
    for em in emulations:
        executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(emulation_name=em.name)
        if em.sdn_controller_config is not None:
            running = False
            if em.name in rc_emulations:
                running = True
            for exec in executions:
                response_dicts.append({
                    api_constants.MGMT_WEBAPP.ID_PROPERTY: em.id,
                    api_constants.MGMT_WEBAPP.EMULATION_PROPERTY: em.name,
                    api_constants.MGMT_WEBAPP.RUNNING_PROPERTY: running,
                    api_constants.MGMT_WEBAPP.IP_PROPERTY:
                        exec.emulation_env_config.sdn_controller_config.container.get_ips()[0],
                    api_constants.MGMT_WEBAPP.EXEC_ID_PROPERTY: exec.ip_first_octet
                })
    response = jsonify(response_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
