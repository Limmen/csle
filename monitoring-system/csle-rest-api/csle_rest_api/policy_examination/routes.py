from flask import Blueprint

policy_examination = Blueprint("policyexamination", __name__, url_prefix="/policyexamination",
                               static_url_path='/policyexamination/static',
                               static_folder='../../../csle-mgmt-webapp/build')

@policy_examination.route('/', methods=['GET'])
def policy_examination_page():
    return policy_examination.send_static_file('index.html')