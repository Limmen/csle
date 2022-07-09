from flask import Flask, request
from waitress import serve
from requests import get, post, delete
import json
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


def create_app(static_folder: str, proxy_server: str):
    """
    Creates and initializes the Flask App

    :param static_folder: path to the folder to serve static resources
    :param proxy_server: proxy server
    :return: the flask app
    """
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

    @app.route(constants.COMMANDS.SLASH_DELIM, methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
    def root():
        return app.send_static_file(api_constants.MGMT_WEBAPP.STATIC_RESOURCE_INDEX)

    @app.route(f'/{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                                                             api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def emulations_proxy():
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}?ids=true').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
               f'{constants.COMMANDS.SLASH_DELIM}<emulation_id>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                                                           api_constants.MGMT_WEBAPP.HTTP_REST_DELETE,
                                                                           api_constants.MGMT_WEBAPP.HTTP_REST_POST])
    def emulation_proxy(emulation_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{emulation_id}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
               f'{constants.COMMANDS.SLASH_DELIM}<emulation_id>{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                                                               api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def executions_of_emulation_proxy(emulation_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{emulation_id}{constants.COMMANDS.SLASH_DELIM}'
                   f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
               f'{constants.COMMANDS.SLASH_DELIM}<emulation_id>{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}{constants.COMMANDS.SLASH_DELIM}<execution_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def execution_of_emulation_proxy(emulation_id: int, execution_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{emulation_id}{constants.COMMANDS.SLASH_DELIM}'
                   f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}{constants.COMMANDS.SLASH_DELIM}'
                   f'{execution_id}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
               f'{constants.COMMANDS.SLASH_DELIM}<emulation_id>{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}{constants.COMMANDS.SLASH_DELIM}<execution_id>'
               f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.MONITOR_SUBRESOURCE}'
               f'{constants.COMMANDS.SLASH_DELIM}<minutes>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
    def monitor_emulation_proxy(emulation_id: int, execution_id: int, minutes: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{emulation_id}{constants.COMMANDS.SLASH_DELIM}'
                   f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}{constants.COMMANDS.SLASH_DELIM}'
                   f'{execution_id}{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.MONITOR_SUBRESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{minutes}').content


    @app.route(f'/{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
               f'{constants.COMMANDS.SLASH_DELIM}<emulation_id>{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}{constants.COMMANDS.SLASH_DELIM}<execution_id>'
               f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.SWITCHES_SUBRESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
    def sdn_switches_of_execution_proxy(emulation_id: int, execution_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{emulation_id}{constants.COMMANDS.SLASH_DELIM}'
                   f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}{constants.COMMANDS.SLASH_DELIM}'
                   f'{execution_id}{constants.COMMANDS.SLASH_DELIM}'
                   f'{api_constants.MGMT_WEBAPP.SWITCHES_SUBRESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.ALPHA_VEC_POLICIES_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,  api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def alpha_vec_policies_proxy():
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.ALPHA_VEC_POLICIES_RESOURCE}?ids=true').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.ALPHA_VEC_POLICIES_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.ALPHA_VEC_POLICIES_RESOURCE}{constants.COMMANDS.SLASH_DELIM}<policy_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def alpha_vec_policy_proxy(policy_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.ALPHA_VEC_POLICIES_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{policy_id}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE}', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                                                           api_constants.MGMT_WEBAPP.HTTP_REST_POST])
    def cadvisor_proxy():
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.PROMETHEUS_RESOURCE}', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                                                             api_constants.MGMT_WEBAPP.HTTP_REST_POST])
    def prometheus_proxy():
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.PROMETHEUS_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_POST])
    def nodeexporter_proxy():
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.GRAFANA_RESOURCE}', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                                                          api_constants.MGMT_WEBAPP.HTTP_REST_POST])
    def grafana_proxy():
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.GRAFANA_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def data_collection_jobs_proxy():
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}?ids=true').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}{constants.COMMANDS.SLASH_DELIM}<job_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def data_collection_job_proxy(job_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{job_id}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def dqn_policies_proxy():
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE}?ids=true').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE}{constants.COMMANDS.SLASH_DELIM}<policy_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def dqn_policy_proxy(policy_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{policy_id}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def fnn_w_softmax_policies_proxy():
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE}?ids=true').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE}{constants.COMMANDS.SLASH_DELIM}<policy_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def fnn_w_softmax_policy_proxy(policy_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{policy_id}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def ppo_policies_proxy():
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}?ids=true').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}{constants.COMMANDS.SLASH_DELIM}<policy_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def ppo_policy_proxy(policy_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{policy_id}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def tabular_policies_proxy():
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE}?ids=true').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE}{constants.COMMANDS.SLASH_DELIM}<policy_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def tabular_policy_proxy(policy_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{policy_id}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def vector_policies_proxy():
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE}?ids=true').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE}{constants.COMMANDS.SLASH_DELIM}<policy_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def vector_policy_proxy(policy_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{policy_id}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def multi_threshold_policies_proxy():
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE}?ids=true').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE}{constants.COMMANDS.SLASH_DELIM}<policy_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def multi_threshold_policy_proxy(policy_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{policy_id}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def training_jobs_proxy():
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}?ids=true').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}{constants.COMMANDS.SLASH_DELIM}<job_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def training_job_proxy(job_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{job_id}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def system_identification_jobs_proxy():
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}?ids=true').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}{constants.COMMANDS.SLASH_DELIM}<job_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def system_identification_job_proxy(job_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{job_id}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def emulation_executions_proxy():
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}?ids=true').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}{constants.COMMANDS.SLASH_DELIM}'
               f'<execution_id>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                           api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def emulation_execution_proxy(execution_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{execution_id}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.EMULATION_SIMULATION_TRACES_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def emulation_simulation_traces_proxy():
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_SIMULATION_TRACES_RESOURCE}?ids=true').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_SIMULATION_TRACES_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.EMULATION_SIMULATION_TRACES_RESOURCE}{constants.COMMANDS.SLASH_DELIM}'
               f'<trace_id>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                       api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def emulation_simulation_trace_proxy(trace_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_SIMULATION_TRACES_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{trace_id}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def emulation_statistics_proxy():
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}?ids=true').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}{constants.COMMANDS.SLASH_DELIM}'
               f'<statistics_id>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                            api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def emulation_statistic_proxy(statistics_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{statistics_id}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def emulation_traces_proxy():
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}?ids=true').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}{constants.COMMANDS.SLASH_DELIM}'
               f'<trace_id>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                       api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def emulation_trace_proxy(trace_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{trace_id}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def simulation_traces_proxy():
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}?ids=true').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}{constants.COMMANDS.SLASH_DELIM}'
               f'<trace_id>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                       api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def simulation_trace_proxy(trace_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{trace_id}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def experiments_proxy():
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}?ids=true').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}{constants.COMMANDS.SLASH_DELIM}'
               f'<experiment_id>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                            api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def experiment_proxy(experiment_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{experiment_id}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.FILE_RESOURCE}', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
    def fileproxy():
        # path = json.loads(request.data)[api_constants.MGMT_WEBAPP.PATH_PROPERTY]
        res = post(f'{proxy_server}{api_constants.MGMT_WEBAPP.FILE_RESOURCE}', json=request.data).content
        print(f"returning:{res}")
        return res
        # return post(f'{proxy_server}{api_constants.MGMT_WEBAPP.FILE_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.IMAGES_RESOURCE}', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
    def images_proxy():
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.IMAGES_RESOURCE}?ids=true').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.IMAGES_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.SDN_CONTROLLERS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
    def sdn_controllers_proxy():
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SDN_CONTROLLERS_RESOURCE}?ids=true').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SDN_CONTROLLERS_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def simulations_proxy():
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}?ids=true').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}{constants.COMMANDS.SLASH_DELIM}'
               f'<simulation_id>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                            api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def simulation_proxy(simulation_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{simulation_id}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.SYSTEM_MODELS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def system_models_proxy():
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SYSTEM_MODELS_RESOURCE}?ids=true').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SYSTEM_MODELS_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.SYSTEM_MODELS_RESOURCE}{constants.COMMANDS.SLASH_DELIM}'
               f'<system_model_id>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                              api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def system_model_proxy(system_model_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SYSTEM_MODELS_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{system_model_id}').content

    return app


def start_proxy_server(static_folder: str, port: int = 7777, proxy_server: str = "http://172.31.212.92:7777/",
                       num_threads: int = 100, host: str = "0.0.0.0") -> None:
    """
    Creates the flasp app and serves it

    :param static_folder: path to the folder to server static resources
    :param port: the port for serving
    :param num_threads: number of threads for serving
    :param host: the host string for serving
    :param proxy_server: the proxy server

    :return: None
    """
    app = create_app(static_folder=static_folder, proxy_server=proxy_server)
    serve(app, host=host, port=port, threads=num_threads)