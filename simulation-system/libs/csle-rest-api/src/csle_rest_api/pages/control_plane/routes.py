"""
Routes and resources for the /control-plane-page page
"""
from flask import Blueprint
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants


def get_control_plane_page_bp(static_folder: str) -> Blueprint:
    """
    Creates a blueprint "sub application" of the main REST app that represents the control plane page

    :param static_folder: the folder with the static resources
    :return: the created blueprint
    """
    # Creates a blueprint "sub application" of the main REST app
    control_plane_page_bp = Blueprint(api_constants.MGMT_WEBAPP.CONTROL_PLANE_PAGE_RESOURCE, __name__,
                                      url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                                 f"{api_constants.MGMT_WEBAPP.CONTROL_PLANE_PAGE_RESOURCE}",
                                      static_url_path=f'{constants.COMMANDS.SLASH_DELIM}'
                                                      f'{api_constants.MGMT_WEBAPP.CONTROL_PLANE_PAGE_RESOURCE}'
                                                      f'{constants.COMMANDS.SLASH_DELIM}'
                                                      f'{api_constants.MGMT_WEBAPP.STATIC}',
                                      static_folder=static_folder)

    @control_plane_page_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
    def control_plane_page():
        """
        :return: static resources for the /control-plane-page url
        """
        return control_plane_page_bp.send_static_file(api_constants.MGMT_WEBAPP.STATIC_RESOURCE_INDEX)

    return control_plane_page_bp
