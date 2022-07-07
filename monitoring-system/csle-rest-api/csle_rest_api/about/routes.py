from flask import Blueprint

about = Blueprint("about", __name__, url_prefix="/about",
                 static_url_path='/about/static', static_folder='../../../csle-mgmt-webapp/build')

@about.route('/', methods=['GET'])
def about_page():
    return about.send_static_file('index.html')