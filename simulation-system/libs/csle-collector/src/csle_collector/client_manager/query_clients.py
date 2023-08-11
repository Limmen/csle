from typing import List
import csle_collector.client_manager.client_manager_pb2_grpc
import csle_collector.client_manager.client_manager_pb2
from csle_collector.client_manager.dao.workflows_config import WorkflowsConfig
from csle_collector.client_manager.dao.client import Client
import csle_collector.constants.constants as constants


def get_clients(stub: csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub,
                timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
    """
    Queries the server for the client state

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a clientsDTO describing the state of the clients
    """
    get_clients_dto_msg = csle_collector.client_manager.client_manager_pb2.GetClientsMsg()
    clients_dto: csle_collector.client_manager.client_manager_pb2.ClientsDTO = \
        stub.getClients(get_clients_dto_msg, timeout=timeout)
    return clients_dto


def stop_clients(stub: csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub,
                 timeout=constants.GRPC.TIMEOUT_SECONDS):
    """
    Stops the client arrival process

    :param stub: the stub to the gRPC server
    :param timeout: the GRPC timeout (seconds)
    :return: a clientsDTO describing the state of the clients
    """
    stop_clients_msg = csle_collector.client_manager.client_manager_pb2.StopClientsMsg()
    clients_dto: csle_collector.client_manager.client_manager_pb2.ClientsDTO = \
        stub.stopClients(stop_clients_msg, timeout=timeout)
    return clients_dto


def start_clients(stub: csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub,
                  time_step_len_seconds: int, workflows_config: WorkflowsConfig, clients: List[Client],
                  timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
    """
    Starts the client arrival process

    :param stub: the stub to the gRPC server
    :param time_step_len_seconds: length of a time-step in the emulation
    :param workflows_config: configuration of the workflows
    :param clients: list of client profiles
    :param timeout: the timeout for sending a request to the GRPC server
    :return: a clients DTO describing the state of the clients
    """
    clients_grpcs = list(map(lambda x: x.to_grpc_object(), clients))
    workflows_config_grpc = workflows_config.to_grpc_object()
    start_clients_msg = csle_collector.client_manager.client_manager_pb2.StartClientsMsg(
        time_step_len_seconds=time_step_len_seconds, clients=clients_grpcs,
        workflows_config=workflows_config_grpc)
    clients_dto: csle_collector.client_manager.client_manager_pb2.ClientsDTO = \
        stub.startClients(start_clients_msg, timeout=timeout)
    return clients_dto


def stop_producer(stub: csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub,
                  timeout=constants.GRPC.TIMEOUT_SECONDS):
    """
    Stops the producer process

    :param stub: the stub to the gRPC server
    :param timeout: the GRPC timeout (seconds)
    :return: a clientsDTO describing the state of the clients
    """
    stop_producer_msg = csle_collector.client_manager.client_manager_pb2.StopProducerMsg()
    clients_dto = stub.stopProducer(stop_producer_msg, timeout=timeout)
    return clients_dto


def start_producer(stub: csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub, ip: str, port: int,
                   time_step_len_seconds: int, timeout=constants.GRPC.TIMEOUT_SECONDS):
    """
    Stops the producer process

    :param stub: the stub to the gRPC server
    :param ip: ip of the kafka server to produce to
    :param port: port of the kafka server to produce to
    :param timeout: the GRPC timeout (seconds)
    :return: a clientsDTO describing the state of the clients
    """
    start_producer_msg = csle_collector.client_manager.client_manager_pb2.StartProducerMsg(
        ip=ip,
        port=port,
        time_step_len_seconds=time_step_len_seconds
    )
    clients_dto = stub.startProducer(start_producer_msg, timeout=timeout)
    return clients_dto
