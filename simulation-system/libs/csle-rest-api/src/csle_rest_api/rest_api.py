from flask import Flask
from . import socketio
import csle_common.constants.constants as constants
from csle_common.logging.log import Logger
from csle_common.dao.emulation_config.config import Config
from csle_rest_api.pages.emulations.routes import get_emulations_page_bp
from csle_rest_api.pages.simulations.routes import get_simulations_page_bp
from csle_rest_api.pages.monitoring.routes import get_monitoring_page_bp
from csle_rest_api.pages.traces.routes import get_traces_page_bp
from csle_rest_api.pages.emulation_statistics.routes import get_emulation_statistics_page_bp
from csle_rest_api.pages.system_models.routes import get_system_models_page_bp
from csle_rest_api.pages.about.routes import get_about_page_bp
from csle_rest_api.pages.login.routes import get_login_page_bp
from csle_rest_api.pages.register.routes import get_register_page_bp
from csle_rest_api.pages.downloads.routes import get_downloads_page_bp
from csle_rest_api.pages.images.routes import get_images_page_bp
from csle_rest_api.pages.jobs.routes import get_jobs_page_bp
from csle_rest_api.pages.policies.routes import get_policies_page_bp
from csle_rest_api.pages.policy_examination.routes import get_policy_examination_page_bp
from csle_rest_api.pages.training.routes import get_training_page_bp
from csle_rest_api.pages.sdn_controllers.routes import get_sdn_controllers_page_bp
from csle_rest_api.pages.control_plane.routes import get_control_plane_page_bp
from csle_rest_api.pages.user_admin.routes import get_user_admin_page_bp
from csle_rest_api.pages.host_terminal.routes import get_host_terminal_page_bp
from csle_rest_api.pages.container_terminal.routes import get_container_terminal_page_bp
from csle_rest_api.pages.system_admin.routes import get_system_admin_page_bp
from csle_rest_api.pages.logs_admin.routes import get_logs_admin_page_bp
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
from csle_rest_api.resources.gaussian_mixture_system_models.routes import gaussian_mixture_system_models_bp
from csle_rest_api.resources.empirical_system_models.routes import empirical_system_models_bp
from csle_rest_api.resources.gp_system_models.routes import gp_system_models_bp
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
from csle_rest_api.resources.login.routes import login_bp
from csle_rest_api.resources.traces_datasets.routes import traces_datasets_bp
from csle_rest_api.resources.statistics_datasets.routes import statistics_datasets_bp
from csle_rest_api.resources.users.routes import users_bp
from csle_rest_api.resources.config.routes import config_bp
from csle_rest_api.resources.version.routes import version_bp
from csle_rest_api.resources.logs.routes import logs_bp
from csle_rest_api.web_sockets.host_terminal.host_terminal import get_host_terminal_bp
from csle_rest_api.web_sockets.container_terminal.container_terminal import get_container_terminal_bp
import csle_rest_api.constants.constants as api_constants


