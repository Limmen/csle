"""
Routes and sub-resources for the /experiments resource
"""
from flask import Blueprint, jsonify, request
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_common.metastore.metastore_facade import MetastoreFacade
import csle_rest_api.util.rest_api_util as rest_api_util

# Creates a blueprint "sub application" of the main REST app
experiments_bp = Blueprint(
    api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}")


@experiments_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def experiments():
    """
    The /experiments resource.

    :return: A list of experiments or a list of ids of the experiments or deletes the experiments
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
        # Check if ids query parameter is True, then only return the ids and not the whole list of experiments
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return experiments_ids()

        experiments = MetastoreFacade.list_experiment_executions()
        experiment_dicts = list(map(lambda x: x.to_dict(), experiments))
        response = jsonify(experiment_dicts)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        experiments = MetastoreFacade.list_experiment_executions()
        for exp in experiments:
            MetastoreFacade.remove_experiment_execution(experiment_execution=exp)
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE


def experiments_ids():
    """
    :return: An HTTP response with all experiments ids
    """
    experiments_ids = MetastoreFacade.list_experiment_executions_ids()
    response_dicts = []
    for tup in experiments_ids:
        response_dicts.append({
            api_constants.MGMT_WEBAPP.ID_PROPERTY: tup[0],
            api_constants.MGMT_WEBAPP.SIMULATION_PROPERTY: tup[1],
            api_constants.MGMT_WEBAPP.EMULATION_PROPERTY: tup[2]
        })
    response = jsonify(response_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@experiments_bp.route("/<experiment_id>", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                                   api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def experiment(experiment_id: int):
    """
    The /experiments/id resource.

    :param experiment_id: the id of the experiment

    :return: The given experiment or deletes the experiment
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    experiment = MetastoreFacade.get_experiment_execution(id=experiment_id)
    response = jsonify({})
    if experiment is not None:
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            response = jsonify(experiment.to_dict())
        else:
            MetastoreFacade.remove_experiment_execution(experiment_execution=experiment)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
