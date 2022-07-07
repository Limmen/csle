from flask import Blueprint

emulations = Blueprint("emulations", __name__, url_prefix="/emulations",
                       static_url_path='/emulations/static', static_folder='../../../csle-mgmt-webapp/build')

@emulations.route('/', methods=['GET'])
def emulations_page():
    return emulations.send_static_file('index.html')