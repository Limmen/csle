"""
Routes and sub-resources for the /config resource
"""
from flask import Blueprint, jsonify, request
import json
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util
from csle_common.dao.emulation_config.config import Config
from csle_common.logging.log import Logger


# Creates a blueprint "sub application" of the main REST app
config_bp = Blueprint(
    api_constants.MGMT_WEBAPP.CONFIG_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.CONFIG_RESOURCE}")


@config_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                              api_constants.MGMT_WEBAPP.HTTP_REST_PUT])
def config():
    """
    The /config resource.

    :return: The CSLE configuration
    """
    requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
        try:
            config = Config.read_config_file()
            response = jsonify(config.to_param_dict())
        except Exception as e:
            Logger.__call__().get_logger().info(f"There was an error reading the config file: {str(e)}, {repr(e)}")
            response = jsonify({})
            return response, constants.HTTPS.INTERNAL_SERVER_ERROR_STATUS_CODE
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_PUT:
        json_data = json.loads(request.data)
        # Verify payload
        if api_constants.MGMT_WEBAPP.CONFIG_RESOURCE not in json_data:
            return jsonify({}), constants.HTTPS.BAD_REQUEST_STATUS_CODE
        config = json_data[api_constants.MGMT_WEBAPP.CONFIG_PROPERTY]
        config = Config.from_param_dict(config)
        Config.save_config_file(config=config.to_dict())
        Config.set_config_parameters_from_config_file()
        response = jsonify(config.to_param_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE


@config_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.REGISTRATION_ALLOWED_SUBRESOURCE}",
                 methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def registration_allowed():
    """
    The /config/registration-allowed resource.

    :return: The CSLE configuration
    """
    allow_registration = False
    if constants.CONFIG_FILE.PARSED_CONFIG is not None and constants.CONFIG_FILE.PARSED_CONFIG.allow_registration:
        allow_registration = True
    response_dict = {}
    response_dict[api_constants.MGMT_WEBAPP.REGISTRATION_ALLOWED_PROPERTY] = allow_registration
    response = jsonify(response_dict)
    return response, constants.HTTPS.OK_STATUS_CODE


@config_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.HOST_TERMINAL_ALLOWED_SUBRESOURCE}",
                 methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def host_terminal_allowed():
    """
    The /config/host-terminal-allowed resource.

    :return: The CSLE configuration
    """
    allow_host_terminal = False
    if constants.CONFIG_FILE.PARSED_CONFIG is not None and constants.CONFIG_FILE.PARSED_CONFIG.allow_host_shell:
        allow_host_terminal = True
    response_dict = {}
    response_dict[api_constants.MGMT_WEBAPP.HOST_TERMINAL_ALLOWED_PROPERTY] = allow_host_terminal
    response = jsonify(response_dict)
    return response, constants.HTTPS.OK_STATUS_CODE
