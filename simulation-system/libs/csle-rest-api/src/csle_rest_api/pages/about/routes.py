"""
Routes and resources for the /about-page page
"""
from flask import Blueprint
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants


def get_about_page_bp(static_folder: str) -> Blueprint:
    """
    Creates a blueprint "sub application" of the main REST app that represents the about page

    :param static_folder: the folder with the static resources
    :return: the created blueprint
    """
    # Creates a blueprint "sub application" of the main REST app
    about_page_bp = Blueprint(
        api_constants.MGMT_WEBAPP.ABOUT_PAGE_RESOURCE, __name__,
        url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.ABOUT_PAGE_RESOURCE}",
        static_url_path=f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.ABOUT_PAGE_RESOURCE}'
                        f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.STATIC}',
        static_folder=static_folder)

    @about_page_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
    def about_page():
        """
        :return: static resources for the /about-page url
        """
        return about_page_bp.send_static_file(api_constants.MGMT_WEBAPP.STATIC_RESOURCE_INDEX)

    return about_page_bp
