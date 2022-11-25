"""
Routes and sub-resources for the /prometheus resource
"""

from flask import Blueprint, jsonify, request
from csle_common.controllers.management_system_controller import ManagementSystemController
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util


# Creates a blueprint "sub application" of the main REST app
prometheus_bp = Blueprint(api_constants.MGMT_WEBAPP.PROMETHEUS_RESOURCE, __name__,
                          url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.PROMETHEUS_RESOURCE}")


@prometheus_bp.route("",
                     methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def prometheus():
    """
    :return: static resources for the /prometheus url
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    running = ManagementSystemController.is_prometheus_running()
    port = constants.COMMANDS.PROMETHEUS_PORT
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        if running:
            ManagementSystemController.stop_prometheus()
            running = False
        else:
            ManagementSystemController.start_prometheus()
            running = True
    prometheus_ip = "localhost"
    if constants.CONFIG_FILE.PARSED_CONFIG is not None:
        prometheus_ip = constants.CONFIG_FILE.PARSED_CONFIG.metastore_ip
        port = constants.CONFIG_FILE.PARSED_CONFIG.prometheus_port
    prometheus_dict = {
        api_constants.MGMT_WEBAPP.RUNNING_PROPERTY: running,
        api_constants.MGMT_WEBAPP.PORT_PROPERTY: port,
        api_constants.MGMT_WEBAPP.URL_PROPERTY: f"http://{prometheus_ip}:{port}/"
    }
    response = jsonify(prometheus_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
