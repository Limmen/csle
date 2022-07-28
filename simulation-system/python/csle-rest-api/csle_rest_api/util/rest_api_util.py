from flask import jsonify
import csle_common.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade
import csle_rest_api.constants.constants as api_constants


def check_if_user_is_authorized(request, requires_admin: bool = False):
    """
    Checks if a user request is authorized

    :param request: the request to check
    :param requires_admin: boolean flag indicating whether only admins are authorized or not
    :return: the non-authorized response or None
    """
    # Extract token and check if user is authorized
    token = request.args.get(api_constants.MGMT_WEBAPP.TOKEN_QUERY_PARAM)
    token_obj = MetastoreFacade.get_session_token_metadata(token=token)
    user = None
    if requires_admin:
        user = MetastoreFacade.get_management_user_by_username(username=token_obj.username)
    if token_obj == None or token_obj.expired(valid_length_hours=api_constants.SESSION_TOKENS.EXPIRE_TIME_HOURS) \
            or (requires_admin and user is not None and not user.admin):
        if token_obj is not None:
            MetastoreFacade.remove_session_token(session_token=token_obj)
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.UNAUTHORIZED_STATUS_CODE
    else:
        return None