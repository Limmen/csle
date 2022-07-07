from flask import Blueprint

policyexamination = Blueprint("policyexamination", __name__, url_prefix="/policyexamination",
                       static_url_path='/policyexamination/static', static_folder='../../../csle-mgmt-webapp/build')

@policyexamination.route('/', methods=['GET'])
def policy_examination_page():
    return policyexamination.send_static_file('index.html')