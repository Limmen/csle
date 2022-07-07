from flask import Blueprint

simulations = Blueprint("simulations", __name__, url_prefix="/simulations",
                       static_url_path='/simulations/static', static_folder='../../../csle-mgmt-webapp/build')

@simulations.route('/', methods=['GET'])
def simulations_page():
    return simulations.send_static_file('index.html')