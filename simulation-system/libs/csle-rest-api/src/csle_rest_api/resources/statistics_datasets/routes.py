"""
Routes and sub-resources for the /statistics-datasets resource
"""
import os
from typing import Tuple
from flask import Blueprint, Response, jsonify, request, send_from_directory
import csle_common.constants.constants as constants
from csle_common.dao.datasets.statistics_dataset import StatisticsDataset
from csle_common.metastore.metastore_facade import MetastoreFacade
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util

# Creates a blueprint "sub application" of the main REST app
statistics_datasets_bp = Blueprint(
    api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.STATISTICS_DATASETS_RESOURCE}")


@statistics_datasets_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                           api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def statistics_datasets() -> Tuple[Response, int]:
    """
    The /statistics-datasets resource.

    :return: A list of statistics datasets or a list of ids of the statistics datasets or deletes the datasets
    """
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=True)
        if authorized is not None:
            return authorized

    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
        # Check if ids query parameter is True, then only return the ids and not the whole list of statistics datasets
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return statistics_datasets_ids()

        statistics_datasets = MetastoreFacade.list_statistics_datasets()
        statistics_dicts = list(map(lambda x: x.to_dict(), statistics_datasets))
        response = jsonify(statistics_dicts)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        statistics_datasets = MetastoreFacade.list_statistics_datasets()
        for statistics_dataset in statistics_datasets:
            MetastoreFacade.remove_statistics_dataset(statistics_dataset)
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: "HTTP method not supported"}),
            constants.HTTPS.BAD_REQUEST_STATUS_CODE)


def statistics_datasets_ids() -> Tuple[Response, int]:
    """
    :return: An HTTP response with all statistics datasets ids
    """
    ids_statistics_datasets = MetastoreFacade.list_statistics_datasets_ids()
    response_dicts = []
    for tup in ids_statistics_datasets:
        response_dicts.append({
            api_constants.MGMT_WEBAPP.ID_PROPERTY: tup[0],
            api_constants.MGMT_WEBAPP.STATISTICS_DATASET_PROPERTY: tup[1]
        })
    response = jsonify(response_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@statistics_datasets_bp.route("/<statistics_dataset_id>", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                                                   api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def statistics_dataset(statistics_dataset_id: int) -> Tuple[Response, int]:
    """
    The /statistics-datasets/id resource.

    :param statistics_dataset_id: the id of the statistics dataset
    :return: The given statistics dataset or deletes the statistics dataset
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    statistics_dataset = MetastoreFacade.get_statistics_dataset_metadata(id=statistics_dataset_id)
    response = jsonify({})
    if statistics_dataset is not None:
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            # Check if download query parameter is True, then return the file
            download = request.args.get(api_constants.MGMT_WEBAPP.DOWNLOAD_QUERY_PARAM)
            if download is not None and download:
                return download_dataset_file(statistics_dataset)
            else:
                response = jsonify(statistics_dataset.to_dict())
        else:
            MetastoreFacade.remove_statistics_dataset(statistics_dataset)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


def download_dataset_file(statistics_dataset: StatisticsDataset) -> Tuple[Response, int]:
    """
    Downloads a dataset file

    :param statistics_dataset: the dataset file to download
    :return: the HTTP response
    """
    if statistics_dataset.file_path is not None and statistics_dataset.file_path != "":
        dir_filename = os.path.split(statistics_dataset.file_path)
        dir = dir_filename[0]
        filename = dir_filename[1]
        statistics_dataset.download_count = statistics_dataset.download_count + 1
        MetastoreFacade.update_statistics_dataset(statistics_dataset=statistics_dataset, id=statistics_dataset.id)
        try:
            return send_from_directory(dir, filename, as_attachment=True), constants.HTTPS.OK_STATUS_CODE
        except FileNotFoundError:
            response = jsonify({})
            return response, constants.HTTPS.NOT_FOUND_STATUS_CODE
    else:
        response = jsonify({})
        return response, constants.HTTPS.NOT_FOUND_STATUS_CODE
