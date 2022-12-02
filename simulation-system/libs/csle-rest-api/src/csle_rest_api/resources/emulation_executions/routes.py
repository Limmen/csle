"""
Routes and sub-resources for the /emulation-executions resource
"""
import time

from flask import Blueprint, jsonify, request
from requests import get
import json
from csle_common.logging.log import Logger
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.controllers.container_controller import ContainerController
from csle_common.controllers.emulation_env_controller import EmulationEnvController
from csle_common.controllers.traffic_controller import TrafficController
from csle_common.controllers.kafka_controller import KafkaController
from csle_common.controllers.elk_controller import ELKController
from csle_common.controllers.snort_ids_controller import SnortIDSController
from csle_common.controllers.ossec_ids_controller import OSSECIDSController
from csle_common.controllers.host_controller import HostController
from csle_common.controllers.management_system_controller import ManagementSystemController
import csle_rest_api.util.rest_api_util as rest_api_util

# Creates a blueprint "sub application" of the main REST app
emulation_executions_bp = Blueprint(
    api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}")


@emulation_executions_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def emulation_executions():
    """
    The /emulation-executions resource.

    :return: A list of emulation executions or a list of ids of the executions
    """
    authorized = rest_api_util.check_if_user_is_authorized(request=request)
    if authorized is not None:
        return authorized

    # Check if ids query parameter is True, then only return the ids and not the whole list of emulation executions
    ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
    if ids is not None and ids:
        return emulation_execution_ids()

    all_executions = MetastoreFacade.list_emulation_executions()
    emulation_execution_dicts = []
    for exec in all_executions:
        emulation_execution_dicts.append(exec.to_dict())
    response = jsonify(emulation_execution_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


def emulation_execution_ids():
    """
    Utiltiy method for returning the ids of emulation executions to an HTTP client

    :return: a list of emulation execution ids
    """
    ex_ids = MetastoreFacade.list_emulation_execution_ids()
    rc_emulations = ContainerController.list_running_emulations()
    response_dicts = []
    for tup in ex_ids:
        if tup[1] in rc_emulations:
            response_dicts.append({
                api_constants.MGMT_WEBAPP.ID_PROPERTY: tup[0],
                api_constants.MGMT_WEBAPP.EMULATION_PROPERTY: tup[1],
                api_constants.MGMT_WEBAPP.RUNNING_PROPERTY: True
            })
    response = jsonify(response_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def emulation_execution(execution_id: int):
    """
    The /emulation-executions/id resource.

    :param execution_id: the id of the execution

    :return: The given execution
    """
    authorized = rest_api_util.check_if_user_is_authorized(request=request)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        response = jsonify(execution.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response
    else:
        all_executions_with_the_given_id_dicts = []
        all_executions = MetastoreFacade.list_emulation_executions()
        for exec in all_executions:
            if exec.ip_first_octet == execution_id:
                all_executions_with_the_given_id_dicts.append(exec.to_dict())

        response = jsonify(all_executions_with_the_given_id_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.INFO_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def emulation_execution_info(execution_id: int):
    """
    The /emulation-executions/id/info resource.

    :param execution_id: the id of the execution
    :return: Runtime information about the given execution
    """
    authorized = rest_api_util.check_if_user_is_authorized(request=request)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        local_port = api_constants.MGMT_WEBAPP.KIBANA_TUNNEL_BASE_PORT + execution.ip_first_octet
        if execution.emulation_env_config.elk_config.container.get_ips()[0] \
                not in api_constants.MGMT_WEBAPP.KIBANA_TUNNELS_DICT:
            try:
                EmulationEnvController.create_kibana_tunnel(execution=execution,
                                                            tunnels_dict=api_constants.MGMT_WEBAPP.KIBANA_TUNNELS_DICT,
                                                            local_port=local_port)
            except Exception:
                local_port = local_port + 100
                EmulationEnvController.create_kibana_tunnel(execution=execution,
                                                            tunnels_dict=api_constants.MGMT_WEBAPP.KIBANA_TUNNELS_DICT,
                                                            local_port=local_port)
        else:
            tunnel_thread_dict = api_constants.MGMT_WEBAPP.KIBANA_TUNNELS_DICT[
                execution.emulation_env_config.elk_config.container.get_ips()[0]]
            response = get(f'{constants.HTTP.HTTP_PROTOCOL_PREFIX}{constants.COMMON.LOCALHOST}:'
                           f'{local_port}')
            if response.status_code != constants.HTTPS.OK_STATUS_CODE:
                tunnel_thread_dict[api_constants.MGMT_WEBAPP.THREAD_PROPERTY].shutdown()
                del api_constants.MGMT_WEBAPP.KIBANA_TUNNELS_DICT[
                    execution.emulation_env_config.elk_config.container.get_ips()[0]]
                EmulationEnvController.create_kibana_tunnel(execution=execution,
                                                            tunnels_dict=api_constants.MGMT_WEBAPP.KIBANA_TUNNELS_DICT,
                                                            local_port=local_port)

        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        execution_info.elk_managers_info.local_kibana_port = local_port
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response
    else:
        all_executions_with_the_given_id_dicts = []
        all_executions = MetastoreFacade.list_emulation_executions()
        for exec in all_executions:
            if exec.ip_first_octet == execution_id:
                execution_info = EmulationEnvController.get_execution_info(execution=exec)
                all_executions_with_the_given_id_dicts.append(execution_info)
        response = jsonify({})
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.CLIENT_MANAGER_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_client_manager(execution_id: int):
    """
    The /emulation-executions/id/client-manager resource.

    :param execution_id: the id of the execution
    :return: Starts or stop the client manager of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)
    # Verify payload
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data \
            or api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            Logger.__call__().get_logger().info(
                f"Stopping client manager on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            TrafficController.stop_client_manager(emulation_env_config=execution.emulation_env_config)
        if start:
            Logger.__call__().get_logger().info(
                f"Starting client manager on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            TrafficController.start_client_manager(emulation_env_config=execution.emulation_env_config)
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.CLIENT_POPULATION_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_client_population(execution_id: int):
    """
    The /emulation-executions/id/client-population resource.

    :param execution_id: the id of the execution
    :return: Starts or stop the client manager of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)
    # Verify payload
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data \
            or api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            Logger.__call__().get_logger().info(
                f"Stopping client population on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            TrafficController.stop_client_population(emulation_env_config=execution.emulation_env_config)
        if start:
            Logger.__call__().get_logger().info(
                f"Starting client population on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            TrafficController.start_client_population(emulation_env_config=execution.emulation_env_config)
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.CLIENT_PRODUCER_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_client_producer(execution_id: int):
    """
    The /emulation-executions/id/client-producer resource.

    :param execution_id: the id of the execution
    :return: Starts or stops the client producer of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)
    # Verify payload
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data \
            or api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            Logger.__call__().get_logger().info(
                f"Stopping client producer on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            TrafficController.stop_client_producer(emulation_env_config=execution.emulation_env_config)
        if start:
            Logger.__call__().get_logger().info(
                f"Starting client producer on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            TrafficController.start_client_producer(emulation_env_config=execution.emulation_env_config)
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MANAGER_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_docker_stats_manager(execution_id: int):
    """
    The /emulation-executions/id/docker-stats-manager resource.

    :param execution_id: the id of the execution
    :return: Starts or stop the docker stats manager of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)
    # Verify payload
    if api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            Logger.__call__().get_logger().info(
                f"Stopping docker stats manager for emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            ManagementSystemController.stop_docker_stats_manager()
        if start:
            Logger.__call__().get_logger().info(
                f"Starting docker stats manager for emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            ManagementSystemController.start_docker_stats_manager(
                port=execution.emulation_env_config.docker_stats_manager_config.docker_stats_manager_port,
                log_file=execution.emulation_env_config.docker_stats_manager_config.docker_stats_manager_log_file,
                log_dir=execution.emulation_env_config.docker_stats_manager_config.docker_stats_manager_log_dir
            )
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MONITOR_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_docker_stats_monitor(execution_id: int):
    """
    The /emulation-executions/id/docker-stats-monitor resource.

    :param execution_id: the id of the execution
    :return: Starts or stop the docker stats manager of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)
    # Verify payload
    if api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            Logger.__call__().get_logger().info(
                f"Stopping docker stats monitor for emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            ContainerController.stop_docker_stats_thread(execution=execution)
        if start:
            Logger.__call__().get_logger().info(
                f"Starting docker stats monitor for emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            ContainerController.start_docker_stats_thread(execution=execution)
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.KAFKA_MANAGER_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_kafka_manager(execution_id: int):
    """
    The /emulation-executions/id/kafka-manager resource.

    :param execution_id: the id of the execution
    :return: Starts or stop the kafka manager of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)
    # Verify payload
    if api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            Logger.__call__().get_logger().info(
                f"Stopping kafka manager on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            KafkaController.stop_kafka_manager(emulation_env_config=execution.emulation_env_config)
        if start:
            Logger.__call__().get_logger().info(
                f"Starting kafka manager on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            KafkaController.start_kafka_manager(emulation_env_config=execution.emulation_env_config)
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.KAFKA_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_kafka(execution_id: int):
    """
    The /emulation-executions/id/kafka resource.

    :param execution_id: the id of the execution
    :return: Starts or stop the kafka manager of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)
    # Verify payload
    if api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            Logger.__call__().get_logger().info(
                f"Stopping kafka server on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            KafkaController.stop_kafka_server(emulation_env_config=execution.emulation_env_config)
            time.sleep(20)
        elif start:
            Logger.__call__().get_logger().info(
                f"Starting kafka server on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            KafkaController.start_kafka_server(emulation_env_config=execution.emulation_env_config)
            time.sleep(35)
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MANAGER_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_snort_manager(execution_id: int):
    """
    The /emulation-executions/id/snort-ids-manager resource.

    :param execution_id: the id of the execution
    :return: Starts or stop the snort manager of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)
    # Verify payload
    if api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            Logger.__call__().get_logger().info(
                f"Stopping snort manager on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            SnortIDSController.stop_snort_managers(emulation_env_config=execution.emulation_env_config)
        if start:
            Logger.__call__().get_logger().info(
                f"Starting snort manager on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            SnortIDSController.start_snort_managers(emulation_env_config=execution.emulation_env_config)
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.SNORT_IDS_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_snort_ids(execution_id: int):
    """
    The /emulation-executions/id/snort-ids resource.

    :param execution_id: the id of the execution
    :return: Starts or stop the snort manager of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)
    # Verify payload
    if api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            Logger.__call__().get_logger().info(
                f"Stopping snort on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            SnortIDSController.stop_snort_idses(emulation_env_config=execution.emulation_env_config)
        if start:
            Logger.__call__().get_logger().info(
                f"Starting snort on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            SnortIDSController.start_snort_idses(emulation_env_config=execution.emulation_env_config)
        time.sleep(10)
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MONITOR_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_snort_ids_monitor(execution_id: int):
    """
    The /emulation-executions/id/snort-ids-monitor resource.

    :param execution_id: the id of the execution
    :return: Starts or stop the snort manager of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)
    # Verify payload
    if api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            Logger.__call__().get_logger().info(
                f"Stopping snort-ids-monitor on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            SnortIDSController.stop_snort_idses_monitor_threads(emulation_env_config=execution.emulation_env_config)
        if start:
            Logger.__call__().get_logger().info(
                f"Starting snort-ids-monitor on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            SnortIDSController.start_snort_idses_monitor_threads(emulation_env_config=execution.emulation_env_config)
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_MANAGER_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_ossec_manager(execution_id: int):
    """
    The /emulation-executions/id/ossec-ids-manager resource.

    :param execution_id: the id of the execution
    :return: Starts or stop the ossec manager of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)
    # Verify payload
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data \
            or api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            if ip == api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Stopping all OSSEC IDS managers on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                OSSECIDSController.stop_ossec_idses_managers(emulation_env_config=execution.emulation_env_config)
            else:
                Logger.__call__().get_logger().info(
                    f"Stopping OSSEC IDS manager with ip:{ip} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                OSSECIDSController.stop_ossec_ids_manager(emulation_env_config=execution.emulation_env_config, ip=ip)
        if start:
            if ip == api_constants.MGMT_WEBAPP.START_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Starting all OSSEC IDS managers on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                OSSECIDSController.start_ossec_idses_managers(emulation_env_config=execution.emulation_env_config)
            else:
                Logger.__call__().get_logger().info(
                    f"Starting OSSEC IDS manager with ip:{ip} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                OSSECIDSController.start_ossec_ids_manager(emulation_env_config=execution.emulation_env_config, ip=ip)
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_ossec_ids(execution_id: int):
    """
    The /emulation-executions/id/ossec-ids resource.

    :param execution_id: the id of the execution
    :return: Starts or stop the ossec manager of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)
    # Verify payload
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data \
            or api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            if ip == api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Stopping all OSSEC IDSes on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                OSSECIDSController.stop_ossec_idses(emulation_env_config=execution.emulation_env_config)
            else:
                Logger.__call__().get_logger().info(
                    f"Stopping OSSEC IDS with IP: {ip} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                OSSECIDSController.stop_ossec_ids(emulation_env_config=execution.emulation_env_config, ip=ip)
        if start:
            if ip == api_constants.MGMT_WEBAPP.START_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Starting all OSSEC IDSes on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                OSSECIDSController.start_ossec_idses(emulation_env_config=execution.emulation_env_config)
            else:
                Logger.__call__().get_logger().info(
                    f"Starting OSSEC IDS with IP: {ip} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                OSSECIDSController.start_ossec_ids(emulation_env_config=execution.emulation_env_config, ip=ip)
        time.sleep(30)
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_MONITOR_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_ossec_ids_monitor(execution_id: int):
    """
    The /emulation-executions/id/ossec-ids-monitor resource.

    :param execution_id: the id of the execution
    :return: Starts or stop the ossec-ids-monitor of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)
    # Verify payload
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data \
            or api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            if ip == api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Stopping all OSSEC IDS monitors on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                OSSECIDSController.stop_ossec_idses_monitor_threads(
                    emulation_env_config=execution.emulation_env_config)
            else:
                Logger.__call__().get_logger().info(
                    f"Stopping OSSEC IDS monitors with IP: {ip} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                OSSECIDSController.stop_ossec_ids_monitor_thread(emulation_env_config=execution.emulation_env_config,
                                                                 ip=ip)
        if start:
            if ip == api_constants.MGMT_WEBAPP.START_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Starting all OSSEC IDS monitors on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                OSSECIDSController.start_ossec_idses_monitor_threads(
                    emulation_env_config=execution.emulation_env_config)
            else:
                Logger.__call__().get_logger().info(
                    f"Starting OSSEC IDS monitor with IP: {ip} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                OSSECIDSController.start_ossec_ids_monitor_thread(emulation_env_config=execution.emulation_env_config,
                                                                  ip=ip)
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.HOST_MANAGER_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_host_manager(execution_id: int):
    """
    The /emulation-executions/id/host-manager resource.

    :param execution_id: the id of the execution
    :return: Starts or stop the host managers of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)
    # Verify payload
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data \
            or api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            if ip == api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Stopping all host managers on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.stop_host_managers(emulation_env_config=execution.emulation_env_config)
            else:
                Logger.__call__().get_logger().info(
                    f"Stopping host manager with IP:{ip} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.stop_host_manager(emulation_env_config=execution.emulation_env_config, ip=ip)
        if start:
            if ip == api_constants.MGMT_WEBAPP.START_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Starting all host managers on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.start_host_managers(emulation_env_config=execution.emulation_env_config)
            else:
                Logger.__call__().get_logger().info(
                    f"Starting host manager with IP: {ip} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.start_host_manager(emulation_env_config=execution.emulation_env_config, ip=ip)
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.HOST_MONITOR_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_host_monitor_thread(execution_id: int):
    """
    The /emulation-executions/id/host-manager resource.

    :param execution_id: the id of the execution
    :return: Starts or stop the host managers of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)
    # Verify payload
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data \
            or api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            if ip == api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Stopping all host monitors on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.stop_host_monitor_threads(emulation_env_config=execution.emulation_env_config)
            else:
                Logger.__call__().get_logger().info(
                    f"Stopping host monitor with IP:{ip} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.stop_host_monitor_thread(emulation_env_config=execution.emulation_env_config, ip=ip)
        if start:
            if ip == api_constants.MGMT_WEBAPP.START_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Starting all host monitors on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.start_host_monitor_threads(emulation_env_config=execution.emulation_env_config)
            else:
                Logger.__call__().get_logger().info(
                    f"Starting host monitor with IP:{ip} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.start_host_monitor_thread(emulation_env_config=execution.emulation_env_config, ip=ip)
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.CONTAINER_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_container(execution_id: int):
    """
    The /emulation-executions/id/container resource.

    :param execution_id: the id of the execution
    :return: Starts or stops a container of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)

    json_data = json.loads(request.data)
    # Extract container name
    if api_constants.MGMT_WEBAPP.NAME_PROPERTY not in json_data \
            or api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        container_name = json_data[api_constants.MGMT_WEBAPP.NAME_PROPERTY]
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            if container_name == api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Stopping all running containers on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                EmulationEnvController.stop_containers(execution=execution)
            else:
                Logger.__call__().get_logger().info(
                    f"Stopping container: {container_name} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                ContainerController.stop_container(container_name)
        if start:
            if container_name == api_constants.MGMT_WEBAPP.START_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Starting all running containers on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                EmulationEnvController.start_containers(emulation_execution=execution)
            Logger.__call__().get_logger().info(
                f"Starting container: {container_name}, on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            ContainerController.start_container(container_name)
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.ELK_MANAGER_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_elk_manager(execution_id: int):
    """
    The /emulation-executions/id/elk-manager resource.

    :param execution_id: the id of the execution
    :return: Starts or stop the elk manager of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)

    json_data = json.loads(request.data)
    # Verify payload
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data \
            or api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            Logger.__call__().get_logger().info(
                f"Stopping ELK manager: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            ELKController.stop_elk_manager(emulation_env_config=execution.emulation_env_config)
        if start:
            Logger.__call__().get_logger().info(
                f"Starting ELK manager: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            ELKController.start_elk_manager(emulation_env_config=execution.emulation_env_config)
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.ELK_STACK_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_elk_stack(execution_id: int):
    """
    The /emulation-executions/id/elk-stack resource.

    :param execution_id: the id of the execution
    :return: Starts or stop the ELK stack of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)
    # Verify payload
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data \
            or api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            Logger.__call__().get_logger().info(
                f"Stopping ELK stack on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            ELKController.stop_elk_stack(emulation_env_config=execution.emulation_env_config)
            time.sleep(5)
        if start:
            Logger.__call__().get_logger().info(
                f"Starting ELK stack on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            ELKController.start_elk_stack(emulation_env_config=execution.emulation_env_config)
            time.sleep(30)
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.ELASTIC_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_elastic(execution_id: int):
    """
    The /emulation-executions/id/elastic resource.

    :param execution_id: the id of the execution
    :return: Starts or stop the elastic instance of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)
    # Verify payload
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data \
            or api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            Logger.__call__().get_logger().info(
                f"Stopping elasticsearch on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            ELKController.stop_elastic(emulation_env_config=execution.emulation_env_config)
        if start:
            Logger.__call__().get_logger().info(
                f"Starting elasticsearch on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            ELKController.start_elastic(emulation_env_config=execution.emulation_env_config)
        time.sleep(2)
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.LOGSTASH_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_logstash(execution_id: int):
    """
    The /emulation-executions/id/logstash resource.

    :param execution_id: the id of the execution
    :return: Starts or stop the logstash of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)
    # Verify payload
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data \
            or api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            Logger.__call__().get_logger().info(
                f"Stopping logstash on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            ELKController.stop_logstash(emulation_env_config=execution.emulation_env_config)
        if start:
            Logger.__call__().get_logger().info(
                f"Starting logstash on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            ELKController.start_logstash(emulation_env_config=execution.emulation_env_config)
        time.sleep(2)
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.KIBANA_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_kibana(execution_id: int):
    """
    The /emulation-executions/id/kibana resource.

    :param execution_id: the id of the execution
    :return: Starts or stop the kibana instance of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)
    # Verify payload
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data \
            or api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            Logger.__call__().get_logger().info(
                f"Stopping kibana on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            ELKController.stop_kibana(emulation_env_config=execution.emulation_env_config)
        if start:
            Logger.__call__().get_logger().info(
                f"Starting kibana on emulation: {execution.emulation_env_config.name}, "
                f"execution id: {execution.ip_first_octet}")
            ELKController.start_kibana(emulation_env_config=execution.emulation_env_config)
        time.sleep(2)
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.TRAFFIC_MANAGER_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_traffic_manager(execution_id: int):
    """
    The /emulation-executions/id/traffic-manager resource.

    :param execution_id: the id of the execution
    :return: Starts or stop the traffic manager of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)
    # Verify payload
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data \
            or api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            if ip == api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Stopping all traffic managers on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                TrafficController.stop_traffic_managers(emulation_env_config=execution.emulation_env_config)
            else:
                Logger.__call__().get_logger().info(
                    f"Stopping traffic manager with ip: {ip} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                TrafficController.stop_traffic_manager(
                    emulation_env_config=execution.emulation_env_config,
                    node_traffic_config=execution.emulation_env_config.traffic_config.get_node_traffic_config_by_ip(
                        ip=ip))
        if start:
            if ip == api_constants.MGMT_WEBAPP.START_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Starting all traffic managers on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                TrafficController.start_traffic_managers(emulation_env_config=execution.emulation_env_config)
            else:
                Logger.__call__().get_logger().info(
                    f"Starting traffic manager with ip: {ip} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                TrafficController.start_traffic_manager(
                    emulation_env_config=execution.emulation_env_config,
                    node_traffic_config=execution.emulation_env_config.traffic_config.get_node_traffic_config_by_ip(
                        ip=ip))
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.TRAFFIC_GENERATOR_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_traffic_generator(execution_id: int):
    """
    The /emulation-executions/id/traffic-generator resource.

    :param execution_id: the id of the execution
    :return: Starts or stop the traffic manager of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)
    # Verify payload
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data \
            or api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            if ip == api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Stopping all traffic generators on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                TrafficController.stop_internal_traffic_generators(emulation_env_config=execution.emulation_env_config)
            else:
                Logger.__call__().get_logger().info(
                    f"Stopping traffic generator with ip: {ip} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                TrafficController.stop_internal_traffic_generator(
                    emulation_env_config=execution.emulation_env_config,
                    node_traffic_config=execution.emulation_env_config.traffic_config.get_node_traffic_config_by_ip(
                        ip=ip))
        if start:
            if ip == api_constants.MGMT_WEBAPP.START_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Starting all traffic generators on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                TrafficController.start_internal_traffic_generators(emulation_env_config=execution.emulation_env_config)
            else:
                Logger.__call__().get_logger().info(
                    f"Starting traffic generator with ip: {ip} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                TrafficController.start_internal_traffic_generator(
                    emulation_env_config=execution.emulation_env_config,
                    node_traffic_config=execution.emulation_env_config.traffic_config.get_node_traffic_config_by_ip(
                        ip=ip),
                    container=execution.emulation_env_config.get_container_from_ip(ip=ip))
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.FILEBEAT_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_filebeat(execution_id: int):
    """
    The /emulation-executions/id/filebeat resource.

    :param execution_id: the id of the execution
    :return: Starts or stop filebeat of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)

    # Verify payload
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data \
            or api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            if ip == api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Stopping all filebeats on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.stop_filebeats(emulation_env_config=execution.emulation_env_config)
            else:
                Logger.__call__().get_logger().info(
                    f"Stopping filebeat with ip: {ip} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.stop_filebeat(emulation_env_config=execution.emulation_env_config, ip=ip)
        if start:
            if ip == api_constants.MGMT_WEBAPP.START_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Starting all filebeats on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.start_filebeats(emulation_env_config=execution.emulation_env_config,
                                               initial_start=False)
            else:
                Logger.__call__().get_logger().info(
                    f"Starting filebeat with ip: {ip} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.start_filebeat(
                    emulation_env_config=execution.emulation_env_config,
                    ips=execution.emulation_env_config.get_container_from_ip(ip=ip).get_ips())
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.PACKETBEAT_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_packetbeat(execution_id: int):
    """
    The /emulation-executions/id/packetbeat resource.

    :param execution_id: the id of the execution
    :return: Starts or stop packetbeat of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)

    # Verify payload
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data \
            or api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            if ip == api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Stopping all packetbeats on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.stop_packetbeats(emulation_env_config=execution.emulation_env_config)
            else:
                Logger.__call__().get_logger().info(
                    f"Stopping packetbeat with ip: {ip} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.stop_packetbeat(emulation_env_config=execution.emulation_env_config, ip=ip)
        if start:
            if ip == api_constants.MGMT_WEBAPP.START_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Starting all packetbeats on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.start_packetbeats(emulation_env_config=execution.emulation_env_config,
                                                 initial_start=False)
            else:
                Logger.__call__().get_logger().info(
                    f"Starting packetbeat with ip: {ip} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.start_packetbeat(
                    emulation_env_config=execution.emulation_env_config,
                    ips=execution.emulation_env_config.get_container_from_ip(ip=ip).get_ips())
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.METRICBEAT_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_metricbeat(execution_id: int):
    """
    The /emulation-executions/id/metricbeat resource.

    :param execution_id: the id of the execution
    :return: Starts or stop metricbeat of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)

    # Verify payload
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data \
            or api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            if ip == api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Stopping all metricbeats on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.stop_metricbeats(emulation_env_config=execution.emulation_env_config)
            else:
                Logger.__call__().get_logger().info(
                    f"Stopping metricbeat with ip: {ip} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.stop_metricbeat(emulation_env_config=execution.emulation_env_config, ip=ip)
        if start:
            if ip == api_constants.MGMT_WEBAPP.START_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Starting all metricbeats on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.start_metricbeats(emulation_env_config=execution.emulation_env_config,
                                                 initial_start=False)
            else:
                Logger.__call__().get_logger().info(
                    f"Starting metricbeat with ip: {ip} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.start_metricbeat(
                    emulation_env_config=execution.emulation_env_config,
                    ips=execution.emulation_env_config.get_container_from_ip(ip=ip).get_ips())
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE


@emulation_executions_bp.route(f"{constants.COMMANDS.SLASH_DELIM}<execution_id>{constants.COMMANDS.SLASH_DELIM}"
                               f"{api_constants.MGMT_WEBAPP.HEARTBEAT_SUBRESOURCE}",
                               methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def start_stop_heartbeat(execution_id: int):
    """
    The /emulation-executions/id/heartbeat resource.

    :param execution_id: the id of the execution
    :return: Starts or stop heartbeat of a given execution
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # Extract emulation query parameter
    emulation = request.args.get(api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM)
    json_data = json.loads(request.data)

    # Verify payload
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data \
            or api_constants.MGMT_WEBAPP.START_PROPERTY not in json_data or \
            api_constants.MGMT_WEBAPP.STOP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation)
        ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]
        start = json_data[api_constants.MGMT_WEBAPP.START_PROPERTY]
        stop = json_data[api_constants.MGMT_WEBAPP.STOP_PROPERTY]
        if stop:
            if ip == api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Stopping all heartbeats on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.stop_heartbeats(emulation_env_config=execution.emulation_env_config)
            else:
                Logger.__call__().get_logger().info(
                    f"Stopping heartbeat with ip: {ip} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.stop_heartbeat(emulation_env_config=execution.emulation_env_config, ip=ip)
        if start:
            if ip == api_constants.MGMT_WEBAPP.START_ALL_PROPERTY:
                Logger.__call__().get_logger().info(
                    f"Starting all heartbeats on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.start_heartbeats(emulation_env_config=execution.emulation_env_config,
                                                initial_start=False)
            else:
                Logger.__call__().get_logger().info(
                    f"Starting heartbeat with ip: {ip} on emulation: {execution.emulation_env_config.name}, "
                    f"execution id: {execution.ip_first_octet}")
                HostController.start_heartbeat(
                    emulation_env_config=execution.emulation_env_config,
                    ips=execution.emulation_env_config.get_container_from_ip(ip=ip).get_ips())
        execution_info = EmulationEnvController.get_execution_info(execution=execution)
        response = jsonify(execution_info.to_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    else:
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.BAD_REQUEST_STATUS_CODE
