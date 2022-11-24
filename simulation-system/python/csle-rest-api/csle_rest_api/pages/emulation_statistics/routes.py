"""
Routes and resources for the /emulation-statistics-page page
"""

from flask import Blueprint
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants


# Creates a blueprint "sub application" of the main REST app
emulation_statistics_page_bp = Blueprint(
    api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_PAGE_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_PAGE_RESOURCE}",
    static_url_path=f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.EMULATION_STATISTICS_PAGE_RESOURCE}'
                    f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.STATIC}',
    static_folder="../../../../../../management-system/csle-mgmt-webapp/build")


@emulation_statistics_page_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def emulation_statistics_page():
    """
    :return: static resources for the /emulation-statistics-page url
    """
    return emulation_statistics_page_bp.send_static_file(api_constants.MGMT_WEBAPP.STATIC_RESOURCE_INDEX)
