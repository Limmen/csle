"""
Routes and sub-resources for the /logs resource
"""
from typing import Tuple
from flask import Blueprint, jsonify, request, Response
import json
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_cluster.cluster_manager.cluster_controller import ClusterController

# Creates a blueprint "sub application" of the main REST app
logs_bp = Blueprint(
    api_constants.MGMT_WEBAPP.LOGS_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.LOGS_RESOURCE}")


@logs_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def logs() -> Tuple[Response, int]:
    """
    The /logs resource.

    :return: List of log files in the CSLE logging directory
    """

    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    json_data = json.loads(request.data)
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data:
        response_str = f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} not provided"
        return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: response_str}),
                constants.HTTPS.BAD_REQUEST_STATUS_CODE)
    ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
    data_dict = ClusterController.get_csle_log_files(ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
    response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.DOCKER_STATS_MANAGER_SUBRESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def docker_stats_manager_logs() -> Tuple[Response, int]:
    """
    The /logs/docker-stats-manager resource.

    :return: The logs of the docker stats manager
    """
    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    json_data = json.loads(request.data)
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data:
        response_str = f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} not provided"
        return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: response_str}),
                constants.HTTPS.BAD_REQUEST_STATUS_CODE)
    ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
    data_dict = ClusterController.get_docker_statsmanager_logs(ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
    response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.PROMETHEUS_RESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def prometheus_logs() -> Tuple[Response, int]:
    """
    The /logs/prometheus resource.

    :return: The Prometheus logs
    """

    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    json_data = json.loads(request.data)
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data:
        response_str = f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} not provided"
        return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: response_str}),
                constants.HTTPS.BAD_REQUEST_STATUS_CODE)
    ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
    data_dict = ClusterController.get_prometheus_logs(ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
    response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.NGINX_RESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def nginx_logs() -> Tuple[Response, int]:
    """
    The /logs/nginx resource.

    :return: The nginx logs
    """

    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    json_data = json.loads(request.data)
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data:
        response_str = f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} not provided"
        return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: response_str}),
                constants.HTTPS.BAD_REQUEST_STATUS_CODE)
    ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
    data_dict = ClusterController.get_nginx_logs(ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
    response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.POSTGRESQL_RESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def postgresql_logs() -> Tuple[Response, int]:
    """
    The /logs/postgresql resource.

    :return: The PostgreSQL logs
    """
    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    json_data = json.loads(request.data)
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data:
        response_str = f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} not provided"
        return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: response_str}),
                constants.HTTPS.BAD_REQUEST_STATUS_CODE)
    ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
    data_dict = ClusterController.get_postgresql_logs(ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
    response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.FLASK_RESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def flask_logs() -> Tuple[Response, int]:
    """
    The /logs/flask resource.

    :return: The Flask logs
    """
    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    json_data = json.loads(request.data)
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data:
        response_str = f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} not provided"
        return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: response_str}),
                constants.HTTPS.BAD_REQUEST_STATUS_CODE)
    ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
    data_dict = ClusterController.get_flask_logs(ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
    response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.CLUSTERMANAGER_RESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def cluster_manager_logs() -> Tuple[Response, int]:
    """
    The /logs/clustermanager resource.

    :return: The Clustermanager logs
    """
    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    json_data = json.loads(request.data)
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data:
        response_str = f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} not provided"
        return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: response_str}),
                constants.HTTPS.BAD_REQUEST_STATUS_CODE)
    ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
    data_dict = ClusterController.get_cluster_manager_logs(ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
    response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.DOCKER_RESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def docker_logs() -> Tuple[Response, int]:
    """
    The /logs/docker resource.

    :return: The Docker logs
    """
    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    json_data = json.loads(request.data)
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data:
        response_str = f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} not provided"
        return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: response_str}),
                constants.HTTPS.BAD_REQUEST_STATUS_CODE)
    ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
    data_dict = ClusterController.get_docker_logs(ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
    response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def node_exporter_logs() -> Tuple[Response, int]:
    """
    The /logs/node-exporter resource.

    :return: The logs of the docker stats manager
    """

    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    json_data = json.loads(request.data)
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data:
        response_str = f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} not provided"
        return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: response_str}),
                constants.HTTPS.BAD_REQUEST_STATUS_CODE)
    ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
    data_dict = ClusterController.get_node_exporter_logs(ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
    response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def cadvisor_logs() -> Tuple[Response, int]:
    """
    The /logs/cadvisor resource.

    :return: The logs of cAdvisor
    """

    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    json_data = json.loads(request.data)
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data:
        response_str = f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} not provided"
        return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: response_str}),
                constants.HTTPS.BAD_REQUEST_STATUS_CODE)
    ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
    data_dict = ClusterController.get_cadvisor_logs(ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
    response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.PGADMIN_RESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def pgadmin_logs() -> Tuple[Response, int]:
    """
    The /logs/pgadmin resource.

    :return: The logs of pgAdmin
    """

    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    json_data = json.loads(request.data)
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data:
        response_str = f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} not provided"
        return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: response_str}),
                constants.HTTPS.BAD_REQUEST_STATUS_CODE)
    ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
    data_dict = ClusterController.get_pgadmin_logs(ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
    response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.GRAFANA_RESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def grafana_logs() -> Tuple[Response, int]:
    """
    The /lofgs/grafana resource.

    :return: The logs of the docker stats manager
    """
    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    json_data = json.loads(request.data)
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data:
        response_str = f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} not provided"
        return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: response_str}),
                constants.HTTPS.BAD_REQUEST_STATUS_CODE)
    ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
    data_dict = ClusterController.get_grafana_logs(ip=ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
    response = jsonify(data_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.CONTAINER_SUBRESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def container_logs() -> Tuple[Response, int]:
    """
    The /logs/container resource.

    :return: The logs of a specific container
    """
    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    if api_constants.MGMT_WEBAPP.NAME_PROPERTY not in json.loads(request.data):
        response = jsonify({})
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
    container_name = json.loads(request.data)[api_constants.MGMT_WEBAPP.NAME_PROPERTY]
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM, default="")
    execution_id = request.args.get(api_constants.MGMT_WEBAPP.EXECUTION_ID_QUERY_PARAM, default=-1)
    if emulation == "" or execution_id == 1:
        response_str = "emulation or execution id query parameters were not provided"
        response = jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: response_str})
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
    execution = MetastoreFacade.get_emulation_execution(ip_first_octet=int(execution_id), emulation_name=emulation)
    container_config = execution.emulation_env_config.containers_config.get_container_from_full_name(
        name=container_name)
    if container_config is not None:
        config = MetastoreFacade.get_config(id=1)
        for node in config.cluster_config.cluster_nodes:
            if container_config.physical_host_ip == node.ip:
                data_dict = ClusterController.get_container_logs(
                    ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=emulation,
                    ip_first_octet=int(execution_id), container_ip=container_config.docker_gw_bridge_ip)
                response = jsonify(data_dict)
                response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
                return response, constants.HTTPS.OK_STATUS_CODE

    response = jsonify({})
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.CLIENT_MANAGER_SUBRESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def client_manager_logs() -> Tuple[Response, int]:
    """
    The /logs/client-manager resource.

    :return: The logs of the client manager
    """
    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    if api_constants.MGMT_WEBAPP.NAME_PROPERTY not in json.loads(request.data):
        response = jsonify({})
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    execution_id = request.args.get(api_constants.MGMT_WEBAPP.EXECUTION_ID_QUERY_PARAM)
    if emulation is not None and execution_id is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=int(execution_id), emulation_name=emulation)
        node_ip = execution.emulation_env_config.traffic_config.client_population_config.physical_host_ip
        data_dict = ClusterController.get_client_manager_logs(
            ip=node_ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=emulation,
            ip_first_octet=int(execution_id))
        response = jsonify(data_dict)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.KAFKA_MANAGER_SUBRESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def kafka_manager_logs() -> Tuple[Response, int]:
    """
    The /logs/kafka-manager resource.

    :return: The logs of the kafka manager
    """
    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    if api_constants.MGMT_WEBAPP.NAME_PROPERTY not in json.loads(request.data):
        response = jsonify({})
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    execution_id = request.args.get(api_constants.MGMT_WEBAPP.EXECUTION_ID_QUERY_PARAM)
    if emulation is not None and execution_id is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=int(execution_id), emulation_name=emulation)
        node_ip = execution.emulation_env_config.kafka_config.container.physical_host_ip
        data_dict = ClusterController.get_kafka_manager_logs(
            ip=node_ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=emulation,
            ip_first_octet=int(execution_id))
        response = jsonify(data_dict)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.KAFKA_SUBRESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def kafka_logs() -> Tuple[Response, int]:
    """
    The /logs/kafka resource.

    :return: The logs of the kafka server
    """
    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    if api_constants.MGMT_WEBAPP.NAME_PROPERTY not in json.loads(request.data):
        response = jsonify({})
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    execution_id = request.args.get(api_constants.MGMT_WEBAPP.EXECUTION_ID_QUERY_PARAM)
    if emulation is not None and execution_id is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=int(execution_id), emulation_name=emulation)
        node_ip = execution.emulation_env_config.kafka_config.container.physical_host_ip
        data_dict = ClusterController.get_kafka_logs(
            ip=node_ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=emulation,
            ip_first_octet=int(execution_id))
        response = jsonify(data_dict)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.SNORT_IDS_MANAGER_SUBRESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def snort_ids_manager_logs() -> Tuple[Response, int]:
    """
    The /logs/snort-ids-manager resource.

    :return: The logs of a Snort IDS manager with a specific IP
    """
    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    if api_constants.MGMT_WEBAPP.NAME_PROPERTY not in json.loads(request.data):
        response = jsonify({})
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
    ip = json.loads(request.data)[api_constants.MGMT_WEBAPP.NAME_PROPERTY]
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    execution_id = request.args.get(api_constants.MGMT_WEBAPP.EXECUTION_ID_QUERY_PARAM)
    if emulation is not None and ip is not None and execution_id is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=int(execution_id), emulation_name=emulation)
        container_config = execution.emulation_env_config.containers_config.get_container_from_ip(ip=ip)
        if container_config is None:
            response = jsonify({})
            response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
            return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
        data_dict = ClusterController.get_snort_ids_manager_logs(
            ip=container_config.physical_host_ip,
            port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=emulation,
            ip_first_octet=int(execution_id), container_ip=ip)
        response = jsonify(data_dict)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.SNORT_IDS_SUBRESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def snort_ids_logs() -> Tuple[Response, int]:
    """
    The /logs/snort-ids-logs resource.

    :return: The logs of a Snort IDS with a specific IP
    """
    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    if api_constants.MGMT_WEBAPP.NAME_PROPERTY not in json.loads(request.data):
        response = jsonify({})
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
    ip = json.loads(request.data)[api_constants.MGMT_WEBAPP.NAME_PROPERTY]
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    execution_id = request.args.get(api_constants.MGMT_WEBAPP.EXECUTION_ID_QUERY_PARAM)
    if emulation is not None and ip is not None and execution_id is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=int(execution_id), emulation_name=emulation)
        container_config = execution.emulation_env_config.containers_config.get_container_from_ip(ip=ip)
        if container_config is None:
            response = jsonify({})
            response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
            return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
        data_dict = ClusterController.get_snort_ids_logs(
            ip=container_config.physical_host_ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=emulation,
            ip_first_octet=int(execution_id), container_ip=ip)
        response = jsonify(data_dict)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.OSSEC_IDS_MANAGER_SUBRESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def ossec_ids_manager_logs() -> Tuple[Response, int]:
    """
    The /logs/ossec-ids-manager resource.

    :return: The logs of a OSSEC IDS manager with a specific IP
    """
    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    if api_constants.MGMT_WEBAPP.NAME_PROPERTY not in json.loads(request.data):
        response = jsonify({})
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
    ip = json.loads(request.data)[api_constants.MGMT_WEBAPP.NAME_PROPERTY]
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    execution_id = request.args.get(api_constants.MGMT_WEBAPP.EXECUTION_ID_QUERY_PARAM)
    if emulation is not None and ip is not None and execution_id is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=int(execution_id), emulation_name=emulation)
        container_config = execution.emulation_env_config.containers_config.get_container_from_ip(ip=ip)
        if container_config is None:
            response = jsonify({})
            response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
            return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
        data_dict = ClusterController.get_ossec_ids_manager_logs(
            ip=container_config.physical_host_ip,
            port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=emulation,
            ip_first_octet=int(execution_id), container_ip=ip)
        response = jsonify(data_dict)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.OSSEC_IDS_SUBRESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def ossec_ids_logs() -> Tuple[Response, int]:
    """
    The /logs/ossec-ids resource.

    :return: The logs of an OSSEC IDS with a specific IP
    """
    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    if api_constants.MGMT_WEBAPP.NAME_PROPERTY not in json.loads(request.data):
        response = jsonify({})
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
    ip = json.loads(request.data)[api_constants.MGMT_WEBAPP.NAME_PROPERTY]
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    execution_id = request.args.get(api_constants.MGMT_WEBAPP.EXECUTION_ID_QUERY_PARAM)
    if emulation is not None and ip is not None and execution_id is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=int(execution_id), emulation_name=emulation)
        container_config = execution.emulation_env_config.containers_config.get_container_from_ip(ip=ip)
        if container_config is None:
            response = jsonify({})
            response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
            return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
        data_dict = ClusterController.get_ossec_ids_logs(
            ip=container_config.physical_host_ip,
            port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=emulation,
            ip_first_octet=int(execution_id), container_ip=ip)
        response = jsonify(data_dict)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.HOST_MANAGER_SUBRESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def host_manager_logs() -> Tuple[Response, int]:
    """
    The /logs/host-manager resource.

    :return: The logs of a Host manager with a specific IP
    """
    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    if api_constants.MGMT_WEBAPP.NAME_PROPERTY not in json.loads(request.data):
        response = jsonify({})
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
    ip = json.loads(request.data)[api_constants.MGMT_WEBAPP.NAME_PROPERTY]
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    execution_id = request.args.get(api_constants.MGMT_WEBAPP.EXECUTION_ID_QUERY_PARAM)
    if emulation is not None and ip is not None and execution_id is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=int(execution_id), emulation_name=emulation)
        container_config = execution.emulation_env_config.containers_config.get_container_from_ip(ip=ip)
        if container_config is None:
            response = jsonify({})
            response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
            return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
        data_dict = ClusterController.get_host_manager_logs(
            ip=container_config.physical_host_ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=emulation,
            ip_first_octet=int(execution_id), container_ip=ip)
        response = jsonify(data_dict)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.TRAFFIC_MANAGER_SUBRESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def traffic_manager_logs() -> Tuple[Response, int]:
    """
    The /logs/traffic-manager resource.

    :return: The logs of a Traffic manager with a specific IP
    """
    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    if api_constants.MGMT_WEBAPP.NAME_PROPERTY not in json.loads(request.data):
        response = jsonify({})
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
    ip = json.loads(request.data)[api_constants.MGMT_WEBAPP.NAME_PROPERTY]
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    execution_id = request.args.get(api_constants.MGMT_WEBAPP.EXECUTION_ID_QUERY_PARAM)
    if emulation is not None and ip is not None and execution_id is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=int(execution_id), emulation_name=emulation)
        container_config = execution.emulation_env_config.containers_config.get_container_from_ip(ip=ip)
        if container_config is None:
            response = jsonify({})
            response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
            return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
        data_dict = ClusterController.get_traffic_manager_logs(
            ip=container_config.physical_host_ip,
            port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=emulation,
            ip_first_octet=int(execution_id), container_ip=ip)
        response = jsonify(data_dict)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.ELK_MANAGER_SUBRESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def elk_manager_logs() -> Tuple[Response, int]:
    """
    The /logs/elk-manager resource.

    :return: The logs of a ELK manager with a specific IP
    """

    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    if api_constants.MGMT_WEBAPP.NAME_PROPERTY not in json.loads(request.data):
        response = jsonify({})
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
    ip = json.loads(request.data)[api_constants.MGMT_WEBAPP.NAME_PROPERTY]
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    execution_id = request.args.get(api_constants.MGMT_WEBAPP.EXECUTION_ID_QUERY_PARAM)
    if emulation is not None and ip is not None and execution_id is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=int(execution_id), emulation_name=emulation)
        physical_host_ip = execution.emulation_env_config.elk_config.container.physical_host_ip
        data_dict = ClusterController.get_elk_manager_logs(
            ip=physical_host_ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=emulation,
            ip_first_octet=int(execution_id))
        response = jsonify(data_dict)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.ELK_STACK_SUBRESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def elk_logs() -> Tuple[Response, int]:
    """
    The /logs/elk-stack resource.

    :return: The logs of an ELK-stack instance with a specific IP
    """
    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    if api_constants.MGMT_WEBAPP.NAME_PROPERTY not in json.loads(request.data):
        response = jsonify({})
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
    ip = json.loads(request.data)[api_constants.MGMT_WEBAPP.NAME_PROPERTY]
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    execution_id = request.args.get(api_constants.MGMT_WEBAPP.EXECUTION_ID_QUERY_PARAM)
    if emulation is not None and ip is not None and execution_id is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=int(execution_id), emulation_name=emulation)
        physical_host_ip = execution.emulation_env_config.elk_config.container.physical_host_ip
        data_dict = ClusterController.get_elk_logs(
            ip=physical_host_ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=emulation,
            ip_first_octet=int(execution_id))
        response = jsonify(data_dict)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.RYU_MANAGER_SUBRESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def ryu_manager_logs() -> Tuple[Response, int]:
    """
    The /logs/ryu-manager resource.

    :return: The logs of a Ryu manager with a specific IP
    """
    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    if api_constants.MGMT_WEBAPP.NAME_PROPERTY not in json.loads(request.data):
        response = jsonify({})
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
    ip = json.loads(request.data)[api_constants.MGMT_WEBAPP.NAME_PROPERTY]
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    execution_id = request.args.get(api_constants.MGMT_WEBAPP.EXECUTION_ID_QUERY_PARAM)
    if emulation is not None and ip is not None and execution_id is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=int(execution_id), emulation_name=emulation)
        if execution.emulation_env_config.sdn_controller_config is None:
            response = jsonify({})
            response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
            return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
        physical_host_ip = execution.emulation_env_config.sdn_controller_config.container.physical_host_ip
        data_dict = ClusterController.get_ryu_manager_logs(
            ip=physical_host_ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=emulation,
            ip_first_octet=int(execution_id))
        response = jsonify(data_dict)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@logs_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.RYU_CONTROLLER_SUBRESOURCE}",
               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def ryu_controller_logs() -> Tuple[Response, int]:
    """
    The /logs/ryu-controller resource.

    :return: The logs of a Ryu controller with a specific IP
    """

    # Check that token is valid
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
    if authorized is not None:
        return authorized
    if api_constants.MGMT_WEBAPP.NAME_PROPERTY not in json.loads(request.data):
        response = jsonify({})
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
    ip = json.loads(request.data)[api_constants.MGMT_WEBAPP.NAME_PROPERTY]
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    execution_id = request.args.get(api_constants.MGMT_WEBAPP.EXECUTION_ID_QUERY_PARAM)
    if emulation is not None and ip is not None and execution_id is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=int(execution_id), emulation_name=emulation)
        if execution.emulation_env_config.sdn_controller_config is None:
            response = jsonify({})
            response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
            return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
        physical_host_ip = execution.emulation_env_config.sdn_controller_config.container.physical_host_ip
        data_dict = ClusterController.get_ryu_controller_logs(
            ip=physical_host_ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=emulation,
            ip_first_octet=int(execution_id))
        response = jsonify(data_dict)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
