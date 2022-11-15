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
from csle_rest_api.pages.login.routes import login_page_bp
from csle_rest_api.pages.downloads.routes import downloads_page_bp
from csle_rest_api.pages.images.routes import images_page_bp
from csle_rest_api.pages.jobs.routes import jobs_page_bp
from csle_rest_api.pages.policies.routes import policies_page_bp
from csle_rest_api.pages.policy_examination.routes import policy_examination_page_bp
from csle_rest_api.pages.training.routes import training_page_bp
from csle_rest_api.pages.sdn_controllers.routes import sdn_controllers_page_bp
from csle_rest_api.pages.control_plane.routes import control_plane_page_bp
from csle_rest_api.pages.admin.routes import admin_page_bp


def create_app(static_folder: str, proxy_server: str):
    """
    Creates and initializes the Flask App Proxy server

    :param static_folder: path to the folder to serve static resources
    :param proxy_server: proxy server
    :return: the flask app
    """
    # Create the app
    app = Flask(__name__, static_url_path='', static_folder=static_folder)

    # Register blueprints (sub-applications) to serve static resources
    app.register_blueprint(emulations_page_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.EMULATIONS_PAGE_RESOURCE}")
    app.register_blueprint(simulations_page_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.SIMULATIONS_PAGE_RESOURCE}")
    app.register_blueprint(traces_page_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.TRACES_PAGE_RESOURCE}")
    app.register_blueprint(monitoring_page_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.MONITORING_PAGE_RESOURCE}")
    app.register_blueprint(emulation_statistics_page_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_PAGE_RESOURCE}")
    app.register_blueprint(system_models_page_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.SYSTEM_MODELS_PAGE_RESOURCE}")
    app.register_blueprint(about_page_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.ABOUT_PAGE_RESOURCE}")
    app.register_blueprint(login_page_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.LOGIN_PAGE_RESOURCE}")
    app.register_blueprint(downloads_page_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.DOWNLOADS_PAGE_RESOURCE}")
    app.register_blueprint(images_page_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.IMAGES_PAGE_RESOURCE}")
    app.register_blueprint(jobs_page_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.JOBS_PAGE_RESOURCE}")
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
    app.register_blueprint(control_plane_page_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.CONTROL_PLANE_PAGE_RESOURCE}")
    app.register_blueprint(admin_page_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.ADMIN_PAGE_RESOURCE}")

    # Root route
    @app.route(constants.COMMANDS.SLASH_DELIM, methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
    def root():
        return app.send_static_file(api_constants.MGMT_WEBAPP.STATIC_RESOURCE_INDEX)

    # Specify proxy routes
    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                        api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def emulations_proxy():
        """
        Proxy for the /emulations resource

        :return: the /emulations resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}?ids=true&token={token}').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}?token={token}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
               f'{constants.COMMANDS.SLASH_DELIM}<emulation_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                        api_constants.MGMT_WEBAPP.HTTP_REST_DELETE,
                        api_constants.MGMT_WEBAPP.HTTP_REST_POST])
    def emulation_proxy(emulation_id: int):
        """
        Proxy for the /emulations/emulation_id resource

        :return: the /emulation/emulation_id resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{emulation_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{emulation_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
            return post(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
                          f'{constants.COMMANDS.SLASH_DELIM}{emulation_id}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
               f'{constants.COMMANDS.SLASH_DELIM}<emulation_id>{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                        api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def executions_of_emulation_proxy(emulation_id: int):
        """
        Proxy for the /emulations/emulation_id/executions resource

        :return: the /emulations/emulation_id/executions resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{emulation_id}{constants.COMMANDS.SLASH_DELIM}'
                       f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{emulation_id}{constants.COMMANDS.SLASH_DELIM}'
                       f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
               f'{constants.COMMANDS.SLASH_DELIM}<emulation_id>{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}{constants.COMMANDS.SLASH_DELIM}<execution_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def execution_of_emulation_proxy(emulation_id: int, execution_id: int):
        """
        Proxy for the /emulations/emulation_id/executions/execution_id resource

        :return: the /emulations/emulation_id/executions/execution_id resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{emulation_id}{constants.COMMANDS.SLASH_DELIM}'
                       f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}{constants.COMMANDS.SLASH_DELIM}'
                       f'{execution_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{emulation_id}{constants.COMMANDS.SLASH_DELIM}'
                       f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}{constants.COMMANDS.SLASH_DELIM}'
                       f'{execution_id}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
               f'{constants.COMMANDS.SLASH_DELIM}<emulation_id>{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}{constants.COMMANDS.SLASH_DELIM}<execution_id>'
               f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.MONITOR_SUBRESOURCE}'
               f'{constants.COMMANDS.SLASH_DELIM}<minutes>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
    def monitor_emulation_proxy(emulation_id: int, execution_id: int, minutes: int):
        """
        Proxy for the /emulations/emulation_id/executions/execution_id/monitor/minutes resource

        :return: the /emulations/emulation_id/executions/execution_id/monitor/minutes resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        res =  get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{emulation_id}{constants.COMMANDS.SLASH_DELIM}'
                   f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}{constants.COMMANDS.SLASH_DELIM}'
                   f'{execution_id}{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.MONITOR_SUBRESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{minutes}?token={token}').content
        return res


    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
               f'{constants.COMMANDS.SLASH_DELIM}<emulation_id>{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}{constants.COMMANDS.SLASH_DELIM}<execution_id>'
               f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.SWITCHES_SUBRESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
    def sdn_switches_of_execution_proxy(emulation_id: int, execution_id: int):
        """
        Proxy for the /emulations/emulation_id/executions/execution_id/switches resource

        :return: the /emulations/emulation_id/executions/execution_id/switches resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{emulation_id}{constants.COMMANDS.SLASH_DELIM}'
                   f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}{constants.COMMANDS.SLASH_DELIM}'
                   f'{execution_id}{constants.COMMANDS.SLASH_DELIM}'
                   f'{api_constants.MGMT_WEBAPP.SWITCHES_SUBRESOURCE}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.ALPHA_VEC_POLICIES_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,  api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def alpha_vec_policies_proxy():
        """
        Proxy for the /alpha-vec-policies resource

        :return: the /alpha-vec-policies
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.ALPHA_VEC_POLICIES_RESOURCE}'
                       f'?ids=true&token={token}').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.ALPHA_VEC_POLICIES_RESOURCE}'
                           f'?token={token}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.ALPHA_VEC_POLICIES_RESOURCE}'
                              f'?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.ALPHA_VEC_POLICIES_RESOURCE}{constants.COMMANDS.SLASH_DELIM}<policy_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def alpha_vec_policy_proxy(policy_id: int):
        """
        Proxy for the /alpha-vec-policies/policy_id resource

        :return: the /alpha-vec-policies/policy_id
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.ALPHA_VEC_POLICIES_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{policy_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.ALPHA_VEC_POLICIES_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{policy_id}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_POST])
    def cadvisor_proxy():
        """
        Proxy for the /cadvisor resource

        :return: the /cadvisor resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
            return post(f'{proxy_server}{api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.PROMETHEUS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_POST])
    def prometheus_proxy():
        """
        Proxy for the /prometheus resource

        :return: the /prometheus
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.PROMETHEUS_RESOURCE}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
            return post(f'{proxy_server}{api_constants.MGMT_WEBAPP.PROMETHEUS_RESOURCE}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_POST])
    def nodeexporter_proxy():
        """
        Proxy for the /nodeexporter resource

        :return: the /nodeexporter resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.GRAFANA_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_POST])
    def grafana_proxy():
        """
        Proxy for the /grafana resource

        :return: the /grafana resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.GRAFANA_RESOURCE}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
            return post(f'{proxy_server}{api_constants.MGMT_WEBAPP.GRAFANA_RESOURCE}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def data_collection_jobs_proxy():
        """
        Proxy for the /data-collection-jobs resource

        :return: the /data-collection-jobs resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}'
                       f'?ids=true&oken={token}').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}'
                           f'?token={token}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}'
                              f'?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}{constants.COMMANDS.SLASH_DELIM}<job_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def data_collection_job_proxy(job_id: int):
        """
        Proxy for the /data-collections-jobs/job_id resource

        :return: the /data-collections-jobs/job_id resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{job_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{job_id}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def dqn_policies_proxy():
        """
        Proxy for the /dqn-policies resource

        :return: the /dqn-policies resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE}?ids=true').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE}?token={token}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE}'
               f'{constants.COMMANDS.SLASH_DELIM}<policy_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def dqn_policy_proxy(policy_id: int):
        """
        Proxy for the /dqn-policies/policy-id resource

        :return: the /dqn-policies/policy-id resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{policy_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{policy_id}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def fnn_w_softmax_policies_proxy():
        """
        Proxy for the /fnn-w-softmax-policies resource

        :return: the /fnn-w-softmax-policies resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE}'
                       f'?ids=true&token={token}').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE}'
                           f'?token={token}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE}'
                              f'?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE}{constants.COMMANDS.SLASH_DELIM}<policy_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def fnn_w_softmax_policy_proxy(policy_id: int):
        """
        Proxy for the /fnn-w-softmax-policies/policy_id resource

        :return: the /fnn-w-softmax-policies/policy_id resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{policy_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{policy_id}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def ppo_policies_proxy():
        """
        Proxy for the /ppo-policies resource

        :return: the /ppo-policies resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}'
                       f'?ids=true&token={token}').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}'
                           f'?token={token}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}'
                              f'?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}'
               f'{constants.COMMANDS.SLASH_DELIM}<policy_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def ppo_policy_proxy(policy_id: int):
        """
        Proxy for the /ppo-policies/policy_id resource

        :return: the /ppo-policies/policy_id resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{policy_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{policy_id}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def tabular_policies_proxy():
        """
        Proxy for the /tabular-policies resource

        :return: the /tabular-policies resource
        """
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE}?ids=true&token={token}').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE}'
                           f'?token={token}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE}'
                              f'?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE}{constants.COMMANDS.SLASH_DELIM}<policy_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def tabular_policy_proxy(policy_id: int):
        """
        Proxy for the /tabular-policies/policy_id resource

        :return: the /tabular-policies/policy_id resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{policy_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{policy_id}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def vector_policies_proxy():
        """
        Proxy for the /vector-policies resource

        :return: the /vector-policies resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE}'
                       f'?ids=true&token={token}').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE}'
                           f'?token={token}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE}'
                              f'?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE}{constants.COMMANDS.SLASH_DELIM}<policy_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def vector_policy_proxy(policy_id: int):
        """
        Proxy for the /vector-policies/policy_id resource

        :return: the /vector-policies/policy_id resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{policy_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{policy_id}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def multi_threshold_policies_proxy():
        """
        Proxy for the /multi-threshold-policies resource

        :return: the /multi-threshold-policies resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE}'
                       f'?ids=true&token={token}').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE}'
                           f'?token={token}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE}'
                              f'?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE}{constants.COMMANDS.SLASH_DELIM}<policy_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def multi_threshold_policy_proxy(policy_id: int):
        """
        Proxy for the /multi-threshold-policies/policy_id resource

        :return: the /multi-threshold-policies/policy_id resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{policy_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{policy_id}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def training_jobs_proxy():
        """
        Proxy for the /training-jobs resource

        :return: the /training-jobs resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}'
                       f'?ids=true&token={token}').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}'
                           f'?token={token}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}'
                              f'?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}{constants.COMMANDS.SLASH_DELIM}<job_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def training_job_proxy(job_id: int):
        """
        Proxy for the /training-jobs/job_id resource

        :return: the /training-jobs/job_id resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{job_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{job_id}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def system_identification_jobs_proxy():
        """
        Proxy for the /system-identification-jobs resource

        :return: the /system-identification-jobs resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}'
                       f'?ids=true&token={token}').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}'
                           f'?token={token}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}'
                              f'?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}{constants.COMMANDS.SLASH_DELIM}<job_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def system_identification_job_proxy(job_id: int):
        """
        Proxy for the /system-identification-jobs/job_id resource

        :return: the /system-identification-jobs/job_id resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{job_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{job_id}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
    def emulation_executions_proxy():
        """
        Proxy for the /emulation-executions resource

        :return: the /emulation-executions resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}'
                       f'?ids=true&token={token}').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}'
                           f'?token={token}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}'
                              f'?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}{constants.COMMANDS.SLASH_DELIM}'
               f'<execution_id>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
    def emulation_execution_proxy(execution_id: int):
        """
        Proxy for the /emulation-executions/execution_id resource

        :return: the /emulation-executions/execution_id resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
        if emulation is not None:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{execution_id}?'
                       f'{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}={emulation}&token={token}').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{execution_id}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.EMULATION_SIMULATION_TRACES_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def emulation_simulation_traces_proxy():
        """
        Proxy for the /emulation-simulation-traces resource

        :return: the /emulation-simulation-traces resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_SIMULATION_TRACES_RESOURCE}'
                       f'?ids=true&token={token}').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_SIMULATION_TRACES_RESOURCE}'
                           f'?token={token}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_SIMULATION_TRACES_RESOURCE}'
                              f'?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.EMULATION_SIMULATION_TRACES_RESOURCE}{constants.COMMANDS.SLASH_DELIM}'
               f'<trace_id>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                       api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def emulation_simulation_trace_proxy(trace_id: int):
        """
        Proxy for the /emulation-simulation-traces/trace_id resource

        :return: the /emulation-simulation-traces/trace_id resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_SIMULATION_TRACES_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{trace_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_SIMULATION_TRACES_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{trace_id}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def emulation_statistics_proxy():
        """
        Proxy for the /emulation-statistics resource

        :return: the /emulation-statistics resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}'
                       f'?ids=true&token={token}').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}'
                           f'?token={token}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}'
                              f'?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}{constants.COMMANDS.SLASH_DELIM}'
               f'<statistics_id>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                            api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def emulation_statistic_proxy(statistics_id: int):
        """
        Proxy for the /emulation-statistics/statistics_id resource

        :return: the /emulation-statistics/statistics_id resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{statistics_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{statistics_id}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def emulation_traces_proxy():
        """
        Proxy for the /emulation-traces resource

        :return: the /emulation-traces resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}'
                       f'?ids=true&token={token}').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}'
                           f'?token={token}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}'
                              f'?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}{constants.COMMANDS.SLASH_DELIM}'
               f'<trace_id>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                       api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def emulation_trace_proxy(trace_id: int):
        """
        Proxy for the /emulation-traces/trace_id resource

        :return: the /emulation-traces/trace_id resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{trace_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATION_TRACES_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{trace_id}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def simulation_traces_proxy():
        """
        Proxy for the /simulation-traces resource

        :return: the /simulation-traces resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}'
                       f'?ids=true&token={token}').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}'
                           f'?token={token}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}'
                              f'?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}{constants.COMMANDS.SLASH_DELIM}'
               f'<trace_id>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                       api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def simulation_trace_proxy(trace_id: int):
        """
        Proxy for the /simulation-traces/trace_id resource

        :return: the /simulation-traces/trace_id resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{trace_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{trace_id}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def experiments_proxy():
        """
        Proxy for the /experiments resource

        :return: the /experiments resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}'
                       f'?ids=true&token={token}').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}'
                           f'?token={token}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}'
                              f'?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}{constants.COMMANDS.SLASH_DELIM}'
               f'<experiment_id>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                            api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def experiment_proxy(experiment_id: int):
        """
        Proxy for the /experiments/experiment_id resource

        :return: the /experiments/experiment_id resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{experiment_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{experiment_id}?token={token}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.FILE_RESOURCE}', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
    def fileproxy():
        """
        Proxy for the /file resournce

        :return: the /file resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        post_json_data = json.loads(request.data)
        headers = {api_constants.MGMT_WEBAPP.CONTENT_TYPE_HEADER: api_constants.MGMT_WEBAPP.APPLICATION_JSON_DATA_TYPE,
                   api_constants.MGMT_WEBAPP.ACCEPT_HEADER: api_constants.MGMT_WEBAPP.APPLICATION_JSON_DATA_TYPE}
        return post(f'{proxy_server}{api_constants.MGMT_WEBAPP.FILE_RESOURCE}',
                   json=post_json_data, headers=headers).content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.IMAGES_RESOURCE}', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
    def images_proxy():
        """
        Proxy for the /images resource

        :return: the /images resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.IMAGES_RESOURCE}?ids=true&token={token}').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.IMAGES_RESOURCE}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.SDN_CONTROLLERS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
    def sdn_controllers_proxy():
        """
        Proxy for the /sdn-controllers resource

        :return: the /sdn-controllers resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SDN_CONTROLLERS_RESOURCE}'
                       f'?ids=true&token={token}').content
        else:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SDN_CONTROLLERS_RESOURCE}?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def simulations_proxy():
        """
        Proxy for the /simulations resource

        :return: the /simulations resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}?ids=true&token={token}').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}'
                           f'?token={token}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}'
                              f'?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}{constants.COMMANDS.SLASH_DELIM}'
               f'<simulation_id>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                            api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def simulation_proxy(simulation_id: int):
        """
        Proxy for the /simulations/simulation_id resource

        :return: the /simulations/simulation_id resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{simulation_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{simulation_id}?token={token}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.GAUSSIAN_MIXTURE_SYSTEM_MODELS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def gaussian_mixture_system_models_proxy():
        """
        Proxy for the /gaussian-mixture-system-models resource

        :return: the /system-models resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}'
                       f'{api_constants.MGMT_WEBAPP.GAUSSIAN_MIXTURE_SYSTEM_MODELS_RESOURCE}'
                       f'?ids=true&token={token}').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}'
                           f'{api_constants.MGMT_WEBAPP.GAUSSIAN_MIXTURE_SYSTEM_MODELS_RESOURCE}'
                           f'?token={token}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}'
                              f'{api_constants.MGMT_WEBAPP.GAUSSIAN_MIXTURE_SYSTEM_MODELS_RESOURCE}'
                              f'?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.GAUSSIAN_MIXTURE_SYSTEM_MODELS_RESOURCE}{constants.COMMANDS.SLASH_DELIM}'
               f'<system_model_id>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                              api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def gaussian_mixture_system_model_proxy(system_model_id: int):
        """
        Proxy for the /gaussian-mixture-system-models/system_model_id resource

        :return: the /gaussian-mixture-system-models/system_model_id resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.GAUSSIAN_MIXTURE_SYSTEM_MODELS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{system_model_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.GAUSSIAN_MIXTURE_SYSTEM_MODELS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{system_model_id}?token={token}').content


    @app.route(f'/{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def empirical_system_models_proxy():
        """
        Proxy for the /empirical-system-models resource

        :return: the /system-models resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}'
                       f'?ids=true&token={token}').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}'
                           f'?token={token}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}'
                              f'?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}{constants.COMMANDS.SLASH_DELIM}'
               f'<system_model_id>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                              api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def empirical_system_model_proxy(system_model_id: int):
        """
        Proxy for the /empirical-system-models/system_model_id resource

        :return: the /empirical-system-models/system_model_id resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{system_model_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}'
                          f'{constants.COMMANDS.SLASH_DELIM}{system_model_id}?token={token}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.GP_SYSTEM_MODELS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def gp_system_models_proxy():
        """
        Proxy for the /gp-system-models resource

        :return: the /system-models resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.GP_SYSTEM_MODELS_RESOURCE}'
                       f'?ids=true&token={token}').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.GP_SYSTEM_MODELS_RESOURCE}'
                           f'?token={token}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.GP_SYSTEM_MODELS_RESOURCE}'
                              f'?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.GP_SYSTEM_MODELS_RESOURCE}{constants.COMMANDS.SLASH_DELIM}'
               f'<system_model_id>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                              api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def gp_system_model_proxy(system_model_id: int):
        """
        Proxy for the /gp-system-models/system_model_id resource

        :return: the /gp-system-models/system_model_id resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.GP_SYSTEM_MODELS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{system_model_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.GP_SYSTEM_MODELS_RESOURCE}'
                          f'{constants.COMMANDS.SLASH_DELIM}{system_model_id}?token={token}').content


    @app.route(f'/{api_constants.MGMT_WEBAPP.LOGIN_RESOURCE}', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
    def login_proxy():
        """
        Proxy for the /login resournce

        :return: the /login resource
        """
        post_json_data = json.loads(request.data)
        headers = {api_constants.MGMT_WEBAPP.CONTENT_TYPE_HEADER: api_constants.MGMT_WEBAPP.APPLICATION_JSON_DATA_TYPE,
                   api_constants.MGMT_WEBAPP.ACCEPT_HEADER: api_constants.MGMT_WEBAPP.APPLICATION_JSON_DATA_TYPE}
        return post(f'{proxy_server}{api_constants.MGMT_WEBAPP.LOGIN_RESOURCE}',
                    json=post_json_data, headers=headers).content


    @app.route(f'/{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def traces_datasets_proxy():
        """
        Proxy for the /traces-datasets resource

        :return: the /traces-datasets resource
        """
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}?ids=true').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}{constants.COMMANDS.SLASH_DELIM}'
               f'<traces_dataset_id>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                              api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def traces_dataset_proxy(traces_dataset_id: int):
        """
        Proxy for the /traces-datasets/<traces_dataset_id> resource

        :return: the /traces-datasets/<traces_dataset_id> resource
        """
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{traces_dataset_id}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}'
                          f'{constants.COMMANDS.SLASH_DELIM}{traces_dataset_id}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def statistics_datasets_proxy():
        """
        Proxy for the /statistics-datasets resource

        :return: the /statistics-datasets resource
        """
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}?ids=true').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}').content


    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}{constants.COMMANDS.SLASH_DELIM}'
               f'<statistics_dataset_id>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                                api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def statistics_dataset_proxy(statistics_dataset_id: int):
        """
        Proxy for the /statistics-datasets/<statistics_dataset_id> resource

        :return: the /statistics-datasets/<statistics_dataset_id> resource
        """
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{statistics_dataset_id}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}'
                          f'{constants.COMMANDS.SLASH_DELIM}{statistics_dataset_id}').content


    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.USERS_RESOURCE}',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def users_proxy():
        """
        Proxy for the /users resource

        :return: the /users resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.USERS_RESOURCE}'
                       f'?ids=true&token={token}').content
        else:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
                return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.USERS_RESOURCE}'
                           f'?token={token}').content
            elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
                return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.USERS_RESOURCE}'
                              f'?token={token}').content

    @app.route(f'{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.USERS_RESOURCE}{constants.COMMANDS.SLASH_DELIM}<user_id>',
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
    def user_proxy(user_id: int):
        """
        Proxy for the /users/user_id resource

        :return: the /users/user_id resource
        """
        token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
        if token is None:
            token = -1
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.USERS_RESOURCE}'
                       f'{constants.COMMANDS.SLASH_DELIM}{user_id}?token={token}').content
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            return delete(f'{proxy_server}{api_constants.MGMT_WEBAPP.USERS_RESOURCE}'
                          f'{constants.COMMANDS.SLASH_DELIM}{user_id}?token={token}').content

    return app


def start_proxy_server(static_folder: str, port: int = 7777, proxy_server: str = "http://172.31.212.92:7777/",
                       num_threads: int = 100, host: str = "0.0.0.0", https: bool = False) -> None:
    """
    Creates the flask app and serves it

    :param static_folder: path to the folder to server static resources
    :param port: the port for serving
    :param num_threads: number of threads for serving
    :param host: the host string for serving
    :param proxy_server: the proxy server
    :param https: boolean flag whether to use https or not

    :return: None
    """
    app = create_app(static_folder=static_folder, proxy_server=proxy_server)
    if not https:
        serve(app, host=host, port=port, threads=num_threads)
    else:
        serve(app, host=host, port=port, threads=num_threads, url_scheme='https')