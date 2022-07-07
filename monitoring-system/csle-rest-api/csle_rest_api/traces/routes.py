from flask import Blueprint

traces = Blueprint("traces", __name__, url_prefix="/traces",
                       static_url_path='/traces/static', static_folder='../../../csle-mgmt-webapp/build')

@traces.route('/', methods=['GET'])
def traces_page():
    return traces.send_static_file('index.html')