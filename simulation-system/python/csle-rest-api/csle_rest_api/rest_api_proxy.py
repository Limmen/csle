from flask import Flask
from requests import get
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.pages.emulations.routes import emulations_page_bp
from csle_rest_api.pages.simulations.routes import simulations_page_bp
from csle_rest_api.pages.monitoring.routes import monitoring_page_bp
from csle_rest_api.pages.traces.routes import traces_page_bp
from csle_rest_api.pages.emulation_statistics.routes import emulation_statistics_page_bp
from csle_rest_api.pages.system_models.routes import system_models_page_bp
from csle_rest_api.pages.about.routes import about_page_bp
from csle_rest_api.pages.images.routes import images_page_bp
from csle_rest_api.pages.jobs.routes import jobs_page_bp
from csle_rest_api.pages.policies.routes import policies_page_bp
from csle_rest_api.pages.policy_examination.routes import policy_examination_page_bp
from csle_rest_api.pages.training.routes import training_page_bp
from csle_rest_api.pages.sdn_controllers.routes import sdn_controllers_page_bp

# app = Flask(__name__)
SITE_NAME = 'http://172.31.212.92:7777/'
static_folder = "../../../../monitoring-system/csle-mgmt-webapp/build"

app = Flask(__name__, static_url_path='', static_folder=static_folder)

app.register_blueprint(emulations_page_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.EMULATIONS_PAGE_RESOURCE}")
app.register_blueprint(simulations_page_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.SIMULATIONS_PAGE_RESOURCE}")
app.register_blueprint(traces_page_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.TRACES_PAGE_RESOURCE}")
app.register_blueprint(monitoring_page_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.MONITORING_PAGE_RESOURCE}")
app.register_blueprint(emulation_statistics_page_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_PAGE_RESOURCE}")
app.register_blueprint(system_models_page_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.SYSTEM_MODELS_PAGE_RESOURCE}")
app.register_blueprint(about_page_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.ABOUT_PAGE_RESOURCE}")
app.register_blueprint(images_page_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.IMAGES_PAGE_RESOURCE}")
app.register_blueprint(jobs_page_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.JOBS_PAGE_RESOURCE}")
app.register_blueprint(policies_page_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.POLICIES_PAGE_RESOURCE}")
app.register_blueprint(policy_examination_page_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.POLICY_EXAMINATION_PAGE_RESOURCE}")
app.register_blueprint(training_page_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.TRAINING_PAGE_RESOURCE}")
app.register_blueprint(sdn_controllers_page_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.SDN_CONTROLLERS_PAGE_RESOURCE}")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    return get(f'{SITE_NAME}{path}').content

@app.route('/<path:path>/<path:path2>')
def proxy_1(path, path2):
    return get(f'{SITE_NAME}{path}/{path2}').content

@app.route('/<path:path>/<path:path2>/<path:path3>')
def proxy_2(path, path2, path3):
    return get(f'{SITE_NAME}{path}/{path2}/{path3}').content

@app.route('/<path:path>/<path:path2>/<path:path3>/<path:path4>')
def proxy_3(path, path2, path3, path4):
    return get(f'{SITE_NAME}{path}/{path2}/{path3}/{path4}').content

@app.route('/<path:path>/<path:path2>/<path:path3>/<path:path4>/<path:path5>')
def proxy_4(path, path2, path3, path4, path5):
    return get(f'{SITE_NAME}{path}/{path2}/{path3}/{path4}/{path5}').content

# @app.route('/static/<path:path1>')
# def static_1(path1):
#     return get(f'{SITE_NAME}static/{path1}').content
#
# @app.route('/static/<path:path1>/<path:path2>')
# def static_2(path1, path2):
#     return get(f'{SITE_NAME}static/{path1}/{path2}').content
#
# @app.route('/static/<path:path1>/<path:path2>/<path:path3>')
# def static_3(path1, path2, path3):
#     return get(f'{SITE_NAME}static/{path1}/{path2}/{path3}').content
#
# @app.route('/static/<path:path1>/<path:path2>/<path:path3>/<path:path4>')
# def static_4(path1, path2, path3, path4):
#     return get(f'{SITE_NAME}static/{path1}/{path2}/{path3}/{path4}').content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)