"""
Routes and sub-resources for the /system-models resource
"""
from typing import Tuple
import csle_common.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from flask import Blueprint, jsonify, request, Response
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util

# Creates a blueprint "sub application" of the main REST app
system_models_bp = Blueprint(
    api_constants.MGMT_WEBAPP.SYSTEM_MODELS_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.SYSTEM_MODELS_RESOURCE}")


@system_models_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def system_models() -> Tuple[Response, int]:
    """
    The /system-models resource.

    :return: A list of system-models or a list of ids of the models or deletes the models
    """

    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=False)
    if authorized is not None:
        return authorized
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
        # Check if ids query parameter is True, then only return the ids and not the whole list of system models
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return system_models_ids()
        else:
            response = jsonify({})
            response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: "HTTP method not supported"}),
            constants.HTTPS.BAD_REQUEST_STATUS_CODE)


def system_models_ids() -> Tuple[Response, int]:
    """
    :return: An HTTP response with all system models ids
    """
    response_dicts = []
    gaussian_mixture_system_models_ids = MetastoreFacade.list_gaussian_mixture_system_models_ids()
    for tup in gaussian_mixture_system_models_ids:
        response_dicts.append({
            api_constants.MGMT_WEBAPP.ID_PROPERTY: tup[0],
            api_constants.MGMT_WEBAPP.EMULATION_PROPERTY: tup[1],
            api_constants.MGMT_WEBAPP.STATISTIC_ID_PROPERTY: tup[2],
            api_constants.MGMT_WEBAPP.SYSTEM_MODEL_TYPE: api_constants.MGMT_WEBAPP.GAUSSIAN_MIXTURE_SYSTEM_MODEL_TYPE
        })
    empirical_system_models_ids = MetastoreFacade.list_empirical_system_models_ids()
    for tup in empirical_system_models_ids:
        response_dicts.append({
            api_constants.MGMT_WEBAPP.ID_PROPERTY: tup[0],
            api_constants.MGMT_WEBAPP.EMULATION_PROPERTY: tup[1],
            api_constants.MGMT_WEBAPP.STATISTIC_ID_PROPERTY: tup[2],
            api_constants.MGMT_WEBAPP.SYSTEM_MODEL_TYPE: api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODEL_TYPE
        })
    gp_system_models_ids = MetastoreFacade.list_gp_system_models_ids()
    for tup in gp_system_models_ids:
        response_dicts.append({
            api_constants.MGMT_WEBAPP.ID_PROPERTY: tup[0],
            api_constants.MGMT_WEBAPP.EMULATION_PROPERTY: tup[1],
            api_constants.MGMT_WEBAPP.STATISTIC_ID_PROPERTY: tup[2],
            api_constants.MGMT_WEBAPP.SYSTEM_MODEL_TYPE: api_constants.MGMT_WEBAPP.GP_SYSTEM_MODEL_TYPE
        })
    mcmc_system_models_ids = MetastoreFacade.list_mcmc_system_models_ids()
    for tup in mcmc_system_models_ids:
        response_dicts.append({
            api_constants.MGMT_WEBAPP.ID_PROPERTY: tup[0],
            api_constants.MGMT_WEBAPP.EMULATION_PROPERTY: tup[1],
            api_constants.MGMT_WEBAPP.STATISTIC_ID_PROPERTY: tup[2],
            api_constants.MGMT_WEBAPP.SYSTEM_MODEL_TYPE: api_constants.MGMT_WEBAPP.MCMC_SYSTEM_MODEL_TYPE
        })
    response = jsonify(response_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
