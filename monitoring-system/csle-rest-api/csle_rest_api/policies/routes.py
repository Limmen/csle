from flask import Blueprint

policies = Blueprint("policies", __name__, url_prefix="/policies",
                   static_url_path='/policies/static', static_folder='../../../csle-mgmt-webapp/build')

@policies.route('/', methods=['GET'])
def policies_page():
    return policies.send_static_file('index.html')