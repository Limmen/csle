"""
Routes and sub-resources for the /emulations resource
"""
import base64
import requests
import json
from flask import Blueprint, jsonify, request
import csle_common.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.controllers.container_controller import ContainerController
from csle_common.controllers.emulation_env_controller import EmulationEnvController
from csle_common.util.read_emulation_statistics_util import ReadEmulationStatisticsUtil
import csle_ryu.constants.constants as ryu_constants
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util


# Creates a blueprint "sub application" of the main REST app
emulations_bp = Blueprint(
    api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}")


@emulations_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def emulations():
    """
    The /emulations resource

    :return: Returns a list of emulations, a list of emulation ids, or deletes the list of emulations
    """
    authorized = rest_api_util.check_if_user_is_authorized(request=request)
    if authorized is not None:
        return authorized

    # Check if ids query parameter is True, then only return the ids and not the whole list of emulations
    ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
    if ids is not None and ids:
        return emulation_ids()

    all_emulations = MetastoreFacade.list_emulations()
    all_images = MetastoreFacade.list_emulation_images()
    rc_emulations = ContainerController.list_running_emulations()
    emulations_dicts = []
    for em in all_emulations:
        executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(emulation_name=em.name)
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            if em.name in rc_emulations:
                em.running = True
                for exec in executions:
                    exec.emulation_env_config.running = True
            else:
                em.running = False
            for em_name_img in all_images:
                em_name, img = em_name_img
                if em_name == em.name:
                    em.image = base64.b64encode(img).decode()
                    for exec in executions:
                        exec.emulation_env_config.image = base64.b64encode(img).decode()
            em_dict = em.to_dict()
            em_dict[api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE] = list(map(lambda x: x.to_dict(), executions))
            emulations_dicts.append(em_dict)
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            if em.name in rc_emulations:
                EmulationEnvController.clean_all_emulation_executions(em)
            EmulationEnvController.uninstall_emulation(config=em)
    response = jsonify(emulations_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


def emulation_ids():
    """
    Utility method for returning the list of emulation ids from the metastore to an HTTP client

    :return: HTTP response with list of emulation ids
    """
    emulation_ids = MetastoreFacade.list_emulations_ids()
    rc_emulations = ContainerController.list_running_emulations()
    response_dicts = []
    for tup in emulation_ids:
        running = False
        if tup[1] in rc_emulations:
            running = True
        response_dicts.append({
            api_constants.MGMT_WEBAPP.ID_PROPERTY: tup[0],
            api_constants.MGMT_WEBAPP.EMULATION_PROPERTY: tup[1],
            api_constants.MGMT_WEBAPP.RUNNING_PROPERTY: running
        })
    response = jsonify(response_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@emulations_bp.route(f'{constants.COMMANDS.SLASH_DELIM}<emulation_id>',
                     methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                              api_constants.MGMT_WEBAPP.HTTP_REST_DELETE,
                              api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def emulation_by_id(emulation_id: int):
    """
    The /emulations/id resource. Gets an emulation by its id.

    :param emulation_id: the id of the emulation
    :return: the emulation with the given id if it exists
    """
    authorized = rest_api_util.check_if_user_is_authorized(request=request)
    if authorized is not None:
        return authorized

    em = MetastoreFacade.get_emulation(id=emulation_id)
    rc_emulations = ContainerController.list_running_emulations()
    em_dict = {}
    if em is not None:
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET or \
                request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
            executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(emulation_name=em.name)
            if em.name in rc_emulations:
                em.running = True
                for exec in executions:
                    exec.emulation_env_config.running = True
            em_name, img = MetastoreFacade.get_emulation_image(emulation_name=em.name)
            em.image = base64.b64encode(img).decode()
            for exec in executions:
                exec.emulation_env_config.image = base64.b64encode(img).decode()
            em_dict = em.to_dict()
            em_dict[api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE] = list(map(lambda x: x.to_dict(), executions))
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
                if em.running:
                    EmulationEnvController.clean_all_emulation_executions(emulation_env_config=em)
                    em.running = False
                else:
                    emulation_execution = EmulationEnvController.create_execution(emulation_env_config=em)
                    EmulationEnvController.run_containers(emulation_execution=emulation_execution)
                    EmulationEnvController.apply_emulation_env_config(emulation_execution=emulation_execution,
                                                                      no_traffic=True)
                    em.running = True
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            if em.name in rc_emulations:
                EmulationEnvController.clean_all_emulation_executions(em)
            EmulationEnvController.uninstall_emulation(config=em)
            em_dict = {}
    response = jsonify(em_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response


@emulations_bp.route(f'{constants.COMMANDS.SLASH_DELIM}<emulation_id>{constants.COMMANDS.SLASH_DELIM}'
                     f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}',
                     methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def get_executions_of_emulation(emulation_id: int):
    """
    The /emulations/id/executions resource. Gets all executions of a given emulation.

    :param emulation_id: the id of the emulation
    :return: the list of executions of the emulation
    """
    authorized = rest_api_util.check_if_user_is_authorized(request=request)
    if authorized is not None:
        return authorized

    em = MetastoreFacade.get_emulation(id=emulation_id)
    execution_dicts = []
    if em is not None:
        executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(emulation_name=em.name)
        execution_dicts = list(map(lambda x: x.to_dict(), executions))
    response = jsonify(execution_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@emulations_bp.route(f'{constants.COMMANDS.SLASH_DELIM}<emulation_id>{constants.COMMANDS.SLASH_DELIM}'
                     f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}{constants.COMMANDS.SLASH_DELIM}'
                     f'<execution_id>',
                     methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                              api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def get_execution_of_emulation(emulation_id: int, execution_id: int):
    """
    The /emulations/ids/executions/id resource. Gets a given execution of a given emulation.

    :param emulation_id: the id of the emulation
    :param execution_id: the id of the execution

    :return: The sought for execution if it exist
    """
    authorized = rest_api_util.check_if_user_is_authorized(request=request)
    if authorized is not None:
        return authorized

    execution = None
    emulation = MetastoreFacade.get_emulation(id=emulation_id)
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation.name)
    response = jsonify({})
    if execution is not None:
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            response = jsonify(execution.to_dict())
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            EmulationEnvController.clean_emulation_execution(emulation_env_config=execution.emulation_env_config,
                                                             execution_id=execution.ip_first_octet)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@emulations_bp.route(f'{constants.COMMANDS.SLASH_DELIM}<emulation_id>'
                     f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}'
                     f'{constants.COMMANDS.SLASH_DELIM}<execution_id>'
                     f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.MONITOR_SUBRESOURCE}'
                     f'{constants.COMMANDS.SLASH_DELIM}<minutes>', methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def monitor_emulation(emulation_id: int, execution_id: int, minutes: int):
    """
    The /emulations/id/executions/id/monitor/minutes resource. Fetches monitoring data from Kafka.

    :param emulation_id: the emulation id
    :param execution_id: the execution id
    :param minutes: the number of minutes past to collect data from
    :return: the collected data
    """
    authorized = rest_api_util.check_if_user_is_authorized(request=request)
    if authorized is not None:
        return authorized

    minutes = int(minutes)
    execution = None
    emulation = MetastoreFacade.get_emulation(id=emulation_id)
    if emulation is not None:
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id, emulation_name=emulation.name)
    if execution is None:
        time_series = None
    else:
        time_series = ReadEmulationStatisticsUtil.read_all(emulation_env_config=execution.emulation_env_config,
                                                           time_window_minutes=minutes).to_dict()
    response = jsonify(time_series)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@emulations_bp.route(f'{constants.COMMANDS.SLASH_DELIM}<emulation_id>{constants.COMMANDS.SLASH_DELIM}'
                     f'{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}{constants.COMMANDS.SLASH_DELIM}<exec_id>'
                     f'{constants.COMMANDS.SLASH_DELIM}'
                     f'{api_constants.MGMT_WEBAPP.SWITCHES_SUBRESOURCE}',
                     methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def get_sdn_switches_of_execution(emulation_id: int, exec_id: int):
    """
    The /emulations/id/executions/id/switches resource. Gets SDN switches of a given execution of a given emulation.

    :param emulation_id: the id of the emulation
    :param exec_id: the id of the execution

    :return: The sought for switches if they exist
    """
    authorized = rest_api_util.check_if_user_is_authorized(request=request)
    if authorized is not None:
        return authorized

    em = MetastoreFacade.get_emulation(id=emulation_id)
    response_data = {}
    if em is not None and em.sdn_controller_config is not None:
        executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(emulation_name=em.name)
        for exec in executions:
            if int(exec.ip_first_octet) == int(exec_id):
                response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
                                        f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
                                        f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
                                        f"{ryu_constants.RYU.STATS_SWITCHES_RESOURCE}")
                switches = json.loads(response.content)
                switches_dicts = []
                for dpid in switches:
                    response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
                                            f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
                                            f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
                                            f"{ryu_constants.RYU.STATS_DESC_RESOURCE}/{dpid}")
                    sw_dict = {}
                    sw_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY] = dpid
                    sw_dict[api_constants.MGMT_WEBAPP.DESC_PROPERTY] = json.loads(response.content)[str(dpid)]
                    response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
                                            f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
                                            f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
                                            f"{ryu_constants.RYU.STATS_FLOW_RESOURCE}/{dpid}")
                    sw_dict[api_constants.MGMT_WEBAPP.FLOWS_PROPERTY] = json.loads(response.content)[str(dpid)]
                    response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
                                            f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
                                            f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
                                            f"{ryu_constants.RYU.STATS_AGGREGATE_FLOW_RESOURCE}/{dpid}")
                    sw_dict[api_constants.MGMT_WEBAPP.AGG_FLOWS_PROPERTY] = json.loads(response.content)[str(dpid)][0]
                    response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
                                            f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
                                            f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
                                            f"{ryu_constants.RYU.STATS_TABLE_RESOURCE}/{dpid}")
                    tables = json.loads(response.content)[str(dpid)]
                    tables = list(filter(lambda x: x[api_constants.MGMT_WEBAPP.ACTIVE_COUNT_PROPERTY] > 0, tables))
                    filtered_table_ids = list(map(lambda x: x[api_constants.MGMT_WEBAPP.TABLE_ID_PROPERTY], tables))
                    sw_dict[api_constants.MGMT_WEBAPP.TABLES_PROPERTY] = tables
                    response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
                                            f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
                                            f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
                                            f"{ryu_constants.RYU.STATS_TABLE_FEATURES_RESOURCE}/{dpid}")
                    tablefeatures = json.loads(response.content)[str(dpid)]
                    tablefeatures = list(filter(
                        lambda x: x[api_constants.MGMT_WEBAPP.TABLE_ID_PROPERTY] in filtered_table_ids, tablefeatures))
                    sw_dict[api_constants.MGMT_WEBAPP.TABLE_FEATURES_PROPERTY] = tablefeatures
                    response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
                                            f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
                                            f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
                                            f"{ryu_constants.RYU.STATS_PORT_RESOURCE}/{dpid}")
                    sw_dict[api_constants.MGMT_WEBAPP.PORT_STATS_PROPERTY] = json.loads(response.content)[str(dpid)]
                    response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
                                            f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
                                            f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
                                            f"{ryu_constants.RYU.STATS_PORT_DESC_RESOURCE}/{dpid}")
                    sw_dict[api_constants.MGMT_WEBAPP.PORT_DESCS_PROPERTY] = json.loads(response.content)[str(dpid)]
                    response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
                                            f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
                                            f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
                                            f"{ryu_constants.RYU.STATS_QUEUE_RESOURCE}/{dpid}")
                    sw_dict[api_constants.MGMT_WEBAPP.QUEUES_PROPERTY] = json.loads(response.content)[str(dpid)]
                    response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
                                            f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
                                            f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
                                            f"{ryu_constants.RYU.STATS_QUEUE_CONFIG_RESOURCE}/{dpid}")
                    sw_dict[api_constants.MGMT_WEBAPP.QUEUE_CONFIGS_PROPERTY] = \
                        json.loads(response.content)[str(dpid)][0]
                    response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
                                            f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
                                            f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
                                            f"{ryu_constants.RYU.STATS_GROUP_RESOURCE}/{dpid}")
                    sw_dict[api_constants.MGMT_WEBAPP.GROUPS_PROPERTY] = json.loads(response.content)[str(dpid)]
                    response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
                                            f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
                                            f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
                                            f"{ryu_constants.RYU.STATS_GROUP_DESC_RESOURCE}/{dpid}")
                    sw_dict[api_constants.MGMT_WEBAPP.GROUP_DESCS_PROPERTY] = json.loads(response.content)[str(dpid)]
                    response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
                                            f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
                                            f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
                                            f"{ryu_constants.RYU.STATS_GROUP_FEATURES_RESOURCE}/{dpid}")
                    sw_dict[api_constants.MGMT_WEBAPP.GROUP_FEATURES_PROPERTY] = \
                        json.loads(response.content)[str(dpid)][0]
                    response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
                                            f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
                                            f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
                                            f"{ryu_constants.RYU.STATS_METER_RESOURCE}/{dpid}")
                    sw_dict[api_constants.MGMT_WEBAPP.METERS_PROPERTY] = json.loads(response.content)[str(dpid)]
                    response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
                                            f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
                                            f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
                                            f"{ryu_constants.RYU.STATS_METER_CONFIG_RESOURCE}/{dpid}")
                    sw_dict[api_constants.MGMT_WEBAPP.METER_CONFIGS_PROPERTY] = \
                        json.loads(response.content)[str(dpid)]
                    response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
                                            f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
                                            f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
                                            f"{ryu_constants.RYU.STATS_METER_FEATURES_RESOURCE}/{dpid}")
                    sw_dict[api_constants.MGMT_WEBAPP.METER_FEATURES_PROPERTY] = \
                        json.loads(response.content)[str(dpid)][0]
                    response = requests.get(f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}"
                                            f"{exec.emulation_env_config.sdn_controller_config.container.get_ips()[0]}:"
                                            f"{exec.emulation_env_config.sdn_controller_config.controller_web_api_port}"
                                            f"{ryu_constants.RYU.STATS_ROLE_RESOURCE}/{dpid}")
                    sw_dict[api_constants.MGMT_WEBAPP.ROLES_PROPERTY] = json.loads(response.content)[str(dpid)][0]
                    switches_dicts.append(sw_dict)
                response_data = switches_dicts
    response = jsonify(response_data)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
