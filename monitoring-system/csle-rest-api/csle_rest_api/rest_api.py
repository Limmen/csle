import base64
import time
import os
import requests
from flask import Flask, jsonify, request
import csle_ryu.constants.constants as ryu_constants
import csle_common.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.controllers.container_manager import ContainerManager
from csle_common.util.read_emulation_statistics import ReadEmulationStatistics
from csle_common.controllers.emulation_env_manager import EmulationEnvManager
from csle_common.controllers.monitor_tools_controller import MonitorToolsController
from csle_common.util.emulation_util import EmulationUtil
from csle_agents.job_controllers.training_job_manager import TrainingJobManager
from csle_system_identification.job_controllers.data_collection_job_manager import DataCollectionJobManager
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
import csle_rest_api.constants.constants as api_constants
import json
from waitress import serve


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


@app.route('/', methods=['GET'])
def root():
    return app.send_static_file('index.html')


# @app.route('/emulationsimulationtraces', methods=['GET'])
# def emulationsimulationtraces():
#     # emulation_simulation_traces = MetastoreFacade.list_emulation_simulation_traces()
#     # emulation_simulation_traces_dicts = list(map(lambda x: x.to_dict(), emulation_simulation_traces))
#     # response = jsonify(emulation_simulation_traces_dicts)
#     f = open('/var/log/csle/one_tau.json')
#     d = json.load(f)
#     response = jsonify(d["trajectories"])
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response


