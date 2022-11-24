"""
Routes and resources for the /sdn-controllers-page page
"""
from flask import Blueprint
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants


# Creates a blueprint "sub application" of the main REST app
sdn_controllers_page_bp = Blueprint(api_constants.MGMT_WEBAPP.SDN_CONTROLLERS_PAGE_RESOURCE, __name__,
                                    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                               f"{api_constants.MGMT_WEBAPP.SDN_CONTROLLERS_PAGE_RESOURCE}",
                                    static_url_path=f'{constants.COMMANDS.SLASH_DELIM}'
                                                    f'{api_constants.MGMT_WEBAPP.SDN_CONTROLLERS_PAGE_RESOURCE}'
                                                    f'{constants.COMMANDS.SLASH_DELIM}'
                                                    f'{api_constants.MGMT_WEBAPP.STATIC}',
                                    static_folder="../../../../../../management-system/csle-mgmt-webapp/build")


@sdn_controllers_page_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def sdn_controllers_page():
    """
    :return: static resources for the /sdn-controllers-page url
    """
    return sdn_controllers_page_bp.send_static_file(api_constants.MGMT_WEBAPP.STATIC_RESOURCE_INDEX)
