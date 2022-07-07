from flask import Blueprint

sdn_controllers = Blueprint("sdncontrollers", __name__, url_prefix="/sdncontrollers",
                            static_url_path='/sdncontrollers/static', static_folder='../../../csle-mgmt-webapp/build')

@sdn_controllers.route('/', methods=['GET'])
def sdn_controllers_page():
    return sdn_controllers.send_static_file('index.html')