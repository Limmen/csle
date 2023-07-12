"""
Routes and sub-resources for the /training-jobs resource
"""
from typing import Tuple
import time
import csle_common.constants.constants as constants
from csle_agents.job_controllers.training_job_manager import TrainingJobManager
from csle_cluster.cluster_manager.cluster_controller import ClusterController
from csle_common.metastore.metastore_facade import MetastoreFacade
from flask import Blueprint, jsonify, request, Response
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util

# Creates a blueprint "sub application" of the main REST app
training_jobs_bp = Blueprint(
    api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}")


@training_jobs_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                     api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def training_jobs() -> Tuple[Response, int]:
    """
    The /training-jobs resource.

    :return: A list of training-jobs or a list of ids of the jobs or deletes the jobs
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
        # Check if ids query parameter is True, then only return the ids and not the whole list of training jobs
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return training_jobs_ids()

        training_jobs = MetastoreFacade.list_training_jobs()
        alive_jobs = []
        for job in training_jobs:
            if ClusterController.check_pid(ip=job.physical_host_ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                                           pid=job.pid).outcome:
                job.running = True
            alive_jobs.append(job)
        training_jobs_dicts = list(map(lambda x: x.to_dict(), alive_jobs))
        response = jsonify(training_jobs_dicts)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        jobs = MetastoreFacade.list_training_jobs()
        for job in jobs:
            ClusterController.stop_pid(ip=job.physical_host_ip,
                                       port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, pid=job.pid)
            MetastoreFacade.remove_training_job(training_job=job)
        time.sleep(2)
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: "HTTP method not supported"}),
            constants.HTTPS.BAD_REQUEST_STATUS_CODE)


def training_jobs_ids() -> Tuple[Response, int]:
    """
    :return: An HTTP response with all training jobs ids
    """
    training_jobs = MetastoreFacade.list_training_jobs()
    response_dicts = []
    for job in training_jobs:
        response_dicts.append({
            api_constants.MGMT_WEBAPP.ID_PROPERTY: job.id,
            api_constants.MGMT_WEBAPP.SIMULATION_PROPERTY: job.simulation_env_name,
            api_constants.MGMT_WEBAPP.EMULATION_PROPERTY: job.emulation_env_name,
            api_constants.MGMT_WEBAPP.RUNNING_PROPERTY: ClusterController.check_pid(
                ip=job.physical_host_ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, pid=job.pid).outcome
        })
    response = jsonify(response_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@training_jobs_bp.route("/<job_id>", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                              api_constants.MGMT_WEBAPP.HTTP_REST_DELETE,
                                              api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def training_policy(job_id: int) -> Tuple[Response, int]:
    """
    The /training-jobs/id resource.

    :param job_id: the id of the policy

    :return: The given policy or deletes the policy
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE or \
            request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    job = MetastoreFacade.get_training_job_config(id=job_id)
    response = jsonify({})

    if job is not None:
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            if ClusterController.check_pid(ip=job.physical_host_ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                                           pid=job.pid).outcome:
                job.running = True
            response = jsonify(job.to_dict())
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            ClusterController.stop_pid(ip=job.physical_host_ip,
                                       port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, pid=job.pid)
            MetastoreFacade.remove_training_job(training_job=job)
            time.sleep(2)
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
            start = True
            stop = request.args.get(api_constants.MGMT_WEBAPP.STOP_QUERY_PARAM)
            if stop is not None and stop:
                start = False
            if start:
                TrainingJobManager.start_training_job_in_background(training_job=job)
                time.sleep(2)
            else:
                ClusterController.stop_pid(ip=job.physical_host_ip,
                                           port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, pid=job.pid)
                time.sleep(2)

    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
