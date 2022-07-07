from flask import Blueprint

images = Blueprint("images", __name__, url_prefix="/images",
                   static_url_path='/images/static', static_folder='../../../csle-mgmt-webapp/build')

@images.route('/', methods=['GET'])
def images_page():
    return images.send_static_file('index.html')