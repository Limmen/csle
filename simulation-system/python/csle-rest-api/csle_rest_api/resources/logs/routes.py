"""
Routes and sub-resources for the /logs resource
"""
from flask import Blueprint, jsonify, request
import os
import subprocess
import json
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util
from csle_common.dao.emulation_config.config import Config
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.util.emulation_util import EmulationUtil


# Creates a blueprint "sub application" of the main REST app
logs_bp = Blueprint(
    api_constants.MGMT_WEBAPP.LOGS_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.LOGS_RESOURCE}")


@logs_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def logs():
    """
    The /logs resource.

    :return: List of log files in the CSLE logging directory
    """

    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized

    config = Config.get_current_confg()
    path = config.default_log_dir
    log_files = []
    for f in os.listdir(path):
        log_files.append(os.path.join(path, f))
    data = log_files
    data_dict = {api_constants.MGMT_WEBAPP.LOGS_PROPERTY: data}
    response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.DOCKER_STATS_MANAGER_SUBRESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def docker_stats_manager_logs():
    """
    The /logs/docker-stats-manager resource.

    :return: The logs of the docker stats manager
    """

    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized

    config = Config.get_current_confg()
    path = config.docker_stats_manager_log_dir + config.docker_stats_manager_log_file

    if os.path.exists(path):
        with open(path, 'r') as fp:
            data = fp.readlines()
            tail = data[-100:]
            data=tail
    data_dict = {api_constants.MGMT_WEBAPP.LOGS_PROPERTY: data}
    response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.PROMETHEUS_RESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def prometheus_logs():
    """
    The /logs/prometheus resource.

    :return: The logs of the docker stats manager
    """

    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized

    config = Config.get_current_confg()
    path = config.prometheus_log_file

    if os.path.exists(path):
        with open(path, 'r') as fp:
            data = fp.readlines()
            tail = data[-100:]
            data=tail
    data_dict = {api_constants.MGMT_WEBAPP.LOGS_PROPERTY: data}
    response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def node_exporter_logs():
    """
    The /logs/node-exporter resource.

    :return: The logs of the docker stats manager
    """

    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized

    config = Config.get_current_confg()
    path = config.node_exporter_log_file

    if os.path.exists(path):
        with open(path, 'r') as fp:
            data = fp.readlines()
            tail = data[-100:]
            data=tail
    data_dict = {api_constants.MGMT_WEBAPP.LOGS_PROPERTY: data}
    response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def cadvisor_logs():
    """
    The /logs/cadvisor resource.

    :return: The logs of the docker stats manager
    """

    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized

    cmd = constants.COMMANDS.CADVISOR_LOGS
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    output = output.decode("utf-8")
    output = output.split("\n")[-100:]
    data = output
    data_dict = {api_constants.MGMT_WEBAPP.LOGS_PROPERTY: data}
    response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.GRAFANA_RESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def grafana_logs():
    """
    The /lofgs/grafana resource.

    :return: The logs of the docker stats manager
    """

    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized

    cmd = constants.COMMANDS.GRAFANA_LOGS
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    output = output.decode("utf-8")
    output = output.split("\n")[-100:]
    data = output
    data_dict = {api_constants.MGMT_WEBAPP.LOGS_PROPERTY: data}
    response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.CONTAINER_SUBRESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def container_logs():
    """
    The /logs/container resource.

    :return: The logs of a specific container
    """

    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    container_name = json.loads(request.data)[api_constants.MGMT_WEBAPP.NAME_PROPERTY]
    cmd = constants.COMMANDS.CONTAINER_LOGS.format(container_name)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    output = output.decode("utf-8")
    output = output.split("\n")[-100:]
    data = output
    data_dict = {api_constants.MGMT_WEBAPP.LOGS_PROPERTY: data}
    response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.CLIENT_MANAGER_SUBRESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def client_manager_logs():
    """
    The /logs/client-manager resource.

    :return: The logs of the client manager
    """

    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized

    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    execution_id = request.args.get(api_constants.MGMT_WEBAPP.EXECUTION_ID_QUERY_PARAM)
    if emulation is not None:
        emulation_env_config = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, 
                                                                       emulation_name=emulation).emulation_env_config
        path = emulation_env_config.traffic_config.client_population_config.client_manager_log_dir \
               + emulation_env_config.traffic_config.client_population_config.client_manager_log_file
        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config,
                                    ip=emulation_env_config.traffic_config.client_population_config.ip)
        sftp_client = emulation_env_config.get_connection(
            ip=emulation_env_config.traffic_config.client_population_config.ip).open_sftp()
        remote_file = sftp_client.open(path)
        data = []
        try:
            data = remote_file.read()
            data = data.decode()
            data = data.split("\n")
            data = data[-100:]
        finally:
            remote_file.close()

        data_dict = {api_constants.MGMT_WEBAPP.LOGS_PROPERTY: data}
        response = jsonify(data_dict)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE