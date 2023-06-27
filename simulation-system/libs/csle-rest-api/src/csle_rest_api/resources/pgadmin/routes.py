"""
Routes and sub-resources for the /pgadmin resource
"""
import json
from flask import Blueprint, jsonify, request
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_cluster.cluster_manager.cluster_controller import ClusterController

# Creates a blueprint "sub application" of the main REST app
pgadmin_bp = Blueprint(
    api_constants.MGMT_WEBAPP.PGADMIN_RESOURCE,
    __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.PGADMIN_RESOURCE}",
)


@pgadmin_bp.route(
    "",
    methods=[
        api_constants.MGMT_WEBAPP.HTTP_REST_GET,
        api_constants.MGMT_WEBAPP.HTTP_REST_POST,
    ],
)
def pgadmin():
    """
    :return: static resources for the /pgadmin url
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(
        request=request, requires_admin=requires_admin
    )
    if authorized is not None:
        return authorized

    json_data = json.loads(request.data)
    if api_constants.MGMT_WEBAPP.IP_PROPERTY not in json_data:
        return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
    ip = json_data[api_constants.MGMT_WEBAPP.IP_PROPERTY]

    config = MetastoreFacade.get_config(id=1)
    cluster_statuses = []
    for node in config.cluster_config.cluster_nodes:
        node_status = ClusterController.get_node_status(
            ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT
        )
        if node.ip == ip:
            if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
                if node_status.pgAdminRunning:
                    ClusterController.stop_pgadmin(
                        ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT
                    )
                    node_status.pgAdminRunning = False
                else:
                    ClusterController.start_pgadmin(
                        ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT
                    )
                    node_status.pgAdminRunning = True
        cluster_status_dict = {
            api_constants.MGMT_WEBAPP.CADVISOR_RUNNING_PROPERTY: node_status.cAdvisorRunning,
            api_constants.MGMT_WEBAPP.GRAFANA_RUNNING_PROPERTY: node_status.grafanaRunning,
            api_constants.MGMT_WEBAPP.POSTGRESQL_RUNNING_PROPERTY: node_status.postgreSQLRunning,
            api_constants.MGMT_WEBAPP.NODE_EXPORTER_RUNNING_PROPERTY: node_status.nodeExporterRunning,
            api_constants.MGMT_WEBAPP.DOCKER_ENGINE_RUNNING_PROPERTY: node_status.dockerEngineRunning,
            api_constants.MGMT_WEBAPP.NGINX_RUNNING_PROPERTY: node_status.nginxRunning,
            api_constants.MGMT_WEBAPP.FLASK_RUNNING_PROPERTY: node_status.flaskRunning,
            api_constants.MGMT_WEBAPP.PROMETHEUS_RUNNING_PROPERTY: node_status.prometheusRunning,
            api_constants.MGMT_WEBAPP.PGADMIN_RUNNING_PROPERTY: node_status.pgAdminRunning,
            api_constants.MGMT_WEBAPP.CADVISOR_URL_PROPERTY: f"http://{node.ip}:{constants.COMMANDS.CADVISOR_PORT}/",
            api_constants.MGMT_WEBAPP.GRAFANA_URL_PROPERTY: f"http://{node.ip}:{constants.COMMANDS.GRAFANA_PORT}/",
            api_constants.MGMT_WEBAPP.NODE_EXPORTER_URL_PROPERTY: f"http://{node.ip}:"
            f"{constants.COMMANDS.NODE_EXPORTER_PORT}/",
            api_constants.MGMT_WEBAPP.FLASK_URL_PROPERTY: f"http://{node.ip}:{constants.COMMANDS.FLASK_PORT}/",
            api_constants.MGMT_WEBAPP.PROMETHEUS_URL_PROPERTY: f"http://{node.ip}:"
            f"{constants.COMMANDS.PROMETHEUS_PORT}/",
            api_constants.MGMT_WEBAPP.PGADMIN_URL_PROPERTY: f"http://{node.ip}:{constants.COMMANDS.PGADMIN_PORT}/",
            api_constants.MGMT_WEBAPP.CADVISOR_PORT_PROPERTY: constants.COMMANDS.CADVISOR_PORT,
            api_constants.MGMT_WEBAPP.GRAFANA_PORT_PROPERTY: constants.COMMANDS.GRAFANA_PORT,
            api_constants.MGMT_WEBAPP.NODE_EXPORTER_PORT_PROPERTY: constants.COMMANDS.NODE_EXPORTER_PORT,
            api_constants.MGMT_WEBAPP.FLASK_PORT_PROPERTY: constants.COMMANDS.FLASK_PORT,
            api_constants.MGMT_WEBAPP.PROMETHEUS_PORT_PROPERTY: constants.COMMANDS.PROMETHEUS_PORT,
            api_constants.MGMT_WEBAPP.PGADMIN_PORT_PROPERTY: constants.COMMANDS.PGADMIN_PORT,
            api_constants.MGMT_WEBAPP.IP_PROPERTY: node.ip,
            api_constants.MGMT_WEBAPP.CPUS_PROPERTY: node.cpus,
            api_constants.MGMT_WEBAPP.GPUS_PROPERTY: node.gpus,
            api_constants.MGMT_WEBAPP.RAM_PROPERTY: node.RAM,
            api_constants.MGMT_WEBAPP.LEADER_PROPERTY: node.leader,
        }
        cluster_statuses.append(cluster_status_dict)
    response = jsonify(cluster_statuses)
    response.headers.add(
        api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*"
    )
    return response, constants.HTTPS.OK_STATUS_CODE
