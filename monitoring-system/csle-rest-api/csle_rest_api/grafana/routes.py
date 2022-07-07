from flask import Blueprint, jsonify, request
from csle_common.controllers.monitor_tools_controller import MonitorToolsController
import csle_common.constants.constants as constants

grafana = Blueprint("grafana", __name__, url_prefix="/grafana",
                 static_url_path='/grafana/static', static_folder='../../../csle-mgmt-webapp/build')


@grafana.route('/', methods=['GET', 'POST'])
def grafana_page():
    running = MonitorToolsController.is_grafana_running()
    port = constants.COMMANDS.GRAFANA_PORT
    if request.method == "POST":
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