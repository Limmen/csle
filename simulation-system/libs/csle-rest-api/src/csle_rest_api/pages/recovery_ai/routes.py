"""
Routes and resources for the /recovery-ai-page page
"""
from typing import Tuple
from flask import Blueprint, Response
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants


def get_recovery_ai_page_bp(static_folder: str) -> Blueprint:
    """
    Creates a blueprint "sub application" of the main REST app that represents the recovery-ai page

    :param static_folder: the folder with the static resources
    :return: the created blueprint
    """
    # Creates a blueprint "sub application" of the main REST app
    recovery_ai_page_bp = Blueprint(
        api_constants.MGMT_WEBAPP.RECOVERY_AI_PAGE_RESOURCE, __name__,
        url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.RECOVERY_AI_PAGE_RESOURCE}",
        static_url_path=f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.RECOVERY_AI_PAGE_RESOURCE}'
                        f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.STATIC}',
        static_folder=static_folder)

    @recovery_ai_page_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
    def recovery_ai_page_page() -> Tuple[Response, int]:
        """
        :return: static resources for the /recovery-ai-page url
        """
        return (recovery_ai_page_bp.send_static_file(api_constants.MGMT_WEBAPP.STATIC_RESOURCE_INDEX),
                constants.HTTPS.OK_STATUS_CODE)

    return recovery_ai_page_bp
