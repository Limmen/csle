from flask import Flask
from waitress import serve
import csle_common.constants.constants as constants
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
from csle_rest_api.resources.node_exporter.routes import node_exporter_bp
from csle_rest_api.resources.prometheus.routes import prometheus_bp
from csle_rest_api.resources.cadvisor.routes import cadvisor_bp
from csle_rest_api.resources.grafana.routes import grafana_bp
from csle_rest_api.resources.emulations.routes import emulations_bp
from csle_rest_api.resources.emulation_executions.routes import emulation_executions_bp
from csle_rest_api.resources.simulations.routes import simulations_bp
from csle_rest_api.resources.images.routes import images_bp
from csle_rest_api.resources.emulation_traces.routes import emulation_traces_bp
from csle_rest_api.resources.simulation_traces.routes import simulation_traces_bp
from csle_rest_api.resources.emulation_statistics.routes import emulation_statistics_bp
from csle_rest_api.resources.system_models.routes import system_models_bp
from csle_rest_api.resources.experiments.routes import experiments_bp
from csle_rest_api.resources.multi_threshold_policies.routes import multi_threshold_policies_bp
from csle_rest_api.resources.ppo_policies.routes import ppo_policies_bp
from csle_rest_api.resources.dqn_policies.routes import dqn_policies_bp
from csle_rest_api.resources.fnn_w_softmax_policies.routes import fnn_w_softmax_policies_bp
from csle_rest_api.resources.tabular_policies.routes import tabular_policies_bp
from csle_rest_api.resources.vector_policies.routes import vector_policies_bp
from csle_rest_api.resources.alpha_vec_policies.routes import alpha_vec_policies_bp
from csle_rest_api.resources.training_jobs.routes import training_jobs_bp
from csle_rest_api.resources.data_collection_jobs.routes import data_collection_jobs_bp
from csle_rest_api.resources.system_identification_jobs.routes import system_identification_jobs_bp
from csle_rest_api.resources.emulation_simulation_traces.routes import emulation_simulation_traces_bp
from csle_rest_api.resources.sdn_controllers.routes import sdn_controllers_bp
from csle_rest_api.resources.file.routes import file_bp
import csle_rest_api.constants.constants as api_constants


app = Flask(__name__, static_url_path='', static_folder='../../csle-mgmt-webapp/build')
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
app.register_blueprint(cadvisor_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE}")
app.register_blueprint(grafana_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.GRAFANA_RESOURCE}")
app.register_blueprint(images_page_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.IMAGES_PAGE_RESOURCE}")
app.register_blueprint(jobs_page_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.JOBS_PAGE_RESOURCE}")
app.register_blueprint(node_exporter_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE}")
app.register_blueprint(policies_page_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.POLICIES_PAGE_RESOURCE}")
app.register_blueprint(policy_examination_page_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.POLICY_EXAMINATION_PAGE_RESOURCE}")
app.register_blueprint(prometheus_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.PROMETHEUS_RESOURCE}")
app.register_blueprint(training_page_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.TRAINING_PAGE_RESOURCE}")
app.register_blueprint(sdn_controllers_page_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.SDN_CONTROLLERS_PAGE_RESOURCE}")
app.register_blueprint(emulations_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}")
app.register_blueprint(emulation_executions_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}")
app.register_blueprint(simulations_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}")
app.register_blueprint(images_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.IMAGES_RESOURCE}")
app.register_blueprint(emulation_traces_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}")
app.register_blueprint(simulation_traces_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}")
app.register_blueprint(emulation_statistics_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}")
app.register_blueprint(system_models_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.SYSTEM_MODELS_RESOURCE}")
app.register_blueprint(experiments_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}")
app.register_blueprint(multi_threshold_policies_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE}")
app.register_blueprint(ppo_policies_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}")
app.register_blueprint(dqn_policies_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE}")
app.register_blueprint(fnn_w_softmax_policies_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE}")
app.register_blueprint(tabular_policies_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE}")
app.register_blueprint(vector_policies_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE}")
app.register_blueprint(alpha_vec_policies_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.ALPHA_VEC_POLICIES_RESOURCE}")
app.register_blueprint(training_jobs_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}")
app.register_blueprint(data_collection_jobs_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}")
app.register_blueprint(system_identification_jobs_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}")
app.register_blueprint(emulation_simulation_traces_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.EMULATION_SIMULATION_TRACES_RESOURCE}")
app.register_blueprint(file_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.FILE_RESOURCE}")
app.register_blueprint(sdn_controllers_bp,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                  f"{api_constants.MGMT_WEBAPP.SDN_CONTROLLERS_RESOURCE}")

@app.route('/', methods=['GET'])
def root():
    return app.send_static_file('index.html')


def start_server():
    serve(app, host='0.0.0.0', port=7777, threads=100)

