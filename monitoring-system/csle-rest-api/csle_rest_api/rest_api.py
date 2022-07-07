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
from csle_system_identification.job_controllers.system_identification_job_manager import SystemIdentificationJobManager
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


@app.route('/', methods=['GET'])
def root():
    return app.send_static_file('index.html')

#
# @app.route('/multithresholdpolicies', methods=['GET'])
# def policies():
#     multi_threshold_stopping_policies = MetastoreFacade.list_multi_threshold_stopping_policies()
#     multi_threshold_stopping_policies_dicts = list(map(lambda x: x.to_dict(), multi_threshold_stopping_policies))
#     response = jsonify(multi_threshold_stopping_policies_dicts)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/multithresholdpoliciesids', methods=['GET'])
# def multi_threshold_policies_ids():
#     multi_threshold_stopping_policies_ids = MetastoreFacade.list_multi_threshold_stopping_policies_ids()
#     response_dicts = []
#     for tup in multi_threshold_stopping_policies_ids:
#         response_dicts.append({
#             "id": tup[0],
#             "simulation": tup[1]
#         })
#     response = jsonify(response_dicts)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/multithresholdpolicies/get/<multi_threshold_stopping_policy_id>', methods=['GET'])
# def get_multi_threshold_policy(multi_threshold_stopping_policy_id: int):
#     policy = MetastoreFacade.get_multi_threshold_stopping_policy(id=multi_threshold_stopping_policy_id)
#     if policy is not None:
#         response = jsonify(policy.to_dict())
#     else:
#         response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/multithresholdpolicies/remove/<multi_threshold_stopping_policy_id>', methods=['POST'])
# def remove_multi_threshold_policy(multi_threshold_stopping_policy_id: int):
#     policy = MetastoreFacade.get_multi_threshold_stopping_policy(id=multi_threshold_stopping_policy_id)
#     if policy is not None:
#         MetastoreFacade.remove_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/multithresholdpolicies/remove', methods=['POST'])
# def remove_all_multi_threshold_policies():
#     policies = MetastoreFacade.list_multi_threshold_stopping_policies()
#     for policy in policies:
#         MetastoreFacade.remove_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/ppopolicies', methods=['GET'])
# def ppo_policies():
#     ppo_policies = MetastoreFacade.list_ppo_policies()
#     ppo_policies_dicts = list(map(lambda x: x.to_dict(), ppo_policies))
#     response = jsonify(ppo_policies_dicts)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/ppopoliciesids', methods=['GET'])
# def ppo_policies_ids():
#     ppo_policies_ids = MetastoreFacade.list_ppo_policies_ids()
#     response_dicts = []
#     for tup in ppo_policies_ids:
#         response_dicts.append({
#             "id": tup[0],
#             "simulation": tup[1]
#         })
#     response = jsonify(response_dicts)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/ppopolicies/get/<ppo_policy_id>', methods=['GET'])
# def get_ppo_policy(ppo_policy_id: int):
#     policy = MetastoreFacade.get_ppo_policy(id=ppo_policy_id)
#     if policy is not None:
#         response = jsonify(policy.to_dict())
#     else:
#         response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/ppopolicies/remove/<ppo_policy_id>', methods=['POST'])
# def remove_ppo_policy(ppo_policy_id: int):
#     policy = MetastoreFacade.get_ppo_policy(id=ppo_policy_id)
#     if policy is not None:
#         MetastoreFacade.remove_ppo_policy(ppo_policy=policy)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/ppopolicies/remove', methods=['POST'])
# def remove_all_ppo_policies():
#     policies = MetastoreFacade.list_ppo_policies()
#     for policy in policies:
#         MetastoreFacade.remove_ppo_policy(ppo_policy=policy)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/dqnpolicies', methods=['GET'])
# def dqn_policies():
#     dqn_policies = MetastoreFacade.list_dqn_policies()
#     dqn_policies_dicts = list(map(lambda x: x.to_dict(), dqn_policies))
#     response = jsonify(dqn_policies_dicts)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/dqnpoliciesids', methods=['GET'])
# def dqn_policies_ids():
#     dqn_policies_ids = MetastoreFacade.list_dqn_policies_ids()
#     response_dicts = []
#     for tup in dqn_policies_ids:
#         response_dicts.append({
#             "id": tup[0],
#             "simulation": tup[1]
#         })
#     response = jsonify(response_dicts)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/dqnpolicies/get/<dqn_policy_id>', methods=['GET'])
# def get_dqn_policy(dqn_policy_id: int):
#     policy = MetastoreFacade.get_dqn_policy(id=dqn_policy_id)
#     if policy is not None:
#         response = jsonify(policy.to_dict())
#     else:
#         response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/dqnpolicies/remove/<dqn_policy_id>', methods=['POST'])
# def remove_dqn_policy(dqn_policy_id: int):
#     policy = MetastoreFacade.get_dqn_policy(id=dqn_policy_id)
#     if policy is not None:
#         MetastoreFacade.remove_dqn_policy(dqn_policy=policy)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/dqnpolicies/remove', methods=['POST'])
# def remove_all_dqn_policies():
#     policies = MetastoreFacade.list_dqn_policies()
#     for policy in policies:
#         MetastoreFacade.remove_dqn_policy(dqn_policy=policy)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/fnnwsoftmaxpolicies', methods=['GET'])
# def fnn_w_softmax_policies():
#     policies = MetastoreFacade.list_fnn_w_softmax_policies()
#     policies_dicts = list(map(lambda x: x.to_dict(), policies))
#     response = jsonify(policies_dicts)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/fnnwsoftmaxpoliciesids', methods=['GET'])
# def fnn_w_softmax_policies_ids():
#     policies_ids = MetastoreFacade.list_fnn_w_softmax_policies_ids()
#     response_dicts = []
#     for tup in policies_ids:
#         response_dicts.append({
#             "id": tup[0],
#             "simulation": tup[1]
#         })
#     response = jsonify(response_dicts)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/fnnwsoftmaxpolicies/get/<fnn_w_softmax_policy_id>', methods=['GET'])
# def get_fnn_w_softmax_policy(fnn_w_softmax_policy_id: int):
#     policy = MetastoreFacade.get_fnn_w_softmax_policy(id=fnn_w_softmax_policy_id)
#     if policy is not None:
#         response = jsonify(policy.to_dict())
#     else:
#         response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/fnnwsoftmaxpolicies/remove/<fnn_w_softmax_policy_id>', methods=['POST'])
# def remove_fnn_w_softmax_policy(fnn_w_softmax_policy_id: int):
#     policy = MetastoreFacade.get_fnn_w_softmax_policy(id=fnn_w_softmax_policy_id)
#     if policy is not None:
#         MetastoreFacade.remove_fnn_w_softmax_policy(fnn_w_softmax_policy=policy)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/fnnwsoftmaxpolicies/remove', methods=['POST'])
# def remove_all_fnn_w_softmax_policies():
#     policies = MetastoreFacade.list_fnn_w_softmax_policies()
#     for policy in policies:
#         MetastoreFacade.remove_fnn_w_softmax_policy(fnn_w_softmax_policy=policy)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/tabularpolicies', methods=['GET'])
# def tabular_policies():
#     tabular_policies = MetastoreFacade.list_tabular_policies()
#     tabular_policies_dicts = list(map(lambda x: x.to_dict(), tabular_policies))
#     response = jsonify(tabular_policies_dicts)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/tabularpoliciesids', methods=['GET'])
# def tabular_policies_ids():
#     tabular_policies_ids = MetastoreFacade.list_tabular_policies_ids()
#     response_dicts = []
#     for tup in tabular_policies_ids:
#         response_dicts.append({
#             "id": tup[0],
#             "simulation": tup[1]
#         })
#     response = jsonify(response_dicts)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/tabularpolicies/get/<tabular_policy_id>', methods=['GET'])
# def get_tabular_policy(tabular_policy_id: int):
#     policy = MetastoreFacade.get_tabular_policy(id=tabular_policy_id)
#     if policy is not None:
#         response = jsonify(policy.to_dict())
#     else:
#         response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/tabularpolicies/remove/<tabular_policy_id>', methods=['POST'])
# def remove_tabular_policy(tabular_policy_id: int):
#     policy = MetastoreFacade.get_tabular_policy(id=tabular_policy_id)
#     if policy is not None:
#         MetastoreFacade.remove_tabular_policy(tabular_policy=policy)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/tabularpolicies/remove', methods=['POST'])
# def remove_all_tabular_policies():
#     policies = MetastoreFacade.list_tabular_policies()
#     for policy in policies:
#         MetastoreFacade.remove_tabular_policy(tabular_policy=policy)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/vectorpolicies', methods=['GET'])
# def vector_policies():
#     vector_policies = MetastoreFacade.list_vector_policies()
#     vector_policies_dicts = list(map(lambda x: x.to_dict(), vector_policies))
#     response = jsonify(vector_policies_dicts)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/vectorpoliciesids', methods=['GET'])
# def vector_policies_ids():
#     vector_policies_ids = MetastoreFacade.list_vector_policies_ids()
#     response_dicts = []
#     for tup in vector_policies_ids:
#         response_dicts.append({
#             "id": tup[0],
#             "simulation": tup[1]
#         })
#     response = jsonify(response_dicts)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/vectorpolicies/get/<vector_policy_id>', methods=['GET'])
# def get_vector_policy(vector_policy_id: int):
#     policy = MetastoreFacade.get_vector_policy(id=vector_policy_id)
#     if policy is not None:
#         response = jsonify(policy.to_dict())
#     else:
#         response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/vectorpolicies/remove/<vector_policy_id>', methods=['POST'])
# def remove_vector_policy(vector_policy_id: int):
#     policy = MetastoreFacade.get_vector_policy(id=vector_policy_id)
#     if policy is not None:
#         MetastoreFacade.remove_vector_policy(vector_policy=policy)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/vectorpolicies/remove', methods=['POST'])
# def remove_all_vector_policies():
#     policies = MetastoreFacade.list_vector_policies()
#     for policy in policies:
#         MetastoreFacade.remove_vector_policy(vector_policy=policy)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/alphavecpolicies', methods=['GET'])
# def alpha_vec_policies():
#     alpha_vec_policies = MetastoreFacade.list_alpha_vec_policies()
#     alpha_vec_policies_dicts = list(map(lambda x: x.to_dict(), alpha_vec_policies))
#     response = jsonify(alpha_vec_policies_dicts)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/alphavecpoliciesids', methods=['GET'])
# def alpha_vec_policies_ids():
#     alpha_vec_policies_ids = MetastoreFacade.list_alpha_vec_policies_ids()
#     response_dicts = []
#     for tup in alpha_vec_policies_ids:
#         response_dicts.append({
#             "id": tup[0],
#             "simulation": tup[1]
#         })
#     response = jsonify(response_dicts)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/alphavecpolicies/get/<alpha_vec_policy_id>', methods=['GET'])
# def get_alpha_vec_policy(alpha_vec_policy_id: int):
#     policy = MetastoreFacade.get_alpha_vec_policy(id=alpha_vec_policy_id)
#     if policy is not None:
#         response = jsonify(policy.to_dict())
#     else:
#         response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/alphavecpolicies/remove/<alpha_vec_policy_id>', methods=['POST'])
# def remove_alpha_vec_policy(alpha_vec_policy_id: int):
#     policy = MetastoreFacade.get_alpha_vec_policy(id=alpha_vec_policy_id)
#     if policy is not None:
#         MetastoreFacade.remove_alpha_vec_policy(alpha_vec_policy=policy)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/alphavecpolicies/remove', methods=['POST'])
# def remove_all_alpha_vec_policies():
#     policies = MetastoreFacade.list_alpha_vec_policies()
#     for policy in policies:
#         MetastoreFacade.remove_alpha_vec_policy(alpha_vec_policy=policy)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/trainingjobs', methods=['GET'])
# def trainingjobs():
#     training_jobs = MetastoreFacade.list_training_jobs()
#     alive_jobs = []
#     for job in training_jobs:
#         if EmulationUtil.check_pid(job.pid):
#             job.running = True
#         alive_jobs.append(job)
#     training_jobs_dicts = list(map(lambda x: x.to_dict(), alive_jobs))
#     response = jsonify(training_jobs_dicts)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/trainingjobsids', methods=['GET'])
# def trainingjobsids():
#     training_jobs_ids = MetastoreFacade.list_training_jobs_ids()
#     response_dicts = []
#     for tup in training_jobs_ids:
#         response_dicts.append({
#             "id": tup[0],
#             "simulation": tup[1],
#             "emulation": tup[2],
#             "running": EmulationUtil.check_pid(tup[3])
#         })
#     response = jsonify(response_dicts)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/trainingjobs/get/<job_id>', methods=['GET'])
# def get_trainingjob(job_id: int):
#     job = MetastoreFacade.get_training_job_config(id=job_id)
#     if job is not None:
#         if EmulationUtil.check_pid(job.pid):
#             job.running = True
#         response = jsonify(job.to_dict())
#     else:
#         response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/trainingjobs/stop/<job_id>', methods=['POST'])
# def stop_trainingjob(job_id: int):
#     job = MetastoreFacade.get_training_job_config(id=job_id)
#     if job is not None:
#         MonitorToolsController.stop_pid(pid=job.pid)
#         time.sleep(2)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/trainingjobs/start/<job_id>', methods=['POST'])
# def start_trainingjob(job_id: int):
#     job = MetastoreFacade.get_training_job_config(id=job_id)
#     if job is not None:
#         TrainingJobManager.start_training_job_in_background(training_job=job)
#         time.sleep(2)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/trainingjobs/remove/<job_id>', methods=['POST'])
# def remove_trainingjob(job_id: int):
#     job = MetastoreFacade.get_training_job_config(id=job_id)
#     if job is not None:
#         MonitorToolsController.stop_pid(job.pid)
#         MetastoreFacade.remove_training_job(training_job=job)
#         time.sleep(2)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/trainingjobs/remove', methods=['POST'])
# def remove_all_trainingjobs():
#     jobs = MetastoreFacade.list_training_jobs()
#     for job in jobs:
#         MonitorToolsController.stop_pid(job.pid)
#         MetastoreFacade.remove_training_job(training_job=job)
#     time.sleep(2)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/datacollectionjobs', methods=['GET'])
# def datacollectionjobs():
#     data_collection_jobs = MetastoreFacade.list_data_collection_jobs()
#     alive_jobs = []
#     for job in data_collection_jobs:
#         if EmulationUtil.check_pid(job.pid):
#             job.running = True
#         alive_jobs.append(job)
#     data_collection_jobs_dicts = list(map(lambda x: x.to_dict(), alive_jobs))
#     response = jsonify(data_collection_jobs_dicts)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/datacollectionjobsids', methods=['GET'])
# def datacollectionjobsids():
#     data_collection_jobs_ids = MetastoreFacade.list_data_collection_jobs_ids()
#     response_dicts = []
#     for tup in data_collection_jobs_ids:
#         response_dicts.append({
#             "id": tup[0],
#             "emulation": tup[1],
#             "running": EmulationUtil.check_pid(tup[2])
#         })
#     response = jsonify(response_dicts)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/datacollectionjobs/get/<job_id>', methods=['GET'])
# def get_data_collection_job(job_id: int):
#     job = MetastoreFacade.get_data_collection_job_config(id=job_id)
#     if job is not None:
#         if EmulationUtil.check_pid(job.pid):
#             job.running = True
#         response = jsonify(job.to_dict())
#     else:
#         response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/datacollectionjobs/stop/<job_id>', methods=['POST'])
# def stop_data_collection_job(job_id: int):
#     job = MetastoreFacade.get_data_collection_job_config(id=job_id)
#     if job is not None:
#         MonitorToolsController.stop_pid(job.pid)
#         time.sleep(2)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/datacollectionjobs/remove/<job_id>', methods=['POST'])
# def remove_data_collection_job(job_id: int):
#     job = MetastoreFacade.get_data_collection_job_config(id=job_id)
#     if job is not None:
#         MonitorToolsController.stop_pid(job.pid)
#         MetastoreFacade.remove_data_collection_job(data_collection_job=job)
#         time.sleep(2)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/datacollectionjobs/remove', methods=['POST'])
# def remove_all_data_collection_jobs():
#     jobs = MetastoreFacade.list_data_collection_jobs()
#     for job in jobs:
#         MonitorToolsController.stop_pid(job.pid)
#         MetastoreFacade.remove_data_collection_job(data_collection_job=job)
#     time.sleep(2)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/datacollectionjobs/start/<job_id>', methods=['POST'])
# def start_data_collection_job(job_id: int):
#     job = MetastoreFacade.get_data_collection_job_config(id=job_id)
#     if job is not None:
#         DataCollectionJobManager.start_data_collection_job_in_background(data_collection_job=job)
#         time.sleep(4)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/systemidentificationjobs', methods=['GET'])
# def system_identification_jobs():
#     system_identification_jbos = MetastoreFacade.list_system_identification_jobs()
#     alive_jobs = []
#     for job in system_identification_jbos:
#         if EmulationUtil.check_pid(job.pid):
#             job.running = True
#         alive_jobs.append(job)
#     system_identification_jobs_dicts = list(map(lambda x: x.to_dict(), alive_jobs))
#     response = jsonify(system_identification_jobs_dicts)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/systemidentificationjobsids', methods=['GET'])
# def system_identification_jobs_ids():
#     system_identification_jobs_ids = MetastoreFacade.list_system_identification_jobs_ids()
#     response_dicts = []
#     for tup in system_identification_jobs_ids:
#         response_dicts.append({
#             "id": tup[0],
#             "emulation": tup[1],
#             "running": EmulationUtil.check_pid(tup[2])
#         })
#     response = jsonify(response_dicts)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/systemidentificationjobs/get/<job_id>', methods=['GET'])
# def get_system_identification_job(job_id: int):
#     job = MetastoreFacade.get_system_identification_job_config(id=job_id)
#     if job is not None:
#         if EmulationUtil.check_pid(job.pid):
#             job.running = True
#         response = jsonify(job.to_dict())
#     else:
#         response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/systemidentificationjobs/stop/<job_id>', methods=['POST'])
# def stop_system_identification_job(job_id: int):
#     job = MetastoreFacade.get_system_identification_job_config(id=job_id)
#     if job is not None:
#         MonitorToolsController.stop_pid(job.pid)
#         time.sleep(2)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/systemidentificationjobs/remove/<job_id>', methods=['POST'])
# def remove_system_identification_job(job_id: int):
#     job = MetastoreFacade.get_system_identification_job_config(id=job_id)
#     if job is not None:
#         MonitorToolsController.stop_pid(job.pid)
#         MetastoreFacade.remove_system_identification_job(system_identification_job=job)
#         time.sleep(2)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/systemidentificationjobs/remove', methods=['POST'])
# def remove_all_system_identification_jobs():
#     jobs = MetastoreFacade.list_system_identification_jobs()
#     for job in jobs:
#         MonitorToolsController.stop_pid(job.pid)
#         MetastoreFacade.remove_system_identification_job(system_identification_job=job)
#     time.sleep(2)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response
#
# @app.route('/systemidentificationjobs/start/<job_id>', methods=['POST'])
# def start_system_identification_job(job_id: int):
#     job = MetastoreFacade.get_system_identification_job_config(id=job_id)
#     if job is not None:
#         SystemIdentificationJobManager.start_system_identification_job_in_background(system_identification_job=job)
#         time.sleep(4)
#     response = jsonify({})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response


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

