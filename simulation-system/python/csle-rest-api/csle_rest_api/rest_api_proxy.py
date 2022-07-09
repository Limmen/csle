from flask import Flask
from waitress import serve
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

    @app.route(f'/{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}')
    def emulations_proxy():
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
               f'{constants.COMMANDS.SLASH_DELIM}<emulation_id>')
    def emulation_proxy(emulation_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{emulation_id}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
               f'{constants.COMMANDS.SLASH_DELIM}<emulation_id>{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}')
    def executions_of_emulation_proxy(emulation_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{emulation_id}{constants.COMMANDS.SLASH_DELIM}'
                   f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
               f'{constants.COMMANDS.SLASH_DELIM}<emulation_id>{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}{constants.COMMANDS.SLASH_DELIM}<execution_id>')
    def execution_of_emulation_proxy(emulation_id: int, execution_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{emulation_id}{constants.COMMANDS.SLASH_DELIM}'
                   f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}{constants.COMMANDS.SLASH_DELIM}'
                   f'{execution_id}').content

    @app.route(f'/{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
               f'{constants.COMMANDS.SLASH_DELIM}<emulation_id>{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}{constants.COMMANDS.SLASH_DELIM}<execution_id>'
               f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.MONITOR_SUBRESOURCE}'
               f'{constants.COMMANDS.SLASH_DELIM}<minutes>')
    def monitor_emulation_proxy(emulation_id: int, execution_id: int, minutes: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{emulation_id}{constants.COMMANDS.SLASH_DELIM}'
                   f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}{constants.COMMANDS.SLASH_DELIM}'
                   f'{execution_id}{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.MONITOR_SUBRESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{minutes}').content


    @app.route(f'/{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
               f'{constants.COMMANDS.SLASH_DELIM}<emulation_id>{constants.COMMANDS.SLASH_DELIM}'
               f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}{constants.COMMANDS.SLASH_DELIM}<execution_id>'
               f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.SWITCHES_SUBRESOURCE}')
    def sdn_switches_of_execution_proxy(emulation_id: int, execution_id: int):
        return get(f'{proxy_server}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}'
                   f'{constants.COMMANDS.SLASH_DELIM}{emulation_id}{constants.COMMANDS.SLASH_DELIM}'
                   f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}{constants.COMMANDS.SLASH_DELIM}'
                   f'{execution_id}{constants.COMMANDS.SLASH_DELIM}'
                   f'{api_constants.MGMT_WEBAPP.SWITCHES_SUBRESOURCE}').content

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