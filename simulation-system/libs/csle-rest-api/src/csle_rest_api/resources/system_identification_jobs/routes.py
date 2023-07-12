"""
Routes and sub-resources for the /system-identification-jobs resource
"""
from typing import Tuple
import time
import csle_common.constants.constants as constants
from csle_cluster.cluster_manager.cluster_controller import ClusterController
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_system_identification.job_controllers.system_identification_job_manager import SystemIdentificationJobManager
from flask import Blueprint, jsonify, request, Response
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util

# Creates a blueprint "sub application" of the main REST app
system_identification_jobs_bp = Blueprint(
    api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.SYSTEM_IDENTIFICATION_JOBS_RESOUCE}")


@system_identification_jobs_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                                  api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def system_identification_jobs() -> Tuple[Response, int]:
    """
    The /system-identification-jobs resource.

    :return: A list of system-identification-jobs or a list of ids of the jobs or deletes the jobs
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
        # Check if ids query parameter is True, then only return the ids and not the whole list of
        # system identification jobs
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return system_identification_jobs_ids()

        system_identification_jobs = MetastoreFacade.list_system_identification_jobs()
        alive_jobs = []
        for job in system_identification_jobs:
            if ClusterController.check_pid(ip=job.physical_host_ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                                           pid=job.pid).outcome:
                job.running = True
            alive_jobs.append(job)
        system_identification_jobs_dicts = list(map(lambda x: x.to_dict(), alive_jobs))
        response = jsonify(system_identification_jobs_dicts)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        jobs = MetastoreFacade.list_system_identification_jobs()
        for job in jobs:
            ClusterController.stop_pid(ip=job.physical_host_ip,
                                       port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, pid=job.pid)
            MetastoreFacade.remove_system_identification_job(system_identification_job=job)
        time.sleep(2)
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response, constants.HTTPS.OK_STATUS_CODE
    return (jsonify({api_constants.MGMT_WEBAPP.REASON_PROPERTY: "HTTP method not supported"}),
            constants.HTTPS.BAD_REQUEST_STATUS_CODE)


def system_identification_jobs_ids() -> Tuple[Response, int]:
    """
    :return: An HTTP response with all system-identification jobs ids
    """
    system_identification_jobs = MetastoreFacade.list_system_identification_jobs()
    response_dicts = []
    for job in system_identification_jobs:
        response_dicts.append({
            api_constants.MGMT_WEBAPP.ID_PROPERTY: job.id,
            api_constants.MGMT_WEBAPP.EMULATION_PROPERTY: job.emulation_env_name,
            api_constants.MGMT_WEBAPP.RUNNING_PROPERTY: ClusterController.check_pid(
                ip=job.physical_host_ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, pid=job.pid).outcome
        })
    response = jsonify(response_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@system_identification_jobs_bp.route("/<job_id>", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                                           api_constants.MGMT_WEBAPP.HTTP_REST_DELETE,
                                                           api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def system_identification_policy(job_id: int) -> Tuple[Response, int]:
    """
    The /system-identification-jobs/id resource.

    :param job_id: the id of the policy

    :return: The given policy or deletes the policy
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized

    job = MetastoreFacade.get_system_identification_job_config(id=job_id)
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
            MetastoreFacade.remove_system_identification_job(system_identification_job=job)
            time.sleep(2)
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
            start = True
            stop = request.args.get(api_constants.MGMT_WEBAPP.STOP_QUERY_PARAM)
            if stop is not None and stop:
                start = False
            if start:
                SystemIdentificationJobManager.start_system_identification_job_in_background(
                    system_identification_job=job)
                time.sleep(4)
            else:
                ClusterController.stop_pid(ip=job.physical_host_ip,
                                           port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, pid=job.pid)
                time.sleep(2)

    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
