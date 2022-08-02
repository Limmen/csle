"""
Routes and sub-resources for the /traces-datasets resource
"""
from flask import Blueprint, jsonify, request
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_common.metastore.metastore_facade import MetastoreFacade
import csle_rest_api.util.rest_api_util as rest_api_util


# Creates a blueprint "sub application" of the main REST app
traces_datasets_bp = Blueprint(
    api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}")


@traces_datasets_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                       api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def trace_datasets():
    """
    The /traces-datasets resource.

    :return: A list of traces datasets or a list of ids of the traces datasets or deletes the datasets
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
        # Check if ids query parameter is True, then only return the ids and not the whole dataset
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return trace_datasets_ids()

        traces_datasets = MetastoreFacade.list_traces_datasets()
        traces_dicts = list(map(lambda x: x.to_dict(), traces_datasets))
        response = jsonify(traces_dicts)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        traces_datasets = MetastoreFacade.list_traces_datasets()
        for traces_dataset in traces_datasets:
            MetastoreFacade.remove_traces_dataset(traces_dataset)
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE


def trace_datasets_ids():
    """
    :return: An HTTP response with all traces datasets ids
    """
    ids_traces_datasets = MetastoreFacade.list_traces_datasets_ids()
    response_dicts = []
    for tup in ids_traces_datasets:
        response_dicts.append({
            api_constants.MGMT_WEBAPP.ID_PROPERTY: tup[0],
            api_constants.MGMT_WEBAPP.TRACES_DATASET_PROPERTY: tup[1]
        })
    response = jsonify(response_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@traces_datasets_bp.route("/<trace_id>", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                                  api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def trace_dataset(traces_dataset_id: int):
    """
    The /traces-datasets/id resource.

    :param traces_dataset_id: the id of the trace

    :return: The given trace or delets the trace
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    traces_dataset = MetastoreFacade.get_traces_dataset_metadata(id=traces_dataset_id)
    response = jsonify({})
    if traces_dataset is not None:
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            response = jsonify(traces_dataset.to_dict())
        else:
            MetastoreFacade.remove_traces_dataset(traces_dataset)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE