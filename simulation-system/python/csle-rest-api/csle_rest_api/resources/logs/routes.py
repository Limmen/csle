"""
Routes and sub-resources for the /logs resource
"""
from flask import Blueprint, jsonify, request
import os
import subprocess
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util
from csle_common.dao.emulation_config.config import Config


# Creates a blueprint "sub application" of the main REST app
logs_bp = Blueprint(
    api_constants.MGMT_WEBAPP.LOGS_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.LOGS_RESOURCE}")


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