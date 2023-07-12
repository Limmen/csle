"""
Routes and resources for the /server-cluster-page page
"""
from typing import Tuple
from flask import Blueprint, Response
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants


def get_server_cluster_page_bp(static_folder: str) -> Blueprint:
    """
    Creates a blueprint "sub application" of the main REST app that represents the server-cluster page

    :param static_folder: the folder with the static resources
    :return: the created blueprint
    """
    # Creates a blueprint "sub application" of the main REST app
    server_cluster_page_bp = Blueprint(
        api_constants.MGMT_WEBAPP.SERVER_CLUSTER_PAGE_RESOURCE, __name__,
        url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.SERVER_CLUSTER_PAGE_RESOURCE}",
        static_url_path=f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.SERVER_CLUSTER_PAGE_RESOURCE}'
                        f'{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.STATIC}',
        static_folder=static_folder)

    @server_cluster_page_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
    def server_cluster_page() -> Tuple[Response, int]:
        """
        :return: static resources for the /server-cluster-page url
        """
        return (server_cluster_page_bp.send_static_file(api_constants.MGMT_WEBAPP.STATIC_RESOURCE_INDEX),
                constants.HTTPS.OK_STATUS_CODE)

    return server_cluster_page_bp
