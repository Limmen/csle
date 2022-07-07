from flask import Blueprint, jsonify
from csle_common.controllers.monitor_tools_controller import MonitorToolsController
import csle_common.constants.constants as constants

nodeexporter = Blueprint("nodeexporter", __name__, url_prefix="/nodeexporter",
                 static_url_path='/nodeexporter/static', static_folder='../../../csle-mgmt-webapp/build')

@nodeexporter.route('/', methods=['GET', 'POST'])
def node_exporter_page():
    running = MonitorToolsController.is_node_exporter_running()
    port = constants.COMMANDS.NODE_EXPORTER_PORT
    node_exporter_dict = {
        "running": running,
        "port": port,
        "url": f"http://localhost:{port}/"
    }
    response = jsonify(node_exporter_dict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response