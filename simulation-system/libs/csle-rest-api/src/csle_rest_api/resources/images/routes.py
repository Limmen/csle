"""
Routes and sub-resources for the /images resource
"""

from typing import List, Tuple
from flask import Blueprint, Response, jsonify, request
import csle_common.constants.constants as constants
from csle_cluster.cluster_manager.cluster_controller import ClusterController
from csle_cluster.cluster_manager.cluster_manager_pb2 import ContainerImageDTO
from csle_common.metastore.metastore_facade import MetastoreFacade
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util

# Creates a blueprint "sub application" of the main REST app
images_bp = Blueprint(
    api_constants.MGMT_WEBAPP.IMAGES_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.IMAGES_RESOURCE}")


@images_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def images() -> Tuple[Response, int]:
    """
    The /images resource

    :return: Returns a list of images
    """
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=False)
    if authorized is not None:
        return authorized
    config = MetastoreFacade.get_config(id=1)
    images: List[ContainerImageDTO] = []
    for node in config.cluster_config.cluster_nodes:
        images_dto = ClusterController.list_all_container_images(
            ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        images_dtos = list(images_dto.images)
        images = images + images_dtos
    images_dicts = []
    for img in images:
        images_dicts.append(
            {
                api_constants.MGMT_WEBAPP.NAME_PROPERTY: img.repoTags,
                api_constants.MGMT_WEBAPP.SIZE_PROPERTY: img.size
            }
        )
    response = jsonify(images_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
