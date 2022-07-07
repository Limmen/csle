"""
Routes and resources for the /cadvisor resource
"""

from flask import Blueprint, jsonify, request
from csle_common.controllers.monitor_tools_controller import MonitorToolsController
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants


# Creates a blueprint "sub application" of the main REST app
cadvisor_bp = Blueprint(api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE, __name__,
                        url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE}",
                        static_url_path=f'{constants.COMMANDS.SLASH_DELIM}'
                                     f'{api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE}'
                                     f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.STATIC}',
                        static_folder='../../../csle-mgmt-webapp/build')


@cadvisor_bp.route("",
                   methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def cadvisor():
    """
    :return: static resources for the /cadvisor url
    """
    running = MonitorToolsController.is_cadvisor_running()
    port = constants.COMMANDS.CADVISOR_PORT
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        if running:
            MonitorToolsController.stop_cadvisor()
            running = False
        else:
            MonitorToolsController.start_cadvisor()
            running = True
    cadvisor_dict = {
        "running": running,
        "port": port,
        "url": f"http://localhost:{port}/"
    }
    response = jsonify(cadvisor_dict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response