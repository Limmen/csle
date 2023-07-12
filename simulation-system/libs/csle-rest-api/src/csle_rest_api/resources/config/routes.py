"""
Routes and sub-resources for the /config resource
"""
from typing import Tuple
import json
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.config import Config
from csle_common.logging.log import Logger
from csle_common.util.cluster_util import ClusterUtil
from flask import Blueprint, jsonify, request, Response
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util

# Creates a blueprint "sub application" of the main REST app
config_bp = Blueprint(
    api_constants.MGMT_WEBAPP.CONFIG_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.CONFIG_RESOURCE}")


@config_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_PUT])
def config() -> Tuple[Response, int]:
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
        if api_constants.MGMT_WEBAPP.CONFIG_PROPERTY not in json_data:
            response_str = f"{api_constants.MGMT_WEBAPP.CONFIG_PROPERTY} not provided"
            return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: response_str}),
                    constants.HTTPS.BAD_REQUEST_STATUS_CODE)
        config = json_data[api_constants.MGMT_WEBAPP.CONFIG_PROPERTY]
        if not (api_constants.MGMT_WEBAPP.PARAMETERS_PROPERTY in config and
                api_constants.MGMT_WEBAPP.CLUSTER_CONFIG_PROPERTY in config):
            return config, constants.HTTPS.BAD_REQUEST_STATUS_CODE
        found_param_names = []
        for i in range((len(config[api_constants.MGMT_WEBAPP.PARAMETERS_PROPERTY]))):
            found_param_names.append(config[api_constants.MGMT_WEBAPP.PARAMETERS_PROPERTY][i]
                                     [api_constants.MGMT_WEBAPP.PARAM_RESOURCE])
        std_param_names = Config.get_std_param_names()

        for name in std_param_names:
            if name not in found_param_names:
                return config, constants.HTTPS.BAD_REQUEST_STATUS_CODE
        config = Config.from_param_dict(config)
        Config.save_config_file(config=config.to_dict())
        ClusterUtil.set_config_parameters_from_config_file()
        response = jsonify(config.to_param_dict())
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: "HTTP method not supported"}),
            constants.HTTPS.BAD_REQUEST_STATUS_CODE)


@config_bp.route(f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.REGISTRATION_ALLOWED_SUBRESOURCE}",
                 methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def registration_allowed() -> Tuple[Response, int]:
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
