import csle_collector.elk_manager.elk_manager_pb2_grpc
import csle_collector.elk_manager.elk_manager_pb2
import csle_collector.constants.constants as constants


def get_elk_status(stub: csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub,
                   timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
    """
    Queries the server for the ELK stack status

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an ElkDTO describing the status of the ELK stack
    """
    get_elk_status_msg = csle_collector.elk_manager.elk_manager_pb2.GetElkStatusMsg()
    elk_dto = stub.getElkStatus(get_elk_status_msg, timeout=timeout)
    return elk_dto


def stop_elk(stub: csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub,
             timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
    """
    Sends a request to the ELK server to stop the whole ELK stack

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an ElkDTO describing the status of the ELK stack
    """
    stop_elk_msg = csle_collector.elk_manager.elk_manager_pb2.StopElkMsg()
    elk_dto = stub.stopElk(stop_elk_msg, timeout=timeout)
    return elk_dto


def start_elk(stub: csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub,
              timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
    """
    Sends a request to the ELK server to start the ELK stack

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an ElkDTO describing the status of the ELK server
    """
    start_elk_msg = csle_collector.elk_manager.elk_manager_pb2.StartElkMsg()
    elk_dto = stub.startElk(start_elk_msg, timeout=timeout)
    return elk_dto


def stop_elastic(stub: csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub,
                 timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
    """
    Sends a request to the ELK server to stop Elabticsearch

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an ElkDTO describing the status of the ELK stack
    """
    stop_elastic_msg = csle_collector.elk_manager.elk_manager_pb2.StopElasticMsg()
    elk_dto = stub.stopElastic(stop_elastic_msg, timeout=timeout)
    return elk_dto


def start_elastic(stub: csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub,
                  timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
    """
    Sends a request to the ELK server to start Elasticsearch

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an ElkDTO describing the status of the ELK server
    """
    start_elastic_msg = csle_collector.elk_manager.elk_manager_pb2.StartElkMsg()
    elk_dto = stub.startElastic(start_elastic_msg, timeout=timeout)
    return elk_dto


def stop_kibana(stub: csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub,
                timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
    """
    Sends a request to the ELK server to stop Kibana

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an ElkDTO describing the status of the ELK stack
    """
    stop_kibana_msg = csle_collector.elk_manager.elk_manager_pb2.StopKibanaMsg()
    elk_dto = stub.stopKibana(stop_kibana_msg, timeout=timeout)
    return elk_dto


def start_kibana(stub: csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub,
                 timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
    """
    Sends a request to the ELK server to start Kibana

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an ElkDTO describing the status of the ELK server
    """
    start_kibana_msg = csle_collector.elk_manager.elk_manager_pb2.StartKibanaMsg()
    elk_dto = stub.startKibana(start_kibana_msg, timeout=timeout)
    return elk_dto


def stop_logstash(stub: csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub,
                  timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
    """
    Sends a request to the ELK server to stop Logstash

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an ElkDTO describing the status of the ELK stack
    """
    stop_logstash_msg = csle_collector.elk_manager.elk_manager_pb2.StopKibanaMsg()
    elk_dto = stub.stopLogstash(stop_logstash_msg, timeout=timeout)
    return elk_dto


def start_logstash(stub: csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub,
                   timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
    """
    Sends a request to the ELK server to start Logstash

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: an ElkDTO describing the status of the ELK server
    """
    start_logstash_msg = csle_collector.elk_manager.elk_manager_pb2.StartKibanaMsg()
    elk_dto = stub.startLogstash(start_logstash_msg, timeout=timeout)
    return elk_dto
