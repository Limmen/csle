from flask import Blueprint

jobs = Blueprint("jobs", __name__, url_prefix="/jobs",
                 static_url_path='/jobs/static', static_folder='../../../csle-mgmt-webapp/build')

@jobs.route('/', methods=['GET'])
def jobs_page():
    return jobs.send_static_file('index.html')