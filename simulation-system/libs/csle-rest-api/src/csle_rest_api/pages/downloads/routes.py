"""
Routes and resources for the /downloads-page page
"""
from flask import Blueprint
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants

# Creates a blueprint "sub application" of the main REST app
downloads_page_bp = Blueprint(
    api_constants.MGMT_WEBAPP.DOWNLOADS_PAGE_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.DOWNLOADS_PAGE_RESOURCE}",
    static_url_path=f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.DOWNLOADS_PAGE_RESOURCE}'
                    f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.STATIC}',
    static_folder="../../../../../../management-system/csle-mgmt-webapp/build")


@downloads_page_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def downloads_page():
    """
    :return: static resources for the /downloads-page url
    """
    return downloads_page_bp.send_static_file(api_constants.MGMT_WEBAPP.STATIC_RESOURCE_INDEX)
