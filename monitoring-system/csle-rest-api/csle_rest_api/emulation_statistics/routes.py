from flask import Blueprint

emulation_statistics = Blueprint("emulationstatistics", __name__, url_prefix="/emulationstatistics",
                                 static_url_path='/emulationstatistics/static',
                                 static_folder='../../../csle-mgmt-webapp/build')

@emulation_statistics.route('/', methods=['GET'])
def emulation_statistics_page():
    return emulation_statistics.send_static_file('index.html')