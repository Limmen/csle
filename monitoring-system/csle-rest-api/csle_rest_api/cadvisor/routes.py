from flask import Blueprint, jsonify, request
from csle_common.controllers.monitor_tools_controller import MonitorToolsController
import csle_common.constants.constants as constants

cadvisor = Blueprint("cadvisor", __name__, url_prefix="/cadvisor",
                 static_url_path='/cadvisor/static', static_folder='../../../csle-mgmt-webapp/build')


@cadvisor.route('/', methods=['GET', 'POST'])
def cadvisor_page():
    running = MonitorToolsController.is_cadvisor_running()
    port = constants.COMMANDS.CADVISOR_PORT
    if request.method == "POST":
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