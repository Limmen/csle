"""
Routes and sub-resources for the /grafana-page page
"""

from flask import Blueprint, jsonify, request
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_cluster.cluster_manager.cluster_controller import ClusterController


# Creates a blueprint "sub application" of the main REST app
grafana_bp = Blueprint(api_constants.MGMT_WEBAPP.GRAFANA_RESOURCE, __name__,
                       url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.GRAFANA_RESOURCE}")


@grafana_bp.route("",
                  methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def grafana():
    """
    :return: static resources for the /grafana url
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    config = MetastoreFacade.get_config(id=1)
    grafana_statuses = []
    for node in config.cluster_config.cluster_nodes:
        node_status = ClusterController.get_node_status(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
            if node_status.grafanaRunning:
                ClusterController.stop_grafana(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
                node_status.grafanaRunning = False
            else:
                ClusterController.start_grafana(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
                node_status.grafanaRunning = True
        grafana_dict = {
            api_constants.MGMT_WEBAPP.RUNNING_PROPERTY: node_status.grafanaRunning,
            api_constants.MGMT_WEBAPP.PORT_PROPERTY: constants.COMMANDS.GRAFANA_PORT,
            api_constants.MGMT_WEBAPP.URL_PROPERTY: f"http://{node.ip}:{constants.COMMANDS.GRAFANA_PORT}/",
            api_constants.MGMT_WEBAPP.IP_PROPERTY: node.ip
        }
        grafana_statuses.append(grafana_dict)
    response = jsonify(grafana_statuses)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
