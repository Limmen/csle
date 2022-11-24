"""
Routes and sub-resources for the /images resource
"""
from flask import Blueprint, jsonify, request
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_common.controllers.container_controller import ContainerController
import csle_rest_api.util.rest_api_util as rest_api_util


# Creates a blueprint "sub application" of the main REST app
images_bp = Blueprint(
    api_constants.MGMT_WEBAPP.IMAGES_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.IMAGES_RESOURCE}")


@images_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def images():
    """
    The /images resource

    :return: Returns a list of images
    """
    authorized = rest_api_util.check_if_user_is_authorized(request=request)
    if authorized is not None:
        return authorized

    images = ContainerController.list_all_images()
    images_dicts = []
    for img in images:
        images_dicts.append(
            {
                api_constants.MGMT_WEBAPP.NAME_PROPERTY: img[0],
                api_constants.MGMT_WEBAPP.SIZE_PROPERTY: img[4]
            }
        )
    response = jsonify(images_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