def create_app(static_folder: str):
    """
    Creates and initializes the Flask App

    :param static_folder: path to the folder to serve static resources
    :return: the flask app
    """
    app = Flask(__name__, static_url_path='', static_folder=static_folder)

    app.register_blueprint(get_emulations_page_bp(static_folder=f"../../{static_folder}"),
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.EMULATIONS_PAGE_RESOURCE}")
    app.register_blueprint(get_simulations_page_bp(static_folder=f"../../{static_folder}"),
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.SIMULATIONS_PAGE_RESOURCE}")
    app.register_blueprint(get_traces_page_bp(static_folder=f"../../{static_folder}"),
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.TRACES_PAGE_RESOURCE}")
    app.register_blueprint(get_monitoring_page_bp(static_folder=f"../../{static_folder}"),
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.MONITORING_PAGE_RESOURCE}")
    app.register_blueprint(get_emulation_statistics_page_bp(static_folder=f"../../{static_folder}"),
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_PAGE_RESOURCE}")
    app.register_blueprint(get_system_models_page_bp(static_folder=f"../../{static_folder}"),
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.SYSTEM_MODELS_PAGE_RESOURCE}")
    app.register_blueprint(get_about_page_bp(static_folder=f"../../{static_folder}"),
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.ABOUT_PAGE_RESOURCE}")
    app.register_blueprint(get_login_page_bp(static_folder=f"../../{static_folder}"),
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.LOGIN_PAGE_RESOURCE}")
    app.register_blueprint(get_downloads_page_bp(static_folder=f"../../{static_folder}"),
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.DOWNLOADS_PAGE_RESOURCE}")
    app.register_blueprint(cadvisor_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE}")
    app.register_blueprint(grafana_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.GRAFANA_RESOURCE}")
    app.register_blueprint(get_images_page_bp(static_folder=f"../../{static_folder}"),
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.IMAGES_PAGE_RESOURCE}")
    app.register_blueprint(get_jobs_page_bp(static_folder=f"../../{static_folder}"),
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.JOBS_PAGE_RESOURCE}")
    app.register_blueprint(node_exporter_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE}")
    app.register_blueprint(get_policies_page_bp(static_folder=f"../../{static_folder}"),
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.POLICIES_PAGE_RESOURCE}")
    app.register_blueprint(get_policy_examination_page_bp(static_folder=f"../../{static_folder}"),
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.POLICY_EXAMINATION_PAGE_RESOURCE}")
    app.register_blueprint(prometheus_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.PROMETHEUS_RESOURCE}")
    app.register_blueprint(get_training_page_bp(static_folder=f"../../{static_folder}"),
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.TRAINING_PAGE_RESOURCE}")
    app.register_blueprint(get_sdn_controllers_page_bp(static_folder=f"../../{static_folder}"),
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.SDN_CONTROLLERS_PAGE_RESOURCE}")
    app.register_blueprint(get_control_plane_page_bp(static_folder=f"../../{static_folder}"),
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.CONTROL_PLANE_PAGE_RESOURCE}")
    app.register_blueprint(get_user_admin_page_bp(static_folder=f"../../{static_folder}"),
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.USER_ADMIN_PAGE_RESOURCE}")
    app.register_blueprint(get_host_terminal_page_bp(static_folder=f"../../{static_folder}"),
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.HOST_TERMINAL_PAGE_RESOURCE}")
    app.register_blueprint(get_container_terminal_page_bp(static_folder=f"../../{static_folder}"),
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.CONTAINER_TERMINAL_PAGE_RESOURCE}")
    app.register_blueprint(get_system_admin_page_bp(static_folder=f"../../{static_folder}"),
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.SYSTEM_ADMIN_PAGE_RESOURCE}")
    app.register_blueprint(get_logs_admin_page_bp(static_folder=f"../../{static_folder}"),
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.LOGS_ADMIN_PAGE_RESOURCE}")
    app.register_blueprint(get_register_page_bp(static_folder=f"../../{static_folder}"),
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.REGISTER_PAGE_RESOURCE}")
    app.register_blueprint(emulations_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}")
    app.register_blueprint(emulation_executions_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}")
    app.register_blueprint(simulations_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}")
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
    app.register_blueprint(gaussian_mixture_system_models_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.GAUSSIAN_MIXTURE_SYSTEM_MODELS_RESOURCE}")
    app.register_blueprint(empirical_system_models_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}"),
    app.register_blueprint(gp_system_models_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.GP_SYSTEM_MODELS_RESOURCE}")
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
    app.register_blueprint(login_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.LOGIN_RESOURCE}")
    app.register_blueprint(sdn_controllers_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.SDN_CONTROLLERS_RESOURCE}"),
    app.register_blueprint(traces_datasets_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}")
    app.register_blueprint(statistics_datasets_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}")
    app.register_blueprint(users_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.USERS_RESOURCE}")
    app.register_blueprint(config_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.CONFIG_RESOURCE}")
    app.register_blueprint(version_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.VERSION_RESOURCE}")
    app.register_blueprint(logs_bp,
                           url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                      f"{api_constants.MGMT_WEBAPP.LOGS_RESOURCE}")
    web_sockets_host_terminal_bp = get_host_terminal_bp(app)
    app.register_blueprint(web_sockets_host_terminal_bp)
    web_sockets_container_terminal_bp = get_container_terminal_bp(app)
    app.register_blueprint(web_sockets_container_terminal_bp)

    @app.route(constants.COMMANDS.SLASH_DELIM, methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
    def root():
        """
        :return: the root page of the management application
        """
        return app.send_static_file(api_constants.MGMT_WEBAPP.STATIC_RESOURCE_INDEX)

    app.config[api_constants.MGMT_WEBAPP.HOST_TERMINAL_FD] = None
    app.config[api_constants.MGMT_WEBAPP.HOST_TERMINAL_CMD] = [constants.COMMANDS.BASH]
    app.config[api_constants.MGMT_WEBAPP.HOST_TERMINAL_CHILD_PID] = None
    socketio.init_app(app)
    return app


def start_server(static_folder: str, port: int = 7777, num_threads: int = 100, host: str = "0.0.0.0",
                 https: bool = False) -> None:
    """
    Creates the flask app and serves it

    :param static_folder: path to the folder to server static resources
    :param port: the port for serving
    :param num_threads: number of threads for serving
    :param host: the host string for serving
    :param https: boolean flag whether to use https or not

    :return: None
    """
    # from subprocess import run
    # run(f"gunicorn -b {host}:{port} 'csle_rest_api.rest_api:create_app() --workers 4 --threads
    # {num_threads}'".split(' '))
    # gunicorn -b 0.0.0.0:5000 --workers 4 --threads num_threads module:app
    Config.set_config_parameters_from_config_file()
    Logger.__call__().get_logger().info(f"Starting web server, listening on port: {port}")
    app = create_app(static_folder=static_folder)
    socketio.run(app, debug=False, port=port, host=host)