# @app.route('/file', methods=['POST'])
# def read_file():
#     path = json.loads(request.data)["path"]
#     data = ""
#     if os.path.exists(path):
#         with open(path, 'r') as fp:
#             data = fp.read()
#     data_dict = {"logs": data}
#     response = jsonify(data_dict)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
#
# @app.route('/sdncontrollersids', methods=['GET'])
# def sdncontrollerids():
#     emulations = MetastoreFacade.list_emulations()
#     rc_emulations = ContainerManager.list_running_emulations()
#     response_dicts = []
#     for em in emulations:
#         executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(emulation_name=em.name)
#         if em.sdn_controller_config is not None:
#             running = False
#             if em.name in rc_emulations:
#                 running = True
#             for exec in executions:
#                 response_dicts.append({
#                     "id": em.id,
#                     "emulation": em.name,
#                     "running": running,
#                     "ip": exec.emulation_env_config.sdn_controller_config.container.get_ips()[0],
#                     "exec_id": exec.ip_first_octet
#                 })
#     response = jsonify(response_dicts)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/sdncontrollersids/get/<emulation_id>/<exec_id>', methods=['GET'])
# def sdn_controller_by_id(emulation_id: int, exec_id: int):
#     em = MetastoreFacade.get_emulation(id=emulation_id)
#     rc_emulations = ContainerManager.list_running_emulations()
#     em_dict = {}
#     if em is not None and em.sdn_controller_config is not None:
#         executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(emulation_name=em.name)
#         if em.name in rc_emulations:
#             em.running = True
#         for exec in executions:
#             if int(exec.ip_first_octet) == int(exec_id):
#                 if em.running:
#                     exec.emulation_env_config.running = True
#                 em_dict = exec.emulation_env_config.to_dict()
#     response = jsonify(em_dict)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/sdncontroller/switches/get/<emulation_id>/<exec_id>', methods=['GET'])
# def sdn_controller_switches(emulation_id: int, exec_id: int):
#     em = MetastoreFacade.get_emulation(id=emulation_id)
#     response_data = {}
#     if em is not None and em.sdn_controller_config is not None:
#         executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(emulation_name=em.name)
#         for exec in executions:
#             if int(exec.ip_first_octet) == int(exec_id):
#                 response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
#                                         f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
#                                         f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
#                                         f"{ryu_constants.RYU.STATS_SWITCHES_RESOURCE}")
#                 switches = json.loads(response.content)
#                 switches_dicts = []
#                 for dpid in switches:
#                     response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
#                                             f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
#                                             f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
#                                             f"{ryu_constants.RYU.STATS_DESC_RESOURCE}/{dpid}")
#                     sw_dict = {}
#                     sw_dict["dpid"] = dpid
#                     sw_dict["desc"] = json.loads(response.content)[str(dpid)]
#                     response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
#                                             f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
#                                             f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
#                                             f"{ryu_constants.RYU.STATS_FLOW_RESOURCE}/{dpid}")
#                     sw_dict["flows"] = json.loads(response.content)[str(dpid)]
#                     response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
#                                             f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
#                                             f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
#                                             f"{ryu_constants.RYU.STATS_AGGREGATE_FLOW_RESOURCE}/{dpid}")
#                     sw_dict["aggflows"] = json.loads(response.content)[str(dpid)][0]
#                     response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
#                                             f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
#                                             f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
#                                             f"{ryu_constants.RYU.STATS_TABLE_RESOURCE}/{dpid}")
#                     tables = json.loads(response.content)[str(dpid)]
#                     tables = list(filter(lambda x: x["active_count"] > 0, tables))
#                     filtered_table_ids = list(map(lambda x: x["table_id"], tables))
#                     sw_dict["tables"] = tables
#                     response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
#                                             f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
#                                             f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
#                                             f"{ryu_constants.RYU.STATS_TABLE_FEATURES_RESOURCE}/{dpid}")
#                     tablefeatures = json.loads(response.content)[str(dpid)]
#                     tablefeatures = list(filter(lambda x: x["table_id"] in filtered_table_ids, tablefeatures))
#                     sw_dict["tablefeatures"] = tablefeatures
#                     response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
#                                             f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
#                                             f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
#                                             f"{ryu_constants.RYU.STATS_PORT_RESOURCE}/{dpid}")
#                     sw_dict["portstats"] = json.loads(response.content)[str(dpid)]
#                     response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
#                                             f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
#                                             f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
#                                             f"{ryu_constants.RYU.STATS_PORT_DESC_RESOURCE}/{dpid}")
#                     sw_dict["portdescs"] = json.loads(response.content)[str(dpid)]
#                     response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
#                                             f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
#                                             f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
#                                             f"{ryu_constants.RYU.STATS_QUEUE_RESOURCE}/{dpid}")
#                     sw_dict["queues"] = json.loads(response.content)[str(dpid)]
#                     response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
#                                             f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
#                                             f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
#                                             f"{ryu_constants.RYU.STATS_QUEUE_CONFIG_RESOURCE}/{dpid}")
#                     sw_dict["queueconfigs"] = json.loads(response.content)[str(dpid)][0]
#                     response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
#                                             f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
#                                             f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
#                                             f"{ryu_constants.RYU.STATS_GROUP_RESOURCE}/{dpid}")
#                     sw_dict["groups"] = json.loads(response.content)[str(dpid)]
#                     response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
#                                             f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
#                                             f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
#                                             f"{ryu_constants.RYU.STATS_GROUP_DESC_RESOURCE}/{dpid}")
#                     sw_dict["groupdescs"] = json.loads(response.content)[str(dpid)]
#                     response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
#                                             f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
#                                             f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
#                                             f"{ryu_constants.RYU.STATS_GROUP_FEATURES_RESOURCE}/{dpid}")
#                     sw_dict["groupfeatures"] = json.loads(response.content)[str(dpid)][0]
#                     response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
#                                             f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
#                                             f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
#                                             f"{ryu_constants.RYU.STATS_METER_RESOURCE}/{dpid}")
#                     sw_dict["meters"] = json.loads(response.content)[str(dpid)]
#                     response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
#                                             f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
#                                             f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
#                                             f"{ryu_constants.RYU.STATS_METER_CONFIG_RESOURCE}/{dpid}")
#                     sw_dict["meter_configs"] = json.loads(response.content)[str(dpid)]
#                     response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
#                                             f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
#                                             f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
#                                             f"{ryu_constants.RYU.STATS_METER_FEATURES_RESOURCE}/{dpid}")
#                     sw_dict["meter_features"] = json.loads(response.content)[str(dpid)][0]
#                     response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
#                                             f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
#                                             f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
#                                             f"{ryu_constants.RYU.STATS_ROLE_RESOURCE}/{dpid}")
#                     sw_dict["roles"] = json.loads(response.content)[str(dpid)][0]
#                     switches_dicts.append(sw_dict)
#                 response_data = switches_dicts
#
#     response = jsonify(response_data)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response

def start_server():
    serve(app, host='0.0.0.0', port=7777, threads=100)

