from flask import Blueprint

emulationstatistics = Blueprint("emulationstatistics", __name__, url_prefix="/emulationstatistics",
                       static_url_path='/emulationstatistics/static', static_folder='../../../csle-mgmt-webapp/build')

@emulationstatistics.route('/', methods=['GET'])
def statistics_page():
    return emulationstatistics.send_static_file('index.html')