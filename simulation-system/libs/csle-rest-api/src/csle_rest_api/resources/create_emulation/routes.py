"""
Routes and sub-resources for the /create-emulation resource
"""
from typing import Tuple
import csle_common.constants.constants as constants
from flask import Blueprint, jsonify, request, Response
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util

import json

from csle_common.dao.emulation_config.vulnerabilities_config import VulnerabilitiesConfig
from csle_common.dao.emulation_config.node_vulnerability_config import NodeVulnerabilityConfig

def vulnerabilities(emulation_data:json) -> VulnerabilitiesConfig:

    # This function has problems. In this function in the front end the credentials are not defined and prepared on
    # the web page.

    print(emulation_data)

    vulns = []

    emulation_containers = emulation_data["emulationContainer"]
    for containers in emulation_containers:
        container_interfaces = containers["interfaces"]
        for interfaces in container_interfaces:
            interface_ip = interfaces["ip"]
        container_vulns = containers["vulns"]
        for vuln in container_vulns:
            vuln_name = vuln["vulnName"]
            vuln_type = vuln["vulnType"]
            vuln_service_name = vuln["vulnService"]["name"]
            vuln_service_protocol = vuln["vulnService"]["protocol"]
            vuln_service_port = vuln["vulnService"]["port"]
            vuln_service_ip = vuln["vulnService"]["serviceIp"]
            vuln_root_access = vuln["vulnRoot"]

            node_vuln_config = NodeVulnerabilityConfig(
                name=vuln_name,
                ip=interface_ip,
                vuln_type=vuln_type,
                credentials=[],
                cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS,
                cve=None,
                root=vuln_root_access, port=vuln_service_port,
                protocol=vuln_service_protocol, service=vuln_service_name)
            vulns.append(node_vuln_config)
    vulns_config = VulnerabilitiesConfig(node_vulnerability_configs=vulns)
    return vulns_config

# Creates a blueprint "sub application" of the main REST app
create_emulation_bp = Blueprint(
    api_constants.MGMT_WEBAPP.CREATE_EMULATION_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.CREATE_EMULATION_RESOURCE}")


@create_emulation_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def create_emulation() -> Tuple[Response, int]:
    """
    The /create-emulation resource.

    :return: The given policy or deletes the policy
    """
    print("Create emulation")
    requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    # print(request.data)
    emulation_data = json.loads(request.data)
    emulation_name = emulation_data["emulationName"]
    emulation_network_id = emulation_data["emulationNetworkId"]
    emulation_level = emulation_data["emulationLevel"]
    emulation_version = emulation_data["emulationVersion"]
    emulation_time_step_length = emulation_data["emulationTimeStepLengh"]
    emulation_ids_enabled = emulation_data["emulatioIdsEnabled"]
    emulation_description = emulation_data["emulationDescription"]
    emulation_containers = emulation_data["emulationContainer"]
    for containers in emulation_containers:
        container_name = containers["name"]
        container_os = containers["os"]
        container_version = containers["version"]
        containers_level = containers["level"]
        container_restart_policy = containers["restartPolicy"]
        container_network_id = containers["networkId"]
        container_subnet_mask = containers["subnetMask"]
        container_subnet_prefix = containers["subnetPrefix"]
        container_cpu = containers["cpu"]
        container_memory = containers["mem"]
        container_falg_id = containers["flagId"]
        container_flag_score = containers["flagScore"]
        container_flag_permission = containers["flagPermission"]
        container_interfaces = containers["interfaces"]
        for interfaces in container_interfaces:
            interface_name = interfaces["name"]
            interface_ip = interfaces["ip"]
            interface_subnet_mask = interfaces["subnetMask"]
            interface_subnet_prefix = interfaces["subnetPrefix"]
            interface_physical_interface = interfaces["physicalInterface"]
            interface_bit_mask = interfaces["bitmask"]
            interface_limit_packet_queue = interfaces["limitPacketsQueue"]
            interface_packet_delay_ms = interfaces["packetDelayMs"]
            interface_packet_delay_jitter_ms = interfaces["packetDelayJitterMs"]
            interface_packet_delay_correlation_percentage = interfaces["packetDelayCorrelationPercentage"]
            interfaces_packet_delay_distribution = interfaces["packetDelayDistribution"]
            interface_packet_loss_type = interfaces["packetLossType"]
            interface_loss_gmodel_p = interfaces["lossGemodelp"]
            interface_loss_gmodel_p = interfaces["lossGemodelr"]
            interface_loss_gmodel_p = interfaces["lossGemodelk"]
            interface_loss_gmodel_p = interfaces["lossGemodelh"]
            interface_packet_corruption_percentage = interfaces["packetCorruptPercentage"]
            interface_packet_corruption_correlation_percentage = interfaces["packetCorruptCorrelationPercentage"]
            interface_packet_duplication_percentage = interfaces["packetDuplicatePercentage"]
            interface_packet_duplicate_correlation_percentage = interfaces["packetDuplicateCorrelationPercentage"]
            interface_packet_reorder_percentage = interfaces["packetReorderPercentage"]
            interface_packet_reorder_correlation_percentage = interfaces["packetReorderCorrelationPercentage"]
            interface_packet_reorder_gap = interfaces["packetReorderGap"]
            interface_rate_limit_m_bit = interfaces["rateLimitMbit"]
            interface_packet_overhead_bytes = interfaces["packetOverheadBytes"]
            interface_cell_overhead_bytes = interfaces["cellOverheadBytes"]
            interface_default_gateway = interfaces["defaultGateway"]
            interface_default_input = interfaces["defaultInput"]
            interface_default_output = interfaces["defaultOutput"]
            interface_default_forward = interfaces["defaultForward"]
            interfaces_traffic_manager_port = interfaces["trafficManagerPort"]
            interface_traffic_manager_log_file = interfaces["trafficManagerLogFile"]
            interface_traffic_manager_log_dir = interfaces["trafficManagerLogDir"]
            interface_traffic_manager_max_workers = interfaces["trafficManagerMaxWorkers"]
            print("Container name: ", container_name, " interface is:", interface_name)
        container_reachable_by_agent = containers["reachableByAgent"]
        container_users = containers["users"]
        for user in container_users:
            user_name = user["userName"]
            user_pw = user["pw"]
            user_access = user["root"]
        container_services = containers["services"]
        for service in container_services:
            service_name = service["name"]
            service_protocol = service["protocol"]
            service_port = service["port"]
            service_ip = service["serviceIp"]
        container_vulns = containers["vulns"]
        for vuln in container_vulns:
            vuln_name = vuln["vulnName"]
            vuln_type = vuln["vulnType"]
            vuln_service_name = vuln["vulnService"]["name"]
            vuln_service_protocol = vuln["vulnService"]["protocol"]
            vuln_service_port = vuln["vulnService"]["port"]
            vuln_service_ip = vuln["vulnService"]["serviceIp"]
            vuln_root_access = vuln["vulnRoot"]
            print("Container vuln service name: ", vuln_service_name)

    vulnerabilities(emulation_data)

    response = jsonify({"TEST": "TEST"})
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
