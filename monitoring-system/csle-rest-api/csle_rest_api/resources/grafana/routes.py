"""
Routes and resources for the /grafana-page page
"""

from flask import Blueprint, jsonify, request
from csle_common.controllers.monitor_tools_controller import MonitorToolsController
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants


# Creates a blueprint "sub application" of the main REST app
grafana_bp = Blueprint(api_constants.MGMT_WEBAPP.GRAFANA_RESOURCE, __name__,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.GRAFANA_RESOURCE}",
                       static_url_path=f'{constants.COMMANDS.SLASH_DELIM}'
                                    f'{api_constants.MGMT_WEBAPP.GRAFANA_RESOURCE}'
                                    f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.STATIC}',
                       static_folder='../../../csle-mgmt-webapp/build')


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
        "running": running,
        "port": port,
        "url": f"http://localhost:{port}/"
    }
    response = jsonify(grafana_dict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response