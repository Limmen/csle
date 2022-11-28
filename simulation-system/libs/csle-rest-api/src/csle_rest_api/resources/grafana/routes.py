"""
Routes and sub-resources for the /grafana-page page
"""

from flask import Blueprint, jsonify, request
from csle_common.controllers.management_system_controller import ManagementSystemController
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util


# Creates a blueprint "sub application" of the main REST app
grafana_bp = Blueprint(api_constants.MGMT_WEBAPP.GRAFANA_RESOURCE, __name__,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.GRAFANA_RESOURCE}")


@grafana_bp.route("",
                  methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def grafana():
    """
    :return: static resources for the /grafana url
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    running = ManagementSystemController.is_grafana_running()
    port = constants.COMMANDS.GRAFANA_PORT
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        if running:
            ManagementSystemController.stop_grafana()
            running = False
        else:
            ManagementSystemController.start_grafana()
            running = True
    grafana_ip = "localhost"
    if constants.CONFIG_FILE.PARSED_CONFIG is not None:
        grafana_ip = constants.CONFIG_FILE.PARSED_CONFIG.metastore_ip
        port = constants.CONFIG_FILE.PARSED_CONFIG.grafana_port
    grafana_dict = {
        api_constants.MGMT_WEBAPP.RUNNING_PROPERTY: running,
        api_constants.MGMT_WEBAPP.PORT_PROPERTY: port,
        api_constants.MGMT_WEBAPP.URL_PROPERTY: f"http://{grafana_ip}:{port}/"
    }
    response = jsonify(grafana_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
