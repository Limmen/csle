"""
Routes and sub-resources for the /traces-datasets resource
"""
from typing import Tuple
import os
from flask import Blueprint, Response, jsonify, request, send_from_directory
import csle_common.constants.constants as constants
from csle_common.dao.datasets.traces_dataset import TracesDataset
from csle_common.metastore.metastore_facade import MetastoreFacade
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util

# Creates a blueprint "sub application" of the main REST app
traces_datasets_bp = Blueprint(
    api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.TRACES_DATASETS_RESOURCE}")


@traces_datasets_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                       api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def traces_datasets() -> Tuple[Response, int]:
    """
    The /traces-datasets resource.

    :return: A list of traces datasets or a list of ids of the traces datasets or deletes the datasets
    """
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
        if authorized is not None:
            return authorized

    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
        # Check if ids query parameter is True, then only return the ids and not the whole list of traces
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return traces_datasets_ids()

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
    return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: "HTTP method not supported"}),
            constants.HTTPS.BAD_REQUEST_STATUS_CODE)


def traces_datasets_ids() -> Tuple[Response, int]:
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


@traces_datasets_bp.route("/<traces_dataset_id>", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                                           api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def traces_dataset(traces_dataset_id: int) -> Tuple[Response, int]:
    """
    The /traces-datasets/id resource.

    :param traces_dataset_id: the id of the traces dataset
    :return: The given traces dataset or deletes the traces dataset
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
            # Check if download query parameter is True, then return the file
            download = request.args.get(api_constants.MGMT_WEBAPP.DOWNLOAD_QUERY_PARAM)
            if download is not None and download:
                return download_dataset_file(traces_dataset)
            else:
                response = jsonify(traces_dataset.to_dict())
        else:
            MetastoreFacade.remove_traces_dataset(traces_dataset)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


def download_dataset_file(traces_dataset: TracesDataset) -> Tuple[Response, int]:
    """
    Downloads a dataset file

    :param traces_dataset: the dataset file to download
    :return: the HTTP response
    """
    if traces_dataset.file_path is not None and traces_dataset.file_path != "":
        dir_filename = os.path.split(traces_dataset.file_path)
        dir = dir_filename[0]
        filename = dir_filename[1]
        traces_dataset.download_count = traces_dataset.download_count + 1
        MetastoreFacade.update_traces_dataset(traces_dataset=traces_dataset, id=traces_dataset.id)
        try:
            return send_from_directory(dir, filename, as_attachment=True), constants.HTTPS.OK_STATUS_CODE
        except FileNotFoundError:
            response = jsonify({})
            return response, constants.HTTPS.NOT_FOUND_STATUS_CODE
    else:
        response = jsonify({})
        return response, constants.HTTPS.NOT_FOUND_STATUS_CODE
