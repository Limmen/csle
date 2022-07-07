from flask import Blueprint

system_models = Blueprint("systemmodels", __name__, url_prefix="/systemmodels",
                          static_url_path='/systemmodels/static', static_folder='../../../csle-mgmt-webapp/build')

@system_models.route('/', methods=['GET'])
def system_models_page():
    return system_models.send_static_file('index.html')