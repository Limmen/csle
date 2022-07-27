"""
Routes and sub-resources for the /grafana-page page
"""

from flask import Blueprint, jsonify, request
from csle_common.controllers.monitor_tools_controller import MonitorToolsController
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants


# Creates a blueprint "sub application" of the main REST app
grafana_bp = Blueprint(api_constants.MGMT_WEBAPP.GRAFANA_RESOURCE, __name__,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.GRAFANA_RESOURCE}")


@grafana_bp.route("",
                  methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def grafana():
    """
    :return: static resources for the /grafana url
    """
    running = MonitorToolsController.is_grafana_running()
    port = constants.COMMANDS.GRAFANA_PORT
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        if running:
            MonitorToolsController.stop_grafana()
            running = False
        else:
            MonitorToolsController.start_grafana()
            running = True
    grafana_dict = {
        api_constants.MGMT_WEBAPP.RUNNING_PROPERTY: running,
        api_constants.MGMT_WEBAPP.PORT_PROPERTY: port,
        api_constants.MGMT_WEBAPP.URL_PROPERTY: f"http://localhost:{port}/"
    }
    response = jsonify(grafana_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE