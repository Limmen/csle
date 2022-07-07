from flask import Blueprint

monitoring = Blueprint("monitoring", __name__, url_prefix="/monitoring",
                       static_url_path='/monitoring/static', static_folder='../../../csle-mgmt-webapp/build')

@monitoring.route('/', methods=['GET'])
def monitoring_page():
    return monitoring.send_static_file('index.html')