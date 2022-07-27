from flask import jsonify
import csle_common.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade
import csle_rest_api.constants.constants as api_constants


def check_if_user_is_authorized(request):
    """
    Checks if a user request is authorized

    :param request: the request to check
    :return: the non-authorized response or None
    """
    # Extract token and check if user is authorized
    token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
    token_obj = MetastoreFacade.get_session_token_metadata(token=token)
    if token_obj == None or token_obj.expired(valid_length_hours=api_constants.SESSION_TOKENS.EXPIRE_TIME_HOURS):
        if token_obj is not None:
            MetastoreFacade.remove_session_token(session_token=token_obj)
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.UNAUTHORIZED_STATUS_CODE
    else:
        return None