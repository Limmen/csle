from flask import Blueprint

systemmodels = Blueprint("systemmodels", __name__, url_prefix="/systemmodels",
                       static_url_path='/systemmodels/static', static_folder='../../../csle-mgmt-webapp/build')

@systemmodels.route('/', methods=['GET'])
def system_models_page():
    return systemmodels.send_static_file('index.html')