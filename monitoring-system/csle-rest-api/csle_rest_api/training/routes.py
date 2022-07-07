from flask import Blueprint

training = Blueprint("training", __name__, url_prefix="/training",
                       static_url_path='/training/static', static_folder='../../../csle-mgmt-webapp/build')

@training.route('/', methods=['GET'])
def training_page():
    return training.send_static_file('index.html')