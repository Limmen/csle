from flask import Blueprint

sdncontrollers = Blueprint("sdncontrollers", __name__, url_prefix="/sdncontrollers",
                 static_url_path='/sdncontrollers/static', static_folder='../../../csle-mgmt-webapp/build')

@sdncontrollers.route('/', methods=['GET'])
def sdncontrollers_page():
    return sdncontrollers.send_static_file('index.html')